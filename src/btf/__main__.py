"""CLI demo: prints totals for a few preset scenarios."""

from .parser import parse_input
from .pricing import get_total_price


def main() -> None:
    film1 = parse_input("Back to the Future 1")
    film2 = parse_input("Back to the Future 2")
    film3 = parse_input("Back to the Future 3")
    other_film1 = parse_input("La chèvre")

    scenarios = {
        "Scenario 1 [v1, v2, v3]":         [film1, film2, film3],
        "Scenario 2 [v1, v3]":             [film1, film3],
        "Scenario 3 [v1]":                 [film1],
        "Scenario 4 [v1, v2, v3, v2]":     [film1, film2, film3, film2],
        "Scenario 5 [v1, v2, v3, other]":  [film1, film2, film3, other_film1],
    }

    for label, cart in scenarios.items():
        print(f"{label}: {get_total_price(cart):.2f} €")


if __name__ == "__main__":
    main()
