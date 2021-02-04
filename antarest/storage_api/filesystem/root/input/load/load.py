from antarest.storage_api.filesystem.config.model import StudyConfig
from antarest.storage_api.filesystem.folder_node import FolderNode
from antarest.storage_api.filesystem.inode import TREE
from antarest.storage_api.filesystem.root.input.load.prepro.prepro import (
    InputLoadPrepro,
)
from antarest.storage_api.filesystem.root.input.load.series.series import (
    InputLoadSeries,
)


class InputLoad(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            "prepro": InputLoadPrepro(config.next_file("prepro")),
            "series": InputLoadSeries(config.next_file("series")),
        }
        return children
