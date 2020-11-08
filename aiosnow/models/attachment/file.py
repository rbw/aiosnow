from __future__ import annotations

import os
from typing import BinaryIO

from aiosnow.utils import convert_size


class FileHandler:
    def __init__(self, file_name: str, dir_path: str = "."):
        self.file_path = os.path.join(dir_path, file_name)
        self.file = self._open()
        self.open = True

    def _open(self) -> BinaryIO:
        raise NotImplementedError

    def read(self) -> bytes:
        raise NotImplementedError

    def write(self, data: bytes) -> None:
        raise NotImplementedError

    def __enter__(self) -> FileHandler:
        return self

    def __exit__(self, *_: tuple) -> None:
        self.open = False
        self.file.close()


class FileWriter(FileHandler):
    bytes_written: int

    def __repr__(self) -> str:
        written, unit = convert_size(self.bytes_written)
        return (
            f"<{self.__class__.__name__} [path: {self.file_path}, "
            f"open: {self.open}, written: {written}{unit}]>"
        )

    def _open(self) -> BinaryIO:
        self.bytes_written = 0
        dir_path = os.path.dirname(self.file_path)
        os.makedirs(dir_path, exist_ok=True)
        return open(self.file_path, "wb")

    def write(self, data: bytes) -> None:
        self.bytes_written += self.file.write(data)

    def read(self) -> bytes:
        pass


class FileReader(FileHandler):
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} [path: {self.file_path}, open: {self.open}]>"
        )

    def _open(self) -> BinaryIO:
        return open(self.file_path, "rb")

    def read(self) -> bytes:
        return self.file.read()

    def write(self, data: bytes) -> None:
        pass
