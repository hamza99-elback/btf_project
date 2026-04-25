import pytest

from btf.models import Film
from btf.parser import parse_input
from btf.pricing import get_bttf_reduction_rate


def _bttf(*names: str) -> list[Film]:
    films = [parse_input(n) for n in names]
    assert all(f is not None for f in films)
    return films  # type: ignore[return-value]


@pytest.mark.parametrize(
    ("films", "expected_rate"),
    [
        # No BTTF films at all -> no discount.
        ([], 0.0),
        # Single distinct volume (any number of copies) -> no discount.
        (_bttf("Back to the Future 1"), 0.0),
        (_bttf("Back to the Future 1", "Back to the Future 1"), 0.0),
        # Two distinct volumes -> 10% discount.
        (_bttf("Back to the Future 1", "Back to the Future 2"), 0.10),
        (_bttf("Back to the Future 1", "Back to the Future 3"), 0.10),
        # Three distinct volumes -> 20% discount.
        (
            _bttf(
                "Back to the Future 1",
                "Back to the Future 2",
                "Back to the Future 3",
            ),
            0.20,
        ),
        # Duplicates do not increase the distinct count.
        (
            _bttf(
                "Back to the Future 1",
                "Back to the Future 2",
                "Back to the Future 2",
            ),
            0.10,
        ),
    ],
)
def test_reduction_rate(films: list[Film], expected_rate: float) -> None:
    assert get_bttf_reduction_rate(films) == pytest.approx(expected_rate)


def test_reduction_rate_ignores_other_films() -> None:
    """Non-BTTF films must not influence the BTTF reduction rate."""
    films = _bttf("Back to the Future 1") + [parse_input("La chèvre")]  # type: ignore[list-item]
    assert get_bttf_reduction_rate(films) == 0.0
