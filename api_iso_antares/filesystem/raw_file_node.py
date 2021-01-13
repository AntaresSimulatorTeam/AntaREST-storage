import shutil
from typing import List, Optional

from api_iso_antares.custom_types import JSON, SUB_JSON
from api_iso_antares.filesystem.config.model import Config
from api_iso_antares.filesystem.inode import INode, TREE


class RawFileNode(INode[str, str, str]):
    def __init__(self, config: Config):
        self.config = config

    def build(self, config: Config) -> TREE:
        pass  # end node has nothing to build

    def get(self, url: Optional[List[str]] = None, depth: int = -1) -> str:
        self._assert_url(url)
        self.validate("")

        file_path = "/".join(self.config.path.absolute().parts)
        root_path = "/".join(self.config.root_path.parent.absolute().parts)
        file_relative = file_path.replace(root_path, "")
        return f"file{file_relative}"

    def save(self, data: str, url: Optional[List[str]] = None) -> None:
        self._assert_url(url)

        if "file/" in data:
            path = self.config.root_path.parent / data[len("file/") :]
        else:
            path = self.config.root_path / "res" / data

        if path != self.config.path:
            shutil.copyfile(path, self.config.path)

    def validate(self, data: str) -> None:
        assert self.config.path.exists()

    def _assert_url(self, url: Optional[List[str]] = None) -> None:
        url = url or []
        if len(url) > 0:
            raise ValueError(
                f"url should be fully resolved when arrives on {self.__class__.__name__}"
            )
