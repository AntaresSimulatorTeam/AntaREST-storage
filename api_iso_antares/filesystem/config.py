import re
from copy import deepcopy
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple

from api_iso_antares.antares_io.reader import IniReader
from api_iso_antares.custom_types import JSON


class DTO:
    """
    Implement basic method for DTO objects
    """

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self)) and self.__dict__ == other.__dict__
        )

    def __str__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                [
                    "{}={}".format(k, str(self.__dict__[k]))
                    for k in sorted(self.__dict__)
                ]
            ),
        )

    def __repr__(self) -> str:
        return self.__str__()


class Link(DTO):
    def __init__(self, filters_synthesis: List[str], filters_year: List[str]):
        self.filters_synthesis = filters_synthesis
        self.filters_year = filters_year

    @staticmethod
    def from_json(properties: JSON) -> "Link":
        return Link(
            filters_year=Link.split(properties["filter-year-by-year"]),
            filters_synthesis=Link.split(properties["filter-synthesis"]),
        )

    @staticmethod
    def split(line: str) -> List[str]:
        return [
            token.strip() for token in line.split(",") if token.strip() != ""
        ]


class Area(DTO):
    def __init__(
        self,
        links: Dict[str, Link],
        thermals: List[str],
        filters_synthesis: List[str],
        filters_year: List[str],
    ):
        self.links = links
        self.thermals = thermals
        self.filters_synthesis = filters_synthesis
        self.filters_year = filters_year


class Simulation(DTO):
    def __init__(
        self,
        name: str,
        date: str,
        mode: str,
        nbyears: int,
        synthesis: bool,
        by_year: bool,
    ):
        self.name = name
        self.date = date
        self.mode = mode
        self.nbyears = nbyears
        self.synthesis = synthesis
        self.by_year = by_year

    def get_file(self) -> str:
        modes = {"economy": "eco", "adequacy": "adq"}
        dash = "-" if self.name else ""
        return f"{self.date}{modes[self.mode]}{dash}{self.name}"


class Config(DTO):
    def __init__(
        self,
        study_path: Path,
        areas: Optional[Dict[str, Area]] = None,
        outputs: Optional[Dict[int, Simulation]] = None,
    ):
        self.root_path = study_path
        self.path = study_path
        self.areas = areas or dict()
        self.outputs = outputs or dict()

    def next_file(self, name: str) -> "Config":
        copy = deepcopy(self)
        copy.path = copy.path / name
        return copy

    @property
    def area_names(self) -> List[str]:
        return list(self.areas.keys())

    def get_thermals(self, area: str) -> List[str]:
        return self.areas[area].thermals

    def get_links(self, area: str) -> List[str]:
        return list(self.areas[area].links.keys())

    def get_filters_synthesis(
        self, area: str, link: Optional[str] = None
    ) -> List[str]:
        if link:
            return self.areas[area].links[link].filters_synthesis
        return self.areas[area].filters_synthesis

    def get_filters_year(
        self, area: str, link: Optional[str] = None
    ) -> List[str]:
        if link:
            return self.areas[area].links[link].filters_year
        return self.areas[area].filters_year

    @staticmethod
    def from_path(study_path: Path) -> "Config":
        return ConfigPathBuilder.build(study_path)

    @staticmethod
    def from_json(json: JSON, study_path: Path) -> "Config":
        return ConfigJsonBuilder.build(study_path, json)


class ConfigPathBuilder:
    @staticmethod
    def build(study_path: Path) -> "Config":
        return Config(
            study_path=study_path,
            areas=ConfigPathBuilder._parse_areas(study_path),
            outputs=ConfigPathBuilder._parse_outputs(study_path),
        )

    @staticmethod
    def _parse_areas(root: Path) -> Dict[str, Area]:
        areas = (root / "input/areas/list.txt").read_text().split("\n")
        areas = [a.lower() for a in areas if a != ""]
        return {a: ConfigPathBuilder.parse_area(root, a) for a in areas}

    @staticmethod
    def _parse_outputs(root: Path) -> Dict[int, Simulation]:
        files = sorted((root / "output").iterdir())
        return {
            i + 1: ConfigPathBuilder.parse_simulation(f)
            for i, f in enumerate(files)
        }

    @staticmethod
    def parse_simulation(path: Path) -> "Simulation":
        modes = {"eco": "economy", "adq": "adequacy"}
        regex: Any = re.search(
            "^([0-9]{8}-[0-9]{4})(eco|adq)-?(.*)", path.name
        )
        nbyears, by_year, synthesis = ConfigPathBuilder._parse_parameters(path)
        return Simulation(
            date=regex.group(1),
            mode=modes[regex.group(2)],
            name=regex.group(3),
            nbyears=nbyears,
            by_year=by_year,
            synthesis=synthesis,
        )

    @staticmethod
    def _parse_parameters(path: Path) -> Tuple[int, bool, bool]:
        par: JSON = IniReader().read(path / "about-the-study/parameters.ini")
        return (
            par["general"]["nbyears"],
            par["general"]["year-by-year"],
            par["output"]["synthesis"],
        )

    @staticmethod
    def parse_area(root: Path, area: str) -> "Area":
        return Area(
            links=ConfigPathBuilder._parse_links(root, area),
            thermals=ConfigPathBuilder._parse_thermal(root, area),
            filters_synthesis=ConfigPathBuilder._parse_filters_synthesis(
                root, area
            ),
            filters_year=ConfigPathBuilder._parse_filters_year(root, area),
        )

    @staticmethod
    def _parse_thermal(root: Path, area: str) -> List[str]:
        list_ini = IniReader().read(
            root / f"input/thermal/clusters/{area}/list.ini"
        )
        return list(list_ini.keys())

    @staticmethod
    def _parse_links(root: Path, area: str) -> Dict[str, Link]:
        properties_ini = IniReader().read(
            root / f"input/links/{area}/properties.ini"
        )
        return {
            link: Link.from_json(properties_ini[link])
            for link in list(properties_ini.keys())
        }

    @staticmethod
    def _parse_filters_synthesis(root: Path, area: str) -> List[str]:
        filters: str = IniReader().read(
            root / f"input/areas/{area}/optimization.ini"
        )["filtering"]["filter-synthesis"]
        return Link.split(filters)

    @staticmethod
    def _parse_filters_year(root: Path, area: str) -> List[str]:
        filters: str = IniReader().read(
            root / f"input/areas/{area}/optimization.ini"
        )["filtering"]["filter-year-by-year"]
        return Link.split(filters)


class ConfigJsonBuilder:
    @staticmethod
    def build(study_path: Path, json: JSON) -> "Config":
        return Config(
            study_path=study_path,
            areas=ConfigJsonBuilder._parse_areas(json),
            outputs=ConfigJsonBuilder._parse_outputs(json),
        )

    @staticmethod
    def _parse_areas(json: JSON) -> Dict[str, Area]:
        areas = list(json["input"]["areas"])
        areas = [a for a in areas if a not in ["sets", "list"]]
        return {a: ConfigJsonBuilder._parse_area(json, a) for a in areas}

    @staticmethod
    def _parse_outputs(json: JSON) -> Dict[int, Simulation]:
        outputs = json["output"]
        return {
            int(i): ConfigJsonBuilder._parse_simulation(s)
            for i, s in outputs.items()
        }

    @staticmethod
    def _parse_simulation(json: JSON) -> "Simulation":
        nbyears, by_year, synthesis = ConfigJsonBuilder._parse_parameters(
            json["about-the-study"]["parameters"]
        )
        info = json["info"]["general"]
        return Simulation(
            date=info["date"]
            .replace(".", "")
            .replace(":", "")
            .replace(" ", ""),
            mode=info["mode"].lower(),
            name=info["name"],
            nbyears=nbyears,
            by_year=by_year,
            synthesis=synthesis,
        )

    @staticmethod
    def _parse_parameters(json: JSON) -> Tuple[int, bool, bool]:
        return (
            json["general"]["nbyears"],
            json["general"]["year-by-year"],
            json["output"]["synthesis"],
        )

    @staticmethod
    def _parse_area(json: JSON, area: str) -> "Area":
        return Area(
            links=ConfigJsonBuilder._parse_links(json, area),
            thermals=ConfigJsonBuilder._parse_thermal(json, area),
            filters_synthesis=ConfigJsonBuilder._parse_filters_synthesis(
                json, area
            ),
            filters_year=ConfigJsonBuilder._parse_filters_year(json, area),
        )

    @staticmethod
    def _parse_thermal(json: JSON, area: str) -> List[str]:
        list_ini = json["input"]["thermal"]["clusters"][area]["list"]
        return list(list_ini.keys())

    @staticmethod
    def _parse_links(json: JSON, area: str) -> Dict[str, Link]:
        properties_ini = json["input"]["links"][area]["properties"]
        return {
            link: Link(
                filters_synthesis=Link.split(
                    properties_ini[link]["filter-synthesis"]
                ),
                filters_year=Link.split(
                    properties_ini[link]["filter-year-by-year"]
                ),
            )
            for link in list(properties_ini.keys())
        }

    @staticmethod
    def _parse_filters_synthesis(json: JSON, area: str) -> List[str]:
        filters: str = json["input"]["areas"][area]["optimization"][
            "filtering"
        ]["filter-synthesis"]
        return Link.split(filters)

    @staticmethod
    def _parse_filters_year(json: JSON, area: str) -> List[str]:
        filters: str = json["input"]["areas"][area]["optimization"][
            "filtering"
        ]["filter-year-by-year"]
        return Link.split(filters)