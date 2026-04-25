import pytest

from btf.models import BttfFilm, OtherFilm
from btf.parser import parse_input


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Back to the Future 1", BttfFilm(name="Back to the Future 1", volume=1)),
        ("Back to the Future 2", BttfFilm(name="Back to the Future 2", volume=2)),
        ("Back to the Future 3", BttfFilm(name="Back to the Future 3", volume=3)),
        ("La chèvre", OtherFilm(name="La chèvre")),
        ("Fast & Furious", OtherFilm(name="Fast & Furious")),
    ],
)
def test_parse_input_returns_catalog_film(name: str, expected) -> None:
    assert parse_input(name) == expected


@pytest.mark.parametrize(
    "name",
    ["Nonexistent Film", "", "back to the future 1", "BACK TO THE FUTURE 1"],
)
def test_parse_input_returns_none_for_unknown(name: str) -> None:
    assert parse_input(name) is None
