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

 When I asked Copilot to write pytest cases for the logic helpers, it suggested a test for `check_guess` (e.g. `check_guess(75, 50)` should be `"Too High"`) and a test asserting that out-of-range guesses get rejected. That second test failed, which correctly pointed to the missing bounds check I had also seen in the game when I typed 150 and it just said "Go higher!" The suggestion was correct. I verified it by adding the `if guess_int < low or guess_int > high` check in `app.py`, re-running the test until it passed, and then playing the game again — 150 now returns "Guess must be between 1 and 100."

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

For the hint that was stuck on "Go lower," Copilot suggested keeping a `try/except TypeError` block that converts the secret to a string and compares strings (this was actually in the AI-generated starter code). That was misleading because it hid the bug instead of fixing it — string comparison gives wrong answers, since `"100" > "20"` is `False`. I verified this was wrong by testing the comparison in a Python shell and by playing on an even-numbered attempt, where the hint was still backwards. The real fix was to stop converting the secret to a string at all and compare integers directly, plus correct the backwards directions in `HINT_MESSAGES`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed when it passed in two places: a green pytest run *and* the actual game when I replayed it. I didn't trust one without the other, because the hint bug taught me that code can "look" handled (the try/except) while still being wrong. For pytest, I ran `test_guess_too_high`, where `check_guess(60, 50)` has to return `"Too High"` — it failed while the secret was still being compared as a string, and passed once I rewrote `check_guess` to compare ints directly, which confirmed the comparison logic was the real problem and not the UI. AI helped me design the tests: I asked Copilot to write pytest cases for the logic helpers, and it gave me the win/too-high/too-low cases plus the out-of-range case that exposed the missing bounds check. It also helped me *understand* the tests — I had it explain why string comparison made `"100" > "20"` come out `False`, which is what made me realize the fix was to stop converting the secret to a string at all.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I'd tell my friend that Streamlit re-runs the entire script from top to bottom every single time you click a button, type in a box, or change a setting — it doesn't just update the one thing you touched. That means any normal variable gets reset to its starting value on every interaction, which is why a guessing game can't just use a plain counter for attempts. `st.session_state` is the fix: it's a little box that survives the reruns, so the secret number, the attempt count, and the score stick around between clicks. This finally explained the broken "New Game" bug to me — resetting `attempts` and `secret` wasn't enough because the old `status` ("won"/"lost") was still living in session state, so the game thought it was still over. Once I understood that reruns wipe everything *except* session state, I knew the reset had to clear every key in session state, not just a couple of them.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is writing a quick pytest case for any logic that has a clear right answer before I call a bug "fixed," instead of just eyeballing the game. Having a failing test first and a passing test after gave me real proof, and the out-of-range test caught a bug I might have missed by only playing. One thing I'd do differently is read the AI's code more skeptically up front — the try/except string-comparison block looked like a real fix and ran without errors, so I almost kept it; next time I'll ask the AI to explain why its code works before I accept it rather than trusting that "no error" means "correct." This project changed how I think about AI-generated code: I now treat it as a fast but overconfident first draft that can be confidently wrong (it literally called this code "production-ready"), so I review and test every suggestion instead of assuming it's right just because the AI wrote it.
