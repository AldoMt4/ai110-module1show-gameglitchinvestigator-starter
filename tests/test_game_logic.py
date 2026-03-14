from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- Tests targeting specific bugs that were fixed ---

def test_hints_not_inverted():
    # BUG FIX: Original code returned "Too High" when guess < secret and vice versa.
    # Verify that a guess of 1 against a secret of 100 is "Too Low" (not "Too High").
    assert check_guess(1, 100) == "Too Low"
    # And a guess of 100 against a secret of 1 is "Too High" (not "Too Low").
    assert check_guess(100, 1) == "Too High"

def test_check_guess_boundary_one_below():
    # Guess is exactly one below the secret — should be Too Low
    assert check_guess(49, 50) == "Too Low"

def test_check_guess_boundary_one_above():
    # Guess is exactly one above the secret — should be Too High
    assert check_guess(51, 50) == "Too High"

def test_parse_guess_valid_integer():
    ok, value, _ = parse_guess("42")
    assert ok is True
    assert value == 42

def test_parse_guess_decimal_truncates():
    # Decimals should be accepted and truncated to int
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_guess_empty_string():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric():
    ok, value, _ = parse_guess("abc")
    assert ok is False
    assert value is None

def test_hard_difficulty_range_harder_than_normal():
    # BUG FIX: Hard was returning (1, 50), which is easier than Normal (1, 100).
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high
