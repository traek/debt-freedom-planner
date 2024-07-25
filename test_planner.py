import pytest
from datetime import datetime
from planner import format_money, format_percentage, calculate_payoff, add_months, format_month_year

def test_format_money():
    assert format_money(0.0) == "$0.00"
    assert format_money(0) == "$0.00"
    assert format_money(-100) == "-$100.00"
    assert format_money(123.45) == "$123.45"
    assert format_money(12345.67890) == "$12,345.68"
    assert format_money(-12345.67890) == "-$12,345.68"

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

def test_format_month_year():
    assert format_month_year(datetime(2000, 4, 1)) == "Apr 2000"
    assert format_month_year(datetime(2000, 7, 7)) == "Jul 2000"
    assert format_month_year(datetime(1830, 4, 6)) == "Apr 1830"
    assert format_month_year(datetime(1978, 11, 1))== "Nov 1978"
    assert format_month_year(datetime(2025, 4, 6)) == "Apr 2025"

def test_calculate_payoff():
    assert calculate_payoff(2000, 0.05, 171.21, datetime(2024, 1, 1)) == datetime(2025, 1, 1)
    assert calculate_payoff(2000, 0.05, 171.21, datetime(2000, 1, 1)) == datetime(2001, 1, 1)
    assert calculate_payoff(10000, 0.1, 212.47, datetime(2024, 7, 25))== datetime(2029, 7, 25)
    assert calculate_payoff(10000, 0.1, 171.76, datetime(2024, 7, 25))== datetime(2031, 3, 25)

def test_add_months():
    assert add_months(datetime(2024, 1, 1), 12) == datetime(2025, 1, 1)
    assert add_months(datetime(2024, 1, 1), 1)  == datetime(2024, 2, 1)
    assert add_months(datetime(2000, 7, 7), 9)  == datetime(2001, 4, 7)
    assert add_months(datetime(1978, 11, 1), 46*12) == datetime(2024, 11, 1)

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])