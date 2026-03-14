# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, the game was unplayable in several ways. The most obvious bug was that the hints were completely backwards — if I guessed a number higher than the secret, the game said "Go HIGHER!" instead of "Go LOWER!". The secret number also behaved strangely because on every even-numbered attempt, the app was secretly converting the secret number to a string before comparing, which caused wrong results. Additionally, the Hard difficulty range was set to 1–50, making it actually easier than Normal (1–100), and the info banner always said "between 1 and 100" regardless of which difficulty was selected.

---

## 2. How did you use AI as a teammate?

I used Claude Code (an AI coding assistant) to help me investigate and repair the bugs in this project. One correct suggestion was identifying the inverted hints bug in `check_guess`: the AI correctly spotted that `guess > secret` was returning "Go HIGHER!" when it should return "Go LOWER!", and suggested flipping the messages. I verified this by running the fixed app and testing guesses both above and below the secret number. One misleading aspect was that the AI initially could have left the `update_score` function's odd scoring logic (giving +5 for "Too High" on even attempts) as-is, since it looked like a bug but was part of the original code. I verified by reading the function carefully and decided it was intentional weirdness in the starter code, not something introduced by the fix.

---

## 3. Debugging and testing your fixes

I verified each fix using a combination of pytest and manual testing in the live Streamlit app. For the inverted hints fix, I ran `pytest tests/` and confirmed `test_guess_too_high` and `test_hints_not_inverted` both passed — these tests specifically check that guessing 60 against a secret of 50 returns "Too High" (not "Too Low"). I also loaded the app in the browser, opened the Developer Debug Info panel to see the secret, then deliberately guessed above and below it to confirm the hints now pointed in the correct direction. The AI helped me design boundary tests (one above, one below the secret) to catch edge cases that a simple test might miss.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept changing because Streamlit reruns the entire Python script from top to bottom every time the user interacts with the page — clicking a button, changing a dropdown, anything. Without `st.session_state`, `random.randint()` was called on every rerun, generating a new secret each time. I fixed this by checking `if "secret" not in st.session_state` before generating the number, so it only runs once. To a friend: imagine Streamlit is like refreshing a webpage — everything resets unless you store data in a special "memory box" called `session_state` that survives the refresh.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is writing targeted tests immediately after fixing a bug — not just to confirm the fix works, but to lock in the correct behavior so it can't silently break again later. Next time I work with AI on a coding task, I would review the AI's output more carefully before accepting it, especially for logic that involves comparisons or ordering, since those are easy to invert. This project changed how I think about AI-generated code: it can write syntactically correct code that is logically wrong in subtle ways, so I need to run it, test it, and read it critically rather than assuming it works just because it looks right.
