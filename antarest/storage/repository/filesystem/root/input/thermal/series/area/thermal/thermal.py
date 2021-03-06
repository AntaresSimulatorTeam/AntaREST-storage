from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.input.thermal.series.area.thermal.series import (
    InputThermalSeriesAreaThermalSeries,
)


class InputThermalSeriesAreaThermal(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            "series": InputThermalSeriesAreaThermalSeries(
                config.next_file("series.txt")
            ),
        }
        return children
