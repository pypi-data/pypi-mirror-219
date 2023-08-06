# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Constants used in both server and client implementation.
"""

import numpy as np

version = 0, 0, 20

# Default server port.
server_tcp_port = 9999
server_udp_port = 9999
server_websocket_port = 9998

# Audio format.
sample_rate = 16000 #2 ** 14
# Number of audio channels.
num_channels = 1
# Number of samples in an audio frame.
frame_size = 512
# Audio sample data type.
sample_data_type = np.dtype(np.int16).newbyteorder('<')
# Size of a sample in bytes.
sample_size = 2

# Data type of audio meta tags.
# This describes the data structures used for encryption appended to each audio frame.
audio_tag_data_type = np.dtype([('peer_id', np.uint16), ('nonce', np.uint32)]).newbyteorder('>')

# Numpy data types.
uint8_t = np.dtype(np.uint8).newbyteorder('>')
uint16_t = np.dtype(np.uint16).newbyteorder('>')

# Identification (address) of server. Do not change this.
server_id = 1
