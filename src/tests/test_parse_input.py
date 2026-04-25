from models import BttfFilm, OtherFilm
from parser import parse_input

def test_parse_input1():
    assert parse_input("Back to the Future 1") == BttfFilm(name="Back to the Future 1", volume=1)
    
def test_parse_input2():
    assert parse_input("Back to the Future 2") == BttfFilm(name="Back to the Future 2", volume=2)
    
def test_parse_input3():
    assert parse_input("Back to the Future 3") == BttfFilm(name="Back to the Future 3", volume=3)

def test_parse_input4():
    assert parse_input("La chèvre") == OtherFilm(name="La chèvre")

def test_parse_input5():
    assert parse_input("Nonexistent Film") is None