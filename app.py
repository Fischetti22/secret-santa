"""Streamlit interface for the family Secret Santa draw."""

from __future__ import annotations

import hmac
import os

import streamlit as st

from secret_santa import PARTICIPANTS, STATE_FILE, create_assignments, load_state, save_state

st.set_page_config(page_title="Secret Santa", page_icon="🎁", layout="centered")


def reset_draw() -> None:
    """Start a new draw after organizer confirmation."""
    save_state({"assignments": create_assignments(), "revealed": []})
    st.success("A new Secret Santa draw is ready.")


st.title("🎁 Secret Santa")
st.write("Choose your name, then reveal the person you are buying a gift for.")

state = load_state()
assignments = state["assignments"]
revealed = set(state["revealed"])
available = [name for name in PARTICIPANTS if name not in revealed]

if available:
    selected_name = st.selectbox("Your name", available, index=None, placeholder="Choose your name")
    reveal = st.button("Reveal my Secret Santa", type="primary", disabled=selected_name is None)

    if reveal and selected_name:
        recipient = assignments[selected_name]
        state["revealed"] = [*revealed, selected_name]
        save_state(state)
        st.balloons()
        st.success(f"Your Secret Santa is: **{recipient}**")
        st.info("Please keep this secret and close this page when you are done.")
else:
    st.success("Everyone has received their Secret Santa!")

with st.expander("Organizer controls"):
    organizer_password = os.environ.get("ORGANIZER_PASSWORD")
    if organizer_password:
        entered_password = st.text_input("Organizer password", type="password")
        if st.button("Start a new draw"):
            if hmac.compare_digest(entered_password, organizer_password):
                reset_draw()
            else:
                st.error("Incorrect organizer password.")
    else:
        st.caption(
            "Set an `ORGANIZER_PASSWORD` Streamlit secret to enable the reset button."
        )
        if STATE_FILE.exists():
            st.caption("For local use, delete `assignments.json` to start a new draw.")
