from pathlib import Path
from typing import Tuple

from pydantic import BaseModel

from .. import ENCODING
from ..utils.paths import root_path


class ConfigModel(BaseModel):

    __filenames__: Tuple[str, ...]

    def save_to_file_path(self, path: Path):
        self_json = self.json(ensure_ascii=False, indent=2)
        path.write_text(self_json, encoding=ENCODING)

    @classmethod
    def __filepaths__(cls):
        for filename in cls.__filenames__:
            yield root_path / filename

    @classmethod
    def __exist_filepaths__(cls):
        for filepath in cls.__filepaths__():
            if filepath.exists():
                yield filepath

    @classmethod
    def load_from_path(cls, path: Path):
        return cls.parse_file(path, encoding=ENCODING)

    @classmethod
    def load_first(cls):
        for filepath in cls.__exist_filepaths__():
            return cls.load_from_path(filepath)

        raise FileNotFoundError("Count not find any model file")

    @classmethod
    def update(cls, path: Path):
        if not path.exists():
            return

        model_object = cls.load_from_path(path)
        model_object.save_to_file_path(path)

    @classmethod
    def refresh(cls, path: Path):
        if not path.exists():
            return

        model_object = cls()  # type: ignore
        model_object.save_to_file_path(path)
