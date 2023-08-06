# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import numpy as np
from typing import List


class AudioProcessor:

    async def process(self, data: List[np.ndarray]) -> List[np.ndarray]:
        raise NotImplementedError()


class FrameResizer(AudioProcessor):

    def __init__(self, output_frame_size: int):
        assert output_frame_size > 0, "Invalid frame size."
        self.output_frame_size = output_frame_size
        self.buffer = None

    async def process(self, data: List[np.ndarray]) -> List[np.ndarray]:
        if self.buffer is None:
            self.buffer = np.concatenate(data)
        else:
            self.buffer = np.concatenate([self.buffer] + data)

        out = []
        while len(self.buffer) >= self.output_frame_size:
            out.append(self.buffer[:self.output_frame_size])
            self.buffer = self.buffer[self.output_frame_size:]
        return out


class AudioProcessorPipeline(AudioProcessor):

    def __init__(self, *processors: AudioProcessor):
        self.processors: List[AudioProcessor] = list(processors)

    async def process(self, data: List[np.ndarray]) -> List[np.ndarray]:
        for p in self.processors:
            data = await p.process(data)
        return data
