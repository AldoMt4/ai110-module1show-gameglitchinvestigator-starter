import random
import streamlit as st

# FIX: Refactored all game logic functions into logic_utils.py using Claude Code
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# Messages shown to the player for each outcome
OUTCOME_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",   # FIX: was "Go HIGHER!" — hints were inverted
    "Too Low": "📈 Go HIGHER!",   # FIX: was "Go LOWER!" — hints were inverted
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: Changed initial attempts from 1 to 0 — starting at 1 meant the first
# real attempt was counted as attempt #2, inconsistent with new-game resets.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []  # each item: {"guess": int|str, "outcome": str}

st.subheader("Make a guess")

# FIX: Was hardcoded to "1 and 100" regardless of difficulty setting
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# CHALLENGE 4: Attempts progress bar
attempts_used = st.session_state.attempts
progress_fraction = attempts_used / attempt_limit
st.progress(progress_fraction, text=f"Attempts used: {attempts_used} / {attempt_limit}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({"guess": raw_guess, "outcome": "Error"})
        st.error(err)
    else:
        # FIX: Removed string/int type flip — on even attempts the secret was cast
        # to a string, making numeric comparison unreliable (e.g. "9" > "10" in
        # lexicographic order). Now always compare int to int.
        outcome = check_guess(guess_int, st.session_state.secret)
        st.session_state.history.append({"guess": guess_int, "outcome": outcome})
        message = OUTCOME_MESSAGES.get(outcome, "")

        # CHALLENGE 4: Temperature hint based on distance
        if show_hint and outcome != "Win":
            distance = abs(guess_int - st.session_state.secret)
            span = high - low
            if distance <= span * 0.05:
                temp = "🔥 Burning hot!"
            elif distance <= span * 0.15:
                temp = "♨️ Very warm!"
            elif distance <= span * 0.30:
                temp = "🌤️ Warm"
            elif distance <= span * 0.50:
                temp = "❄️ Cold"
            else:
                temp = "🧊 Freezing cold"
            st.warning(f"{message}  |  {temp}")
        elif show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# CHALLENGE 4: Colored guess history
if st.session_state.history:
    st.divider()
    st.subheader("Guess History")
    outcome_icons = {
        "Win": "✅",
        "Too High": "🔺 Too High",
        "Too Low": "🔻 Too Low",
        "Error": "⚠️ Invalid",
    }
    for i, entry in enumerate(st.session_state.history, 1):
        icon = outcome_icons.get(entry["outcome"], "❓")
        st.write(f"**#{i}** — `{entry['guess']}` → {icon}")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
