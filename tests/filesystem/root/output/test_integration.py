from pathlib import Path
from zipfile import ZipFile

import pytest

from api_iso_antares.custom_types import SUB_JSON
from api_iso_antares.filesystem.config import Config
from api_iso_antares.filesystem.root.study import Study
from tests.filesystem.utils import extract_sta


@pytest.mark.integration_test
@pytest.mark.parametrize(
    "url, exp",
    [
        (
            "output/1/about-the-study/map",
            "file/STA-mini/output/20201014-1422eco-hello/about-the-study/map",
        ),
        (
            "output/1/about-the-study/areas",
            "file/STA-mini/output/20201014-1422eco-hello/about-the-study/areas.txt",
        ),
        (
            "output/1/about-the-study/comments",
            "file/STA-mini/output/20201014-1422eco-hello/about-the-study/comments.txt",
        ),
        (
            "output/1/about-the-study/links",
            "file/STA-mini/output/20201014-1422eco-hello/about-the-study/links.txt",
        ),
        ("output/1/about-the-study/study/antares/author", "Andrea SGATTONI"),
        ("output/1/about-the-study/parameters/general/horizon", 2030),
        (
            "output/1/economy/mc-all/areas/de/id-daily",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-all/areas/de/id-daily.txt",
        ),
        (
            "output/1/economy/mc-all/grid/areas",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-all/grid/areas.txt",
        ),
        (
            "output/1/economy/mc-all/grid/digest",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-all/grid/digest.txt",
        ),
        (
            "output/1/economy/mc-all/grid/thermals",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-all/grid/thermals.txt",
        ),
        (
            "output/1/economy/mc-all/grid/links",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-all/grid/links.txt",
        ),
        (
            "output/1/economy/mc-ind/00001/areas/de/values-hourly",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-ind/00001/areas/de/values-hourly.txt",
        ),
        (
            "output/1/economy/mc-ind/00001/links/de/fr/values-hourly",
            "file/STA-mini/output/20201014-1422eco-hello/economy/mc-ind/00001/links/de - fr/values-hourly.txt",
        ),
        (
            "output/1/ts-numbers/hydro/fr",
            "file/STA-mini/output/20201014-1422eco-hello/ts-numbers/hydro/fr.txt",
        ),
        (
            "output/1/ts-numbers/load/fr",
            "file/STA-mini/output/20201014-1422eco-hello/ts-numbers/load/fr.txt",
        ),
        (
            "output/1/ts-numbers/solar/fr",
            "file/STA-mini/output/20201014-1422eco-hello/ts-numbers/solar/fr.txt",
        ),
        (
            "output/1/ts-numbers/wind/fr",
            "file/STA-mini/output/20201014-1422eco-hello/ts-numbers/wind/fr.txt",
        ),
        (
            "output/1/ts-numbers/thermal/fr/01_solar",
            "file/STA-mini/output/20201014-1422eco-hello/ts-numbers/thermal/fr/01_solar.txt",
        ),
        (
            "output/1/annualSystemCost",
            "file/STA-mini/output/20201014-1422eco-hello/annualSystemCost.txt",
        ),
        (
            "output/1/checkIntegrity",
            "file/STA-mini/output/20201014-1422eco-hello/checkIntegrity.txt",
        ),
        (
            "output/1/simulation-comments",
            "file/STA-mini/output/20201014-1422eco-hello/simulation-comments.txt",
        ),
        (
            "output/1/simulation",
            "file/STA-mini/output/20201014-1422eco-hello/simulation.log",
        ),
        ("output/1/info/general/mode", "Economy"),
    ],
)
def test_get_output_it(
    project_path: Path, tmp_path: Path, url: str, exp: SUB_JSON
) -> None:
    path = extract_sta(project_path, tmp_path)
    study = Study(config=Config.from_path(path))

    assert study.get(url.split("/")) == exp


@pytest.mark.integration_test
@pytest.mark.parametrize(
    "url, exp",
    [
        ("output/1/about-the-study/study/antares/author", "Néo"),
        ("output/1/about-the-study/parameters/general/horizon", 42),
        ("output/1/info/general/mode", "Hello, world!"),
    ],
)
def test_save_output_it(
    project_path: Path, tmp_path: Path, url: str, exp: SUB_JSON
) -> None:
    path = extract_sta(project_path, tmp_path)
    study = Study(config=Config.from_path(path))

    study.save(exp, url.split("/"))
    assert study.get(url.split("/")) == exp
