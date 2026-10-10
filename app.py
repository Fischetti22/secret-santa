"""Streamlit interface for the family Secret Santa draw."""

from __future__ import annotations

import hmac
import os

import streamlit as st

from secret_santa import PARTICIPANTS, STATE_FILE, create_assignments, load_state, save_state

st.set_page_config(page_title="Secret Santa", page_icon="🎁", layout="centered")


def reset_draw() -> None:
    """Start a new draw after organizer confirmation."""
    save_state({"assignments": create_assignments(), "revealed": [], "wishlists": {}})
    st.success("A new Secret Santa draw is ready.")


st.title("🎁 Secret Santa")
st.caption("Gift budget: please keep gifts at **$65 or less**.")

state = load_state()
assignments = state["assignments"]
revealed = set(state["revealed"])
available = [name for name in PARTICIPANTS if name not in revealed]
wishlists = state["wishlists"]

draw_tab, wishlist_tab = st.tabs(["Draw a name", "Add Wishlist"])

with draw_tab:
    st.write("Choose your name, then reveal the person you are buying a gift for.")
    if available:
        selected_name = st.selectbox(
            "Your name", available, index=None, placeholder="Choose your name"
        )
        reveal = st.button(
            "Reveal my Secret Santa", type="primary", disabled=selected_name is None
        )

        if reveal and selected_name:
            recipient = assignments[selected_name]
            state["revealed"] = [*revealed, selected_name]
            save_state(state)
            st.balloons()
            st.success(f"Your Secret Santa is: **{recipient}**")
            st.info("Please keep this secret and close this page when you are done.")

            recipient_wishlist = wishlists.get(recipient, [])
            if recipient_wishlist:
                st.subheader(f"{recipient}'s wishlist")
                for item in recipient_wishlist:
                    st.write(f"- {item}")
            else:
                st.caption(f"{recipient} has not added a wishlist yet.")
    else:
        st.success("Everyone has received their Secret Santa!")

with wishlist_tab:
    st.write("Add as many gift ideas as you like. Please keep each idea at **$65 or less**.")
    wishlist_name = st.selectbox(
        "Your name",
        PARTICIPANTS,
        index=None,
        placeholder="Choose your name",
        key="wishlist_name",
    )
    item_description = st.text_area(
        "Item description",
        placeholder="Example: Cozy blanket, blue, available at Target",
        max_chars=300,
    )
    if st.button(
        "Add item to wishlist",
        disabled=wishlist_name is None or not item_description.strip(),
    ):
        wishlists.setdefault(wishlist_name, []).append(item_description.strip())
        state["wishlists"] = wishlists
        save_state(state)
        st.success("Wishlist item added.")

    if wishlist_name and wishlists.get(wishlist_name):
        st.subheader(f"{wishlist_name}'s saved items")
        for item in wishlists[wishlist_name]:
            st.write(f"- {item}")

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
