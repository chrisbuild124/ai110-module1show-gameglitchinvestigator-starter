import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# --- get_range_for_difficulty ---

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 100)


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_valid_float_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None


# --- check_guess ---

def test_check_guess_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_check_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- update_score ---

def test_update_score_win_early():
    # attempt 1: points = 100 - 10*(1+1) = 80
    assert update_score(0, "Win", 1) == 80

def test_update_score_win_minimum_points():
    # attempt 10: points = 100 - 10*(10+1) = -10 → clamped to 10
    assert update_score(0, "Win", 10) == 10

def test_update_score_wrong_deducts():
    assert update_score(20, "Too High", 1) == 15
    assert update_score(20, "Too Low", 1) == 15

def test_update_score_floor_at_zero():
    # Score should never go below 0
    assert update_score(0, "Too Low", 1) == 0
    assert update_score(3, "Too High", 1) == 0
