from antarest.storage_api.filesystem.config.model import StudyConfig
from antarest.storage_api.filesystem.folder_node import FolderNode
from antarest.storage_api.filesystem.inode import TREE
from antarest.storage_api.filesystem.root.settings.resources.study_ico import (
    StudyIcon,
)


class Resources(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {"study": StudyIcon(config.next_file("study.ico"))}
        return children
