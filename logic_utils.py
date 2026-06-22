# FIX: Pulled the hint text into one mapping (Copilot's suggestion) and corrected the
# directions — the AI-generated original told you to "Go HIGHER" when the guess was
# already too high. I verified the new mapping by playing the game in both directions.
# Hint message shown in the UI for each outcome of check_guess().
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    Returns one of: "Win", "Too High", "Too Low".
    Use HINT_MESSAGES[outcome] to get the player-facing hint.
    """
    # FIX: Rewrote this to return just the outcome string and compare ints directly.
    # I dropped the AI's try/except TypeError fallback that compared strings, since
    # that masked the real bug instead of fixing it.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: A wrong guess always costs the same. The old "Too High" branch awarded
    # +5 on even attempts (attempt_number % 2 == 0), letting players farm points by
    # repeatedly guessing too high — and it was asymmetric with "Too Low".
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
