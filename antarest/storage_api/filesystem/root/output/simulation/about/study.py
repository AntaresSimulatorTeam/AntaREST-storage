from antarest.storage_api.filesystem.config.model import Config
from antarest.storage_api.filesystem.ini_file_node import IniFileNode


class OutputSimulationAboutStudy(IniFileNode):
    def __init__(self, config: Config):
        types = {
            "antares": {
                "version": int,
                "caption": str,
                "created": int,
                "lastsave": int,
                "author": str,
            }
        }
        IniFileNode.__init__(self, config, types)