from parser import parse_input
from pricing import get_total_price

def test_example_1():
    result = get_total_price([
        parse_input("Back to the Future 1"),
        parse_input("Back to the Future 2"),
        parse_input("Back to the Future 3"),
    ])
    assert result == 36.0

def test_example_2():
    result = get_total_price([
        parse_input("Back to the Future 1"),
        parse_input("Back to the Future 3"),
    ])
    assert result == 27.0

def test_example_3():
    result = get_total_price([
        parse_input("Back to the Future 1"),
    ])
    assert result == 15.0

def test_example_4():
    result = get_total_price([
        parse_input("Back to the Future 1"),
        parse_input("Back to the Future 2"),
        parse_input("Back to the Future 3"),
        parse_input("Back to the Future 2"),
    ])
    assert result == 48.0

def test_example_5():
    result = get_total_price([
        parse_input("Back to the Future 1"),
        parse_input("Back to the Future 2"),
        parse_input("Back to the Future 3"),
        parse_input("La chèvre")
    ])
    assert result == 56.0