from catalog import CATALOG

def parse_input(film_name: str) -> list[str]:
    return CATALOG.get(film_name, None)