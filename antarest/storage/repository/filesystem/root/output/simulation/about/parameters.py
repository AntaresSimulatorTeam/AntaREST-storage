from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.ini_file_node import IniFileNode
from antarest.storage.repository.filesystem.root.settings.generaldata import (
    GeneralData,
)


class OutputSimulationAboutParameters(IniFileNode):
    def __init__(self, config: StudyConfig):
        IniFileNode.__init__(self, config, GeneralData.TYPES)
