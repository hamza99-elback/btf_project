from .catalog import CATALOG
from .models import Film


def parse_input(film_name: str) -> Film | None:
    """Look up a film by name in the catalog. Returns None if unknown."""
    return CATALOG.get(film_name, None)
