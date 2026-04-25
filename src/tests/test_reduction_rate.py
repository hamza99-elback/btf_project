from parser import parse_input


def test_reduction_rate1():
    from pricing import get_bttf_reduction_rate

    reduction_rate = get_bttf_reduction_rate(
        [
            parse_input("Back to the Future 1"),
            parse_input("Back to the Future 2"),
            parse_input("Back to the Future 3"),
        ]
    )
    assert reduction_rate == 0.2


def test_reduction_rate2():
    from pricing import get_bttf_reduction_rate

    reduction_rate = get_bttf_reduction_rate(
        [
            parse_input("Back to the Future 1"),
            parse_input("Back to the Future 3"),
        ]
    )
    assert reduction_rate == 0.1


def test_reduction_rate3():
    from pricing import get_bttf_reduction_rate

    reduction_rate = get_bttf_reduction_rate(
        [
            parse_input("Back to the Future 1"),
        ]
    )
    assert reduction_rate == 0.0
