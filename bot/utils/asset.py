from aiogram import types

from ..utils.paths import root_path

assets_path = root_path / "assets"


class Asset:
    def __init__(self, filename: str):
        self.filepath = assets_path / filename
        self.bytes = self.filepath.read_bytes()

    def to_input_file(self):
        return types.BufferedInputFile(self.bytes, self.filepath.name)
