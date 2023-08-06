# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import asyncio
from concurrent.futures import ThreadPoolExecutor
import pyaudio
import numpy as np
import scipy.signal
import sys
import struct
import argparse
import logging
import itertools

from typing import Callable, Coroutine, Dict, Optional
import nacl.hash
import nacl.secret
import nacl.bindings
import nacl.utils

from . import common
from .audio.audio_processor import AudioProcessor, AudioProcessorPipeline
from .audio.squelch import Squelch
from .audio.noise_removal import NoiseRemover

from .transports.packet import TLVPacket, PacketType
from .transports.base import Connection
from .transports import udp as transport_udp, tcp as transport_tcp, websocket as transport_ws, \
    encrypted as transport_enc

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(name)8s %(levelname)8s %(message)s')
logger = logging.getLogger("Main")

# PyAudio singleton.
audio: pyaudio.PyAudio = pyaudio.PyAudio()

# Audio format to be used.
audio_format = pyaudio.paInt16

# Thread pool for running blocking tasks
# such as reading from the microphone and writing to the speakers and reading from stdin.
thread_pool = ThreadPoolExecutor()

# Struct used to create the nonce for the encryption of an audio frame.
_nonce_struct = struct.Struct(">HI")


def _runtime_check_nacl():
    """
    Verify that NaCl puts the 16-byte authenticator
    in front of the cipher text.
    This is required for the `generate_key_stream()` function.
    :return:
    """

    key = b"\00" * 32
    nonce = b"\00" * 24
    # Generate two cipher text from slightly plaintext that differ only in a single bit.
    # The same key and nonce are used for both.
    # The authenticators of the ciphertexts should differ significantly, while the encrypted data should differ
    # by only one bit.
    c1 = nacl.bindings.crypto_secretbox(b"\00" * 17, nonce, key)
    c2 = nacl.bindings.crypto_secretbox(b"\01" + b"\00" * 16, nonce, key)

    # Check that the part where plaintext is the same also matches for the cipher texts.
    assert c1[16 + 1:] == c2[16 + 1:], "NaCl crypto_secretbox() does not behave as required."


_runtime_check_nacl()


def generate_key_stream(key: bytes,
                        peer_id: int,
                        counter: int,
                        length: int) -> np.ndarray:
    """
    Generate a pseudo random key signal that will be used to encrypt the audio signal.
    Returns an ndarray with uniformly random 16-bit integers.
    A combination of key, peer_id, counter shall be used only once. Otherwise encryption is
    not secure anymore.
    :param key: Encryption key.
    :param peer_id: ID of the sender.
    :param counter: Frame counter, this is used as a nonce.
    :param length: Length of the ndarray.
    :return:
    """
    assert 0 <= peer_id <= 2 ** 16
    assert 0 <= counter <= 2 ** 32

    assert len(key) == 32, "Key must be exactly 32 bytes."

    # Construct the nonce.
    nonce = _nonce_struct.pack(peer_id, counter) + b"\00" * 18
    assert len(nonce) == 24, "Key must be exactly 24 bytes."

    # Construct key stream.
    zeros = b"\x00" * (length * common.sample_size)
    key_stream = nacl.bindings.crypto_secretbox(zeros, nonce, key)

    assert len(key_stream) == len(zeros) + nacl.secret.SecretBox.MACBYTES
    # Cut away the authenticator (16 bytes).
    key_stream = key_stream[nacl.secret.SecretBox.MACBYTES:]  # 16 byte authenticator is prepended.

    # Convert the key stream into integers of the same bit length as the audio samples.
    key_signal = np.frombuffer(key_stream, dtype=common.sample_data_type)
    assert key_signal.dtype == common.sample_data_type, "Frame has wrong data type."
    assert len(key_signal) == length, "Key stream has wrong length."

    return key_signal


def encrypt_audio_frame(frame: np.ndarray, key: bytes,
                        peer_id: int,
                        counter: int) -> np.ndarray:
    """
    Encrypt an audio frame by adding pseudo-random white noise
    generated from the key, peer_id and counter.
    The key is added element wise modulo 2**16.
    A combination of key, peer_id, counter shall be used only once. Otherwise encryption is
    not secure anymore.
    :param frame:
    :param key:
    :param peer_id:
    :param counter:
    :return: The encrypted signal as a np.ndarray.
    """

    key_signal = generate_key_stream(key, peer_id, counter, len(frame))

    # Add the key stream to the signal.
    return frame + key_signal


def decrypt_audio_frame(frame: np.ndarray, key: bytes,
                        peer_id: int,
                        counter: int) -> np.ndarray:
    """
    Decrypt an audio frame by subtracting pseudo-random white noise
    generated from the key, peer_id and counter.
    A combination of key, peer_id, counter shall be used only once. Otherwise encryption is
    not secure anymore.
    :param frame:
    :param key:
    :param peer_id:
    :param counter:
    :return: The encrypted signal as a np.ndarray.
    """

    key_signal = generate_key_stream(key, peer_id, counter, len(frame))

    # Subtract the key stream to the signal.
    return frame - key_signal


async def run_speaker(audio_buffer: asyncio.Queue):
    """
    Read audio frames from the queue and write them to the audio output.
    """
    logger.debug("Start speaker task.")

    # Open audio output stream (to speaker).
    stream_out = audio.open(format=audio_format,
                            channels=common.num_channels,
                            rate=common.sample_rate,
                            output=True,
                            frames_per_buffer=common.frame_size)

    async def speaker_task():
        silence = np.zeros(common.frame_size, dtype=common.sample_data_type)

        playback_speed = 1.0
        estimated_latency = 0.0
        target_latency_min = 4
        target_latency_max = audio_buffer.maxsize / 2
        assert target_latency_min < target_latency_max
        # Target latency in frames.
        target_latency = 4

        while True:

            while audio_buffer.full():
                # If the buffer is full, then potentially
                # there is also a backlog in the TCP buffer.
                # Skip a frame to catch up with latency.
                logger.debug("Full buffer: drop a frame.")
                audio_buffer.get_nowait()
                await asyncio.sleep(0)

            # Computations for adaptive playback speed.
            a = 0.01
            estimated_latency = a * audio_buffer.qsize() + (1 - a) * estimated_latency

            if estimated_latency < target_latency:
                target_playback_speed = 1 + 0.005 * (estimated_latency - target_latency)
            else:
                target_playback_speed = 1 + 0.2 * (estimated_latency - target_latency)

            playback_speed = target_playback_speed

            if audio_buffer.qsize() > 0:
                frame = audio_buffer.get_nowait()
            else:
                # logger.debug("Inject silence.")
                # Slightly increase target latency if there is frames missing.
                target_latency = min(target_latency_max, target_latency + 0.01)
                frame = silence

            a = 0.0001
            target_latency = max(target_latency_min, (1 - a) * target_latency + a * target_latency_min)

            target_frame_size = int(len(frame) / playback_speed)
            frame = scipy.signal.resample(frame, target_frame_size)

            # Write the frame to the output audio stream in a separate thread.
            def write_to_speaker():
                stream_out.write(frame.astype(np.int16), len(frame))

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(thread_pool, write_to_speaker)

    _speaker_task = asyncio.create_task(speaker_task())

    await _speaker_task


class PeerConnection(Connection):
    """
    Connection to a peer routed via the server.
    Makes sure that the destination address is always correctly set.
    """

    def __init__(self, receive_packet, send_packet):
        super().__init__()
        self.send_packet = send_packet
        self.receive_packet = receive_packet

    async def read_packet(self) -> TLVPacket:
        return await self.receive_packet()

    async def write_packet(self, p: TLVPacket):
        return await self.send_packet(p)


class Peer:
    """
    Data structure for another peer.
    """

    def __init__(self, peer_id: int, send_packet, password: bytes, is_initiator: bool):
        """

        :param peer_id: ID of the other peer.
        :param send_packet: Async function for sending a packet to the server.
        :param password: Password for the authenticated key exchange.
        :param is_initiator: Tell if this local object initiates the key exchange.
        """
        self.msq_queue_in = asyncio.Queue()
        self.peer_id = peer_id
        self.password = password
        self.peer_name: Optional[str] = None
        self.audio_encryption_key: Optional[bytes] = None

        # Send packet to server.
        self.send_packet = send_packet

        # Connection to server.
        async def rx():
            return await self.msq_queue_in.get()

        async def tx(p: TLVPacket):
            p.dest_addr = peer_id
            await send_packet(p)

        # Unencrypted connection to the peer.
        self.conn_plain = PeerConnection(rx, tx)
        # End-to-end encrypted connection to peer.
        self.conn_e2e = asyncio.get_event_loop().create_future()
        asyncio.create_task(self.run_key_exchange(password, is_initiator))
        asyncio.create_task(self.run())

    async def send_to_server(self, p: TLVPacket):
        """
        Send and address a packet to the server.
        """
        p.dest_addr = common.server_id
        await self.send_packet(p)

    def close(self):
        """
        Close this peer connection.
        """
        pass

    async def run(self):
        """
        Process incoming packets from other peers.
        """
        conn = await self.conn_e2e
        while True:
            p = await conn.read_packet()
            logger.debug(f"Got encrypted packet from peer: {p.data}")

            if p.type == PacketType.JSON:
                d = p.to_dict()
                if 'user_name' in d:
                    self.peer_name = d['user_name']
                    print("User joined:", self.peer_name)
                if 'chat_message' in d:
                    msg = d['chat_message']
                    if msg.strip():
                        print(f"{self.peer_name}: {msg}")
                if 'audio_encryption_key' in d:
                    hex_key = d['audio_encryption_key']
                    logger.debug(f"Received audio encryption key: {hex_key}")
                    key = bytes.fromhex(hex_key)
                    self.audio_encryption_key = key

    async def send_to_peer(self, p: TLVPacket):
        """
        Send a packet to the peer over the end-to-end encrypted channel.
        """
        conn = await self.conn_e2e
        await conn.write_packet(p)

    async def run_key_exchange(self, password: bytes, is_initiator: bool):
        """
        Run authenticated key exchange with other peer.
        If the key exchange is successfull the 'self.conn_e2e' future will be set.
        """
        logger.debug(f"Run start key exchange with peer {self.peer_id}.")
        shared_key = await transport_enc.password_authenticated_key_exchange(self.conn_plain,
                                                                             password)
        logger.debug(f"Shared secret: {shared_key}.")

        box = nacl.secret.SecretBox(key=shared_key)

        conn_e2e = transport_enc.SecureConnection(box, self.conn_plain,
                                                  is_initiator=is_initiator,
                                                  nonce=0)

        # Send confirmation packet over the encrypted channel.
        tx = asyncio.create_task(conn_e2e.write_packet(TLVPacket.from_dict(status='ok')))
        rx = conn_e2e.read_packet()

        # TODO Handle reception of packets encrypted with wrong key.
        # -> They signal that the key exchange was not successful, i.e. performed with
        # different passwords.
        response = await rx
        await tx

        d = response.to_dict()
        if d.get('status') == 'ok':
            # Key exchange was successful.
            logger.debug("Key exchange was successful.")

            # Notify the server that the peer is authenticated.
            await self.send_to_server(TLVPacket.from_dict(event='peer_authenticated',
                                                          peer_id=self.peer_id))

            self.conn_e2e.set_result(conn_e2e)
        else:
            logger.warning("Key exchange failed.")

    async def handle_packet_from_peer(self, p: TLVPacket):
        logger.debug(f"Handle packet from peer {p.src_addr}, type={p.type}.")
        self.msq_queue_in.put_nowait(p)


class PicoTalkClient:

    def __init__(self, password: bytes, user_name: str):

        self.password = password
        self.user_name = user_name

        self.peer_id: Optional[int] = None

        # Main control connection to server.
        self.conn_ctrl: Optional[transport_enc.SecureConnection] = None

        # Other peers stored by their ID.
        self.peers: Dict[int, Peer] = dict()

        # Key used to encrypt audio frame.
        self.audio_encryption_key: bytes = nacl.utils.random(32)

    def get_audio_encryption_key_of_peer(self, peer_id: int) -> Optional[bytes]:
        """
        Return the key that is used by the peer `peer_id` for encrypting audio frames.
        `None` might be returned if the key is not known yet.
        :param peer_id:
        :return:
        """
        if peer_id == self.peer_id:
            return self.audio_encryption_key

        peer = self.peers[peer_id]
        if peer is not None:
            return peer.audio_encryption_key
        return None

    async def run_mic(self, send_packet: Callable[[TLVPacket], Coroutine],
                      peer_id: int,
                      _audio_processor: Optional[AudioProcessor] = None):
        """
        Read audio data and send it to the server.
        """
        logger.debug("Start microphone task.")
        # Open audio input stream.
        stream_in = audio.open(format=audio_format,
                               channels=common.num_channels,
                               rate=common.sample_rate,
                               input=True,
                               frames_per_buffer=common.frame_size)

        try:
            logger.debug('Start recording and sending audio.')

            nonce_counter = itertools.count(1)

            while True:
                await asyncio.sleep(0)

                def read_from_mic() -> np.ndarray:
                    while stream_in.get_read_available() > 2 * common.frame_size * common.sample_size:
                        # TODO: can this happen? Or is data discarded already by PyAudio?
                        # Discard data to catch up.
                        logger.debug('Discard mic data.')
                        stream_in.read(common.frame_size)
                    frame = stream_in.read(common.frame_size)
                    # Convert bytes into ndarray.
                    signal = np.frombuffer(frame, dtype=common.sample_data_type)
                    return signal

                # Read from mic in other thread.
                loop = asyncio.get_event_loop()
                frame = await loop.run_in_executor(thread_pool, read_from_mic)
                assert isinstance(frame, np.ndarray), "Frame must be an np.ndarray."
                frames = [frame]

                if _audio_processor is not None:
                    # Push the audio frame through the processor.
                    frames = await _audio_processor.process(frames)

                for frame in frames:
                    assert isinstance(frame, np.ndarray), f'Frame must be a np.ndarray not {type(frame)}.'
                    # Check if datatype is correct.
                    assert frame.dtype == common.sample_data_type, f"Wrong dtype: {frame.dtype}."

                    nonce = next(nonce_counter)

                    # Encrypt the audio frame.
                    key = self.audio_encryption_key
                    if key is not None:
                        # Encrypt frame.
                        frame_encrypted = encrypt_audio_frame(frame, key, peer_id, nonce)
                        frame_bytes = frame_encrypted.tobytes()

                        # Construct tag with the sender ID and nonce used for encryption.
                        tag = np.array([(peer_id, nonce)], dtype=common.audio_tag_data_type)
                        # Send the packet if in transmission mode.
                        data = frame_bytes + tag.tobytes()
                        # Create a packet.
                        packet = TLVPacket(PacketType.AudioFrame, data,
                                           dest_addr=1  # This is directed to the server (1).
                                           )
                        # Write this frame to the server.
                        await send_packet(packet)
                    else:
                        logger.debug("Audio encryption key is not yet known.")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Microphone task interrupted: {}".format(type(e)))
            print(e)

        logger.debug('Microphone task ended.')

    async def run_command_line_input(self):
        while True:
            loop = asyncio.get_event_loop()
            line = await loop.run_in_executor(thread_pool, sys.stdin.readline)

            # Send the line to all peers.
            # TODO: Retrieve timeout exceptions.
            for p in self.peers.values():
                t = asyncio.wait_for(p.send_to_peer(TLVPacket.from_dict(chat_message=line)),
                                     timeout=10)
                asyncio.create_task(t)

    async def say_hello_to_peer(self, peer: Peer):
        # Send my user name and my audio encryption key to the peer.

        await peer.send_to_peer(
            TLVPacket.from_dict(user_name=self.user_name,
                                audio_encryption_key=self.audio_encryption_key.hex())
        )

    async def handle_control_packet(self,
                                    p: TLVPacket):

        if p.src_addr == common.server_id:
            # Packet comes from server.

            assert p.type == PacketType.JSON
            d = p.to_dict()
            logger.debug("Control packet: {}".format(d))

            event = d.get('event')
            if event == 'peer_joined':
                peer_id = d.get('peer_id')
                logger.debug(f"Peer joined: {peer_id}")

                # Create new peer object.
                if peer_id in self.peers:
                    logger.warning(f"Peer with ID {peer_id} is already registered.")
                else:
                    # Start connection to peer.
                    peer = Peer(peer_id, self.conn_ctrl.write_packet,
                                password=self.password, is_initiator=True)
                    self.peers[peer_id] = peer

                    # Send hello message to peer.
                    asyncio.create_task(self.say_hello_to_peer(peer))

            elif event == 'peer_authenticated':
                peer_id = d.get('peer_id')
                logger.debug(f"Peer authenticated: {peer_id}")
                # TODO: Remove if not used.
            elif event == 'peer_disconnected':
                peer_id = d.get('peer_id')
                logger.debug(f"Peer disconnected: {peer_id}")
                peer = self.peers.get(peer_id)
                if peer is None:
                    logger.warning(f"Peer ID not registered: {peer_id}")
                else:
                    print(f"Peer disconnected: {peer.peer_name} ({peer_id})")

        else:
            # Packet comes from another peer.
            peer_id = p.src_addr
            peer = self.peers.get(peer_id)
            if peer is None:
                peer = Peer(peer_id, self.conn_ctrl.write_packet,
                            password=self.password, is_initiator=False)
                self.peers[peer_id] = peer
                # Send hello message to peer.
                asyncio.create_task(self.say_hello_to_peer(peer))

            # Pass the packet to the peer object.
            await peer.handle_packet_from_peer(p)

    async def receive_from_server(self,
                                  receive_packet: Callable[[], Coroutine],
                                  audio_buffer: asyncio.Queue):
        """
        Read packets from the server and handle them.
        """
        logger.debug('Start receiver task.')
        while True:
            # Wait for packet from the server.
            try:
                packet = await receive_packet()

                assert isinstance(packet, TLVPacket)

                if packet.type == PacketType.AudioFrame:
                    # Put audio packets into the audio buffer.
                    data = packet.data
                    audio_data = data[:common.frame_size * common.sample_size]
                    tag_data = data[common.frame_size * common.sample_size:]

                    # Convert frame to a numpy array.
                    frame = np.frombuffer(audio_data, dtype=common.sample_data_type)
                    audio_tags = np.frombuffer(tag_data, dtype=common.audio_tag_data_type)

                    # Decrypt the frame by stripping away the encryption layers of all senders.
                    for peer_id, nonce in audio_tags:
                        key = self.get_audio_encryption_key_of_peer(peer_id)
                        if key is None:
                            # We don't have the key that was used to encrypt this frame.
                            logger.debug(f"Cannot decrypt frame. Missing key of peer {peer_id}.")
                            # Return attenuated white noise to
                            # notify that a frame has not been decrypted.
                            frame = frame / 64  # TODO: Return silence in final version.
                            break
                        else:
                            frame = decrypt_audio_frame(frame, key, peer_id, nonce)

                    # Convert to 32 bit integer for signal processing.
                    frame = frame.astype(np.int32)

                    if audio_buffer.full():
                        # Drop oldest frame if the buffer is full.
                        # logger.debug("Drop oldest frame in FIFO.")
                        audio_buffer.get_nowait()

                    await audio_buffer.put(frame)
                else:
                    await self.handle_control_packet(packet)
            except ConnectionError as e:
                logger.debug("Connection error: {}".format(e))
                logger.debug("Stop receiver task.")
                return
            except Exception as e:
                logger.debug("Exception: {}: {}".format(type(e), e))
                await asyncio.sleep(1)  # Avoid spinning loop on an exception.

    async def run(self,
                  server_addr: str, server_port: int,
                  room_name: str,
                  user_name: str,
                  audio_processor: Optional[AudioProcessor] = None,
                  try_use_udp: bool = True):

        # Start task for reading user inputs.
        cmdline_input_task = asyncio.create_task(self.run_command_line_input())

        """
        Run the client protocol.
        """

        # Open connection to server.
        logger.debug(f'Connecting to {server_addr}:{server_port}.')
        tcp_conn = await transport_tcp.open_tcp_connection(server_addr, server_port)
        logger.debug(f'Connected to {server_addr}:{server_port}.')

        # Receive server-hello message.
        packet = await tcp_conn.read_packet()
        msg = packet.to_dict()
        logger.debug(f'Server-hello: {msg}')
        if 'version' in msg:
            # Check if server and client version are compatible.
            version = msg['version']
            assert len(version) == 3
            logger.debug('Client version: {}.{}.{}'.format(*common.version))
            logger.debug('Server version: {}.{}.{}'.format(*version))
            assert version == list(common.version), "Incompatible server version!"
        else:
            raise Exception('Protocol error: No version field in server-hello message.')

        # Derive shared secret.
        box = await transport_enc.authenticated_key_exchange(tcp_conn, initiator_role=True)

        conn_encrypted = transport_enc.SecureConnection(box, tcp_conn, is_initiator=True, nonce=1)
        self.conn_ctrl = conn_encrypted

        # Room id is the hex-hash of the room name.
        # Salted with 'room_name' to make sure
        # this hash function is distinct from others that could
        # potentially be used.
        # TODO: Use PBKDF or scrypt to derive the room ID.
        room_id = nacl.hash.sha512(
            room_name.encode('utf-8')
        )[:64].decode()

        logger.debug(f'room_id = {room_id}')

        # Write encrypted client-hello message.
        logger.debug(f'Send client-hello message.')
        await conn_encrypted.write_packet(TLVPacket.from_dict(
            room_id=room_id
        ))

        # Wait for accept-message.
        packet = await conn_encrypted.read_packet()
        msg = packet.to_dict()
        logger.debug(f'Server accepted: {msg}')

        peer_id = msg['user_id']
        logger.debug(f'User ID: {peer_id}')
        self.peer_id = peer_id  # Remember the ID.

        udp_stream_id = msg['udp_stream_id']
        logger.debug(f'UDP stream ID: {udp_stream_id}')

        udp_server_port = msg['udp_port']
        logger.debug(f'UDP server port: {udp_server_port}')

        # Create FIFO buffer for audio frames.
        # This is used to transport audio frames from the receiver task to the speaker task.
        frame_duration = common.frame_size / common.sample_rate
        buffer_size_seconds = 2
        # Calculate buffer size to be able to store 2 seconds of audio.
        max_buffer_size = int(buffer_size_seconds / frame_duration + 1) + 1
        audio_buffer = asyncio.Queue(maxsize=max_buffer_size)

        # Open UDP connection.
        udp_conn = await transport_udp.open_udp_connection(server_addr, udp_server_port, stream_id=udp_stream_id)
        # Create encrypted UDP connection which allows packets to be lost
        # but enforces packets to remain ordered.
        udp_conn = transport_enc.SecureConnection(box, udp_conn,
                                                  is_initiator=True, nonce=2,
                                                  permit_dropped_packets=True)

        use_udp = False

        # Check if UDP connection works.
        logger.debug(f"UDP check: init")
        await udp_conn.write_packet(TLVPacket.from_dict(udp_check='init'))

        try:
            logger.debug(f"UDP check: wait for server ack")
            server_ack = await asyncio.wait_for(udp_conn.read_packet(), 2)
            msg = server_ack.to_dict()
            logger.debug(f"UDP check: server ack received ({msg})")
            if msg.get('udp_check') == 'ok':
                # Acknowledge to server to use UDP.
                use_udp = True
        except asyncio.TimeoutError:
            # Tell the server not to use UDP.
            logger.debug(f"UDP check: timeout")

        if not try_use_udp:
            use_udp = False

        logger.debug(f"Using UDP: {use_udp}")
        # Tell the server whether to send audio frames over UDP or not.
        await conn_encrypted.write_packet(TLVPacket.from_dict(use_udp=use_udp))

        if not use_udp:
            # Close UDP connection again.
            udp_conn.close()

        # Launch tasks for server communication and audio.

        if use_udp:
            write_packet_mic = udp_conn.write_packet
        else:
            write_packet_mic = conn_encrypted.write_packet
        task_mic = asyncio.create_task(self.run_mic(write_packet_mic,
                                                    peer_id=peer_id,
                                                    _audio_processor=audio_processor))

        task_tcp_receiver = asyncio.create_task(self.receive_from_server(conn_encrypted.read_packet, audio_buffer))

        task_udp_receiver = asyncio.create_task(self.receive_from_server(udp_conn.read_packet, audio_buffer))

        task_speaker = asyncio.create_task(run_speaker(audio_buffer))

        try:
            # Run tasks concurrently but catch all exceptions.
            await asyncio.gather(task_tcp_receiver, task_udp_receiver, task_mic, task_speaker)
            exit()
        except Exception as e:
            logger.debug("Exiting: ", e)
            exit()


def main():
    parser = argparse.ArgumentParser(description="PicoTalk client.")
    parser.add_argument('-s', '--server', type=str,
                        metavar='REMOTE_HOST',
                        default='localhost',
                        help="Server address.")
    parser.add_argument('-p', '--port', type=int,
                        metavar='REMOTE_PORT',
                        default=common.server_tcp_port,
                        help="Server port.")
    parser.add_argument('-r', '--room', type=str,
                        metavar='ROOM_NAME',
                        required=True,
                        help="Name of the room to join.")
    parser.add_argument('-u', '--user', type=str,
                        metavar='USER_NAME',
                        default='Anonymous 🕵',
                        help="Your user name to be displayed to others.")
    parser.add_argument('--denoise',
                        action='store_true',
                        default=False,
                        help="Enable noise removal in the audio pre-processing.")

    parser.add_argument('--mic-squelch',
                        action='store_true',
                        default=False,
                        help="Transmit audio only of there is a speech signal.")

    parser.add_argument('--noudp',
                        action='store_true',
                        default=False,
                        help="Disable using UDP for the audio stream.")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help="Show more verbose log output.")
    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help="Show fine-grained debug output.")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        print("DEBUG MODE ON")
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    # Read password.
    # This password is used for authenticating the key exchange for end-to-end encryption.
    print("Enter room password:")
    password = sys.stdin.readline().replace('\n', '').encode('utf-8')

    # Set-up audio processor pipeline.
    pipeline = []
    if args.denoise:
        # pipeline.append(FrameResizer(output_frame_size=512))
        pipeline.append(NoiseRemover(frame_size=common.frame_size, sample_rate=common.sample_rate))
        # pipeline.append(FrameResizer(output_frame_size=common.frame_size))

    if args.mic_squelch:
        pipeline.append(Squelch(frame_size=common.frame_size, sample_rate=common.sample_rate))

    audio_processor = AudioProcessorPipeline(*pipeline)

    client = PicoTalkClient(password=password, user_name=args.user)

    asyncio.run(client.run(server_addr=args.server,
                           server_port=args.port,
                           room_name=args.room,
                           user_name=args.user,
                           audio_processor=audio_processor,
                           try_use_udp=not args.noudp
                           ))


if __name__ == '__main__':
    main()
