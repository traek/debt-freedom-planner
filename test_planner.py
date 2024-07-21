import pytest
from planner import format_money, format_percentage

def test_format_money():
    assert format_money(0.0) == "$0.00"
    assert format_money(0) == "$0.00"
    assert format_money(-100) == "-$100.00"
    assert format_money(123.45) == "$123.45"
    assert format_money(12345.67890) == "$12345.68"
    assert format_money(-12345.67890) == "-$12345.68"

def test_format_percentage():
    assert format_percentage(0.0) == "0.00%"
    assert format_percentage(0) == "0.00%"
    assert format_percentage(0.05, 0) == "5%"
    assert format_percentage(0.18125, 0) == "18%"
    assert format_percentage(0.18125, 3) == "18.125%"
    assert format_percentage(-0.757575, 4) == "-75.7575%"
    assert format_percentage(-0.757575, -1) == "-75.7575%"
    assert format_percentage(1/3) == "33.33%"
    assert format_percentage(-2/3) == "-66.67%"
    assert format_percentage(-2/3, -1) == "-66.6667%"
    assert format_percentage(1) == "100.00%"
    assert format_percentage(5.5) == "550.00%"


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])