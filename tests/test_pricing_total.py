"""End-to-end pricing scenarios.

The discount semantics under test are the ones declared in the assignment spec:
the reduction rate is determined by the count of *distinct* BTTF volumes in the
cart, then applied to the entire BTTF subtotal. See `btf.pricing` for details.
"""
from __future__ import annotations

import pytest

from btf.models import Film
from btf.parser import parse_input
from btf.pricing import get_total_price


def _cart(*names: str) -> list[Film]:
    films = [parse_input(n) for n in names]
    assert all(f is not None for f in films), "unknown film in test fixture"
    return films  # type: ignore[return-value]


@pytest.mark.parametrize(
    ("cart", "expected_total"),
    [
        # ---- empty cart ----
        ([], 0.0),

        # ---- single film ----
        (_cart("Back to the Future 1"), 15.0),                      # 1 × 15
        (_cart("La chèvre"), 20.0),                                 # 1 × 20

        # ---- only "other" films (never discounted) ----
        (_cart("La chèvre", "Fast & Furious"), 40.0),               # 2 × 20

        # ---- BTTF, two distinct volumes -> 10% off ----
        (_cart("Back to the Future 1", "Back to the Future 3"),
         pytest.approx(27.0)),                                      # 2 × 15 × 0.9

        # ---- BTTF, three distinct volumes -> 20% off ----
        (_cart("Back to the Future 1",
               "Back to the Future 2",
               "Back to the Future 3"),
         pytest.approx(36.0)),                                      # 3 × 15 × 0.8

        # ---- BTTF with duplicate volume (spec: discount on whole subtotal) ----
        (_cart("Back to the Future 1",
               "Back to the Future 2",
               "Back to the Future 3",
               "Back to the Future 2"),
         pytest.approx(48.0)),                                      # 4 × 15 × 0.8

        # ---- mixed BTTF + other ----
        (_cart("Back to the Future 1",
               "Back to the Future 2",
               "Back to the Future 3",
               "La chèvre"),
         pytest.approx(56.0)),                                      # 36 + 20

        # ---- duplicates only of one volume -> no discount ----
        (_cart("Back to the Future 1", "Back to the Future 1"), 30.0),
    ],
)
def test_total_price_scenarios(cart: list[Film], expected_total: float) -> None:
    assert get_total_price(cart) == expected_total
