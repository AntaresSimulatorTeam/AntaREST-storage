from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.input.wind.series.area import (
    InputWindSeriesArea,
)


class InputWindSeries(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            f"wind_{a}": InputWindSeriesArea(config.next_file(f"wind_{a}.txt"))
            for a in config.area_names()
        }
        return children
