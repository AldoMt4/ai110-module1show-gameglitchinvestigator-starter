# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Purpose:** A number guessing game where the player tries to guess a secret number within a limited number of attempts. The difficulty setting changes the number range (Easy: 1–20, Normal: 1–100, Hard: 1–200).
- [x] **Bugs found:**
  - Inverted hints — "Too High" showed "Go HIGHER!" and vice versa
  - Secret number was cast to a string on even attempts, breaking numeric comparison
  - Hard difficulty range (1–50) was easier than Normal (1–100)
  - Initial attempt counter started at 1 instead of 0
  - Info banner hardcoded "1 and 100" regardless of difficulty
- [x] **Fixes applied:**
  - Corrected hint direction in `check_guess`
  - Removed the string/int type flip from `app.py`
  - Changed Hard range to 1–200
  - Moved all logic functions from `app.py` into `logic_utils.py`
  - Fixed initial attempts and dynamic range display

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
