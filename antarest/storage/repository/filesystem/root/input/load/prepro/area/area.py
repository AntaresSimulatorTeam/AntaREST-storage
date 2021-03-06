from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.input.load.prepro.area.conversion import (
    InputLoadPreproAreaConversation,
)
from antarest.storage.repository.filesystem.root.input.load.prepro.area.data import (
    InputLoadPreproAreaData,
)
from antarest.storage.repository.filesystem.root.input.load.prepro.area.k import (
    InputLoadPreproAreaK,
)
from antarest.storage.repository.filesystem.root.input.load.prepro.area.settings import (
    InputLoadPreproAreaSettings,
)
from antarest.storage.repository.filesystem.root.input.load.prepro.area.translation import (
    InputLoadPreproAreaTranslation,
)


class InputLoadPreproArea(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            "conversion": InputLoadPreproAreaConversation(
                config.next_file("conversion.txt")
            ),
            "data": InputLoadPreproAreaData(config.next_file("data.txt")),
            "k": InputLoadPreproAreaK(config.next_file("k.txt")),
            "translation": InputLoadPreproAreaTranslation(
                config.next_file("translation.txt")
            ),
            "settings": InputLoadPreproAreaSettings(
                config.next_file("settings.ini")
            ),
        }
        return children
