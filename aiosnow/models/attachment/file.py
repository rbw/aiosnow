import os

from .utils import convert_size


class FileHandler:
    def __init__(self, file_name, dir_name="."):
        self.path = os.path.join(dir_name, file_name)
        self.file = self._open()
        self.open = True

    def _open(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open = False
        self.file.close()


class FileWriter(FileHandler):
    bytes_written: int

    def __repr__(self):
        written, unit = convert_size(self.bytes_written)
        return (
            f"<{self.__class__.__name__} [path: {self.path}, "
            f"open: {self.open}, written: {written}{unit}]>"
        )

    def _open(self):
        self.bytes_written = 0
        return open(self.path, "wb")

    def write(self, data):
        self.bytes_written += self.file.write(data)


class FileReader(FileHandler):
    def __repr__(self):
        return (
            f"<{self.__class__.__name__} [path: {self.path}, open: {self.open}]>"
        )

    def _open(self):
        return open(self.path, "rb")

    def read(self):
        return self.file.read()
