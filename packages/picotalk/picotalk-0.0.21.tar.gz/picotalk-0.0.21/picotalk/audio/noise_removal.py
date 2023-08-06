# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import numpy as np
from typing import List
from .audio_processor import AudioProcessor


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


class NoiseRemover(AudioProcessor):
    """
    Try to estimate the noise profile and suppress the background noise.
    """

    def __init__(self, frame_size: int, sample_rate: int):
        self.frame_size = frame_size
        self.sample_rate = sample_rate

        self.previous_frame = None
        self.average_magnitude = 0
        self.noise_gate = None

    async def process(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        return [self.__process_single_frame(frame)
                for frame in frames
                if frame is not None
                ]

    def __process_single_frame(self, frame: np.ndarray) -> np.ndarray:

        assert frame.shape == (self.frame_size,), "Wrong frame size."

        if self.previous_frame is None:
            self.previous_frame = np.zeros_like(frame)

        # Concatenate the previous frame and the new frame.
        # This is used to create a sliding window effect.
        signal = np.concatenate([self.previous_frame, frame])
        self.previous_frame = frame

        fft = np.fft.rfft(signal)
        magnitude = np.abs(fft)

        if self.noise_gate is None:
            self.noise_gate = np.zeros_like(fft)

        # Adaption speed
        a = 0.01
        # Compute moving average of the magnitude using a first order IIR filter.
        self.average_magnitude = a * magnitude + (1 - a) * self.average_magnitude

        # Compute noise gate for each point in time.

        # Tell how fast a noise gate opens (1 = fastest, 0 = infinitely slow).
        attack = 1
        # Tell how fast a noise gate closes.
        release = 0.4

        gate_opens = magnitude > self.average_magnitude * (2 - 1 * self.noise_gate)  # Hysteresis
        gate_closes = ~gate_opens
        self.noise_gate[gate_opens] = attack * 1 + (1 - attack) * self.noise_gate[gate_opens]
        self.noise_gate[gate_closes] = release * 0 + (1 - release) * self.noise_gate[gate_closes]

        # Clip the filter response in time domain.
        filter_response = np.fft.irfft(self.noise_gate)
        l = len(filter_response)
        filter_response[l // 8:] = 0
        # x = np.linspace(0, 128, num=len(filter_response))
        # filter_response *= np.exp(-x ** 2)
        noise_gate = np.fft.rfft(filter_response)

        # Suppress the noise.
        fft_gated = fft * noise_gate

        # Inverse FFT.
        signal_out = np.real(np.fft.irfft(fft_gated))

        # Return only the center part of the enlarged frame.
        signal_out = signal_out[len(frame) // 2:len(frame) // 2 + len(frame)]

        return signal_out.astype(np.int16)
