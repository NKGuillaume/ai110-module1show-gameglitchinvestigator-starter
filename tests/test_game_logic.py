import pytest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("guess", "secret", "expected"),
    [
        (50, 50, ("Win", "🎉 Correct!")),
        (60, 50, ("Too High", "📉 Go LOWER!")),
        (40, 50, ("Too Low", "📈 Go HIGHER!")),
    ],
)
def test_check_guess_returns_expected_outcome_and_hint(guess, secret, expected):
    assert check_guess(guess, secret) == expected


def test_check_guess_regression_lower_guess_stays_too_low():
    """Regression: original code had the comparison reversed (> instead of <)."""
    outcome, message = check_guess(40, 50)

    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_guess_boundary_one_below():
    """Guess is exactly one below the secret — must be Too Low."""
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"


def test_check_guess_boundary_one_above():
    """Guess is exactly one above the secret — must be Too High."""
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"


def test_check_guess_secret_at_minimum():
    """Secret is the lowest possible value; any higher guess is Too High."""
    outcome, _ = check_guess(2, 1)
    assert outcome == "Too High"


def test_check_guess_secret_at_maximum():
    """Secret is the highest possible value; any lower guess is Too Low."""
    outcome, _ = check_guess(99, 100)
    assert outcome == "Too Low"


def test_check_guess_negative_secret():
    """Negative secrets should still compare correctly."""
    outcome, _ = check_guess(-10, -5)
    assert outcome == "Too Low"


def test_check_guess_zero():
    """Zero as both guess and secret counts as a win."""
    outcome, _ = check_guess(0, 0)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("raw", "expected_ok", "expected_value"),
    [
        ("42", True, 42),
        ("1", True, 1),
        ("100", True, 100),
        ("3.7", True, 3),      # float string truncates to int
        ("3.0", True, 3),      # exact float still parses
        ("-5", True, -5),      # negative number is valid
    ],
)
def test_parse_guess_valid_inputs(raw, expected_ok, expected_value):
    ok, value, err = parse_guess(raw)
    assert ok is True
    assert value == expected_value
    assert err is None


@pytest.mark.parametrize(
    "raw",
    ["", None, "abc", "12abc", " ", "!@#"],
)
def test_parse_guess_invalid_inputs_return_false(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert err is not None and len(err) > 0


def test_parse_guess_none_gives_enter_a_guess():
    _, _, err = parse_guess(None)
    assert "guess" in err.lower()


def test_parse_guess_empty_string_gives_enter_a_guess():
    _, _, err = parse_guess("")
    assert "guess" in err.lower()


def test_parse_guess_non_numeric_gives_not_a_number():
    _, _, err = parse_guess("hello")
    assert "number" in err.lower()


def test_parse_guess_large_number():
    """Very large numbers should still parse correctly."""
    ok, value, _ = parse_guess("999999")
    assert ok is True
    assert value == 999999


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("difficulty", "expected_low", "expected_high"),
    [
        ("Easy", 1, 50),
        ("Normal", 1, 100),
        ("Hard", 1, 120),
    ],
)
def test_get_range_for_difficulty_known_levels(difficulty, expected_low, expected_high):
    low, high = get_range_for_difficulty(difficulty)
    assert low == expected_low
    assert high == expected_high


def test_get_range_for_difficulty_unknown_defaults_to_normal():
    """Any unknown difficulty string should fall back to the Normal range."""
    low, high = get_range_for_difficulty("Legendary")
    assert (low, high) == (1, 100)


def test_get_range_for_difficulty_case_sensitive():
    """Difficulty matching is case-sensitive; 'easy' != 'Easy' → falls back."""
    low, high = get_range_for_difficulty("easy")
    assert (low, high) == (1, 100)


def test_get_range_low_always_less_than_high():
    for diff in ("Easy", "Normal", "Hard", "Unknown"):
        low, high = get_range_for_difficulty(diff)
        assert low < high


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_update_score_win_early_attempt():
    """Win on attempt 1 should award maximum points (capped floor at 10)."""
    new_score = update_score(0, "Win", 1)
    assert new_score == 80  # 100 - 10*(1+1) = 80


def test_update_score_win_points_floor_at_ten():
    """Points should never drop below 10 even at a very high attempt count."""
    new_score = update_score(0, "Win", 100)
    assert new_score == 10


def test_update_score_win_accumulates_on_existing_score():
    new_score = update_score(50, "Win", 1)
    assert new_score == 130  # 50 + 80


def test_update_score_too_high_even_attempt_gives_bonus():
    """Even-numbered attempts with Too High award +5."""
    new_score = update_score(100, "Too High", 2)
    assert new_score == 105


def test_update_score_too_high_odd_attempt_deducts():
    """Odd-numbered attempts with Too High deduct 5."""
    new_score = update_score(100, "Too High", 3)
    assert new_score == 95


def test_update_score_too_low_always_deducts():
    new_score = update_score(100, "Too Low", 1)
    assert new_score == 95


def test_update_score_unknown_outcome_no_change():
    """Unrecognised outcome strings should leave score unchanged."""
    new_score = update_score(42, "Draw", 5)
    assert new_score == 42


def test_update_score_can_go_negative():
    """Score is allowed to go below zero (no artificial floor)."""
    new_score = update_score(0, "Too Low", 1)
    assert new_score == -5
