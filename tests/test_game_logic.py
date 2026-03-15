import pytest

from logic_utils import check_guess


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
    outcome, message = check_guess(40, 50)

    assert outcome == "Too Low"
    assert "HIGHER" in message
