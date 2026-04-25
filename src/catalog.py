from models import BttfFilm, Film, OtherFilm

CATALOG: dict[str, Film] = {
    "Back to the Future 1": BttfFilm(name="Back to the Future 1", volume=1),
    "Back to the Future 2": BttfFilm(name="Back to the Future 2", volume=2),
    "Back to the Future 3": BttfFilm(name="Back to the Future 3", volume=3),
    "La chèvre": OtherFilm(name="La chèvre"),
    "Fast & Furious": OtherFilm(name="Fast & Furious"),
}