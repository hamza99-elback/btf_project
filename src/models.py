from dataclasses import dataclass, field
from abc import ABC

@dataclass
class Film(ABC):
    name: str
    price: float
    film_type: str

@dataclass
class BttfFilm(Film):
    price: float = 15.0
    film_type: str = "bttf"
    volume: int = field(default=0)

@dataclass
class OtherFilm(Film):
    price: float = 20.0
    film_type: str = "other"