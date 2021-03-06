from antarest.storage.repository.filesystem.config.model import (
    StudyConfig,
    Simulation,
)
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.output.simulation.mode.mcall.mcall import (
    OutputSimulationModeMcAll,
)
from antarest.storage.repository.filesystem.root.output.simulation.mode.mcind.mcind import (
    OutputSimulationModeMcInd,
)


class OutputSimulationMode(FolderNode):
    def __init__(self, config: StudyConfig, simulation: Simulation):
        FolderNode.__init__(self, config)
        self.simulation = simulation

    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {}

        if self.simulation.by_year:
            children["mc-ind"] = OutputSimulationModeMcInd(
                config.next_file("mc-ind"), self.simulation
            )
        if self.simulation.synthesis:
            children["mc-all"] = OutputSimulationModeMcAll(
                config.next_file("mc-all")
            )

        return children
