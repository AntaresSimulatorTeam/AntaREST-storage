from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.input.hydro.prepro.area.area import (
    InputHydroPreproArea,
)
from antarest.storage.repository.filesystem.root.input.hydro.prepro.correlation import (
    InputHydroPreproCorrelation,
)


class InputHydroPrepro(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            a: InputHydroPreproArea(config.next_file(a))
            for a in config.area_names()
        }
        children["correlation"] = InputHydroPreproCorrelation(
            config.next_file("correlation.ini")
        )
        return children
