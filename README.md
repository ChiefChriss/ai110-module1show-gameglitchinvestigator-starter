# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** Glitchy Guesser is a Streamlit number-guessing
  game. The app picks a secret number within a range that depends on the chosen
  difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player tries to find it
  within a limited number of attempts. After each guess the game gives a "Too High" /
  "Too Low" hint, updates the score, and ends on a win or when attempts run out.

- [x] **Detail which bugs you found.**
  - **Secret number reset on every Submit (state bug).** The secret was re-rolled with
    `random.randint(...)` on each rerun, so it changed every time you clicked Submit and
    the game was unwinnable.
  - **Backwards / stuck hints.** The secret was converted to a string on even attempts,
    causing a type mismatch (`"100" > "20"` is `False`); the hint got stuck telling you
    to "Go LOWER" even when the guess was too low.
  - **Out-of-range guesses accepted.** Typing `150` returned "Too High" instead of being
    rejected as outside the valid range.
  - **New Game didn't fully reset.** Resetting only touched attempts/secret, so a finished
    game stayed "won"/"lost" and used a hardcoded `randint(1, 100)` instead of the
    difficulty's range.

- [x] **Explain what fixes you applied.**
  - Initialized `secret` in `st.session_state` (guarded by `if "secret" not in
    st.session_state`) so it stays fixed across reruns.
  - Rewrote `check_guess` to compare integers directly and dropped the misleading
    `try/except` string fallback; corrected the directions in `HINT_MESSAGES`.
  - Added a bounds check against the difficulty's `[low, high]` range before scoring.
  - Made "New Game" clear every piece of state and use the current range.
  - Refactored the game logic into `logic_utils.py` and covered it with `pytest`.

## 📸 Demo Walkthrough

A step-by-step run through a sample game (secret number = 63):

1. User enters a guess of 40 → game returns "Too Low".
2. User enters a guess of 70 → game returns "Too High".
3. User enters a guess of 55 → game returns "Too Low". The score updates correctly after each guess (e.g., guess count increments to 3).
4. User enters a guess of 63 → game returns "Correct!" and displays the final score.
5. The game ends after the correct guess, and the secret number stays fixed throughout the session (no resetting on each Submit).

## 🧪 Test Results

```
$ python -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/bhristo/Downloads/a110/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.14.0
collected 3 items

tests/test_game_logic.py ...                                             [100%]

============================== 3 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
