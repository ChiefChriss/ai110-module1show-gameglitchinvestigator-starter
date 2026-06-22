# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  The game looked normal. It looked simple and easy to play. Two immediate bugs that I found were that it let you choose a number outside of the range and that the game did not reset properly. Another bug was that the hint was stuck at go lower.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 1 | Go higher (since secret was higher) | Go lower | Type mismatch: secret converted to string on even attempts |
| 150 (out of range) | number out of range | Go higher | Go higher! |
| New Game → Hard difficulty → New Game enter 150| Attempts reset to 5 says go lower or out of range| Attempts reset to 5, still says game over start a new game to try again| sgame over start a new game to try again |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used GitHub Copilot to help create test cases to find bugs in the game.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

**Correct suggestion.** When I asked Copilot to write pytest cases for the logic helpers, it suggested a test for `check_guess` (e.g. `check_guess(75, 50)` should be `"Too High"`) and a test asserting that out-of-range guesses get rejected. That second test failed, which correctly pointed to the missing bounds check I had also seen in the game when I typed 150 and it just said "Go higher!" The suggestion was correct. I verified it by adding the `if guess_int < low or guess_int > high` check in `app.py`, re-running the test until it passed, and then playing the game again — 150 now returns "Guess must be between 1 and 100."

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

**Incorrect / misleading suggestion.** For the hint that was stuck on "Go lower," Copilot suggested keeping a `try/except TypeError` block that converts the secret to a string and compares strings (this was actually in the AI-generated starter code). That was misleading because it hid the bug instead of fixing it — string comparison gives wrong answers, since `"100" > "20"` is `False`. I verified this was wrong by testing the comparison in a Python shell and by playing on an even-numbered attempt, where the hint was still backwards. The real fix was to stop converting the secret to a string at all and compare integers directly, plus correct the backwards directions in `HINT_MESSAGES`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
