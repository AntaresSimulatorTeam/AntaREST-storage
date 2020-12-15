from api_iso_antares.filesystem.config import Config
from api_iso_antares.filesystem.folder_node import FolderNode
from api_iso_antares.filesystem.inode import TREE
from api_iso_antares.filesystem.root.output.simulation.adequacy.mcall.areas.item.details import (
    OutputSimulationAdequacyMcAllAreasItemDetails as Details,
)
from api_iso_antares.filesystem.root.output.simulation.adequacy.mcall.areas.item.id import (
    OutputSimulationAdequacyMcAllAreasItemId as Id,
)
from api_iso_antares.filesystem.root.output.simulation.adequacy.mcall.areas.item.values import (
    OutputSimulationAdequacyMcAllAreasItemValues as Values,
)


class OutputSimulationAdequacyMcAllAreasItem(FolderNode):
    def __init__(self, config: Config, area: str):
        FolderNode.__init__(self, config)
        self.area = area

    def build(self, config: Config) -> TREE:
        children: TREE = dict()

        for timing in config.get_filters_synthesis(self.area):
            children[f"details-{timing}"] = Details(
                config.next_file(f"details-{timing}.txt")
            )

        for timing in config.get_filters_synthesis(self.area):
            children[f"id-{timing}"] = Id(config.next_file(f"id-{timing}.txt"))

        for timing in config.get_filters_synthesis(self.area):
            children[f"values-{timing}"] = Values(
                config.next_file(f"values-{timing}.txt")
            )

        return children