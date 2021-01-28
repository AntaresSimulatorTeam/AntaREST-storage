from antarest.storage_api.filesystem.config.model import Config
from antarest.storage_api.filesystem.ini_file_node import IniFileNode


class BindingConstraintsIni(IniFileNode):
    def __init__(self, config: Config):
        IniFileNode.__init__(self, config, types={})