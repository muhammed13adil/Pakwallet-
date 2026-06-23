"""Savings goals page."""

from __future__ import annotations

import streamlit as st
from sqlalchemy.orm import Session


def render_savings(session: Session, user_id: int) -> None:
    """Render savings goals page."""
    st.title("Savings Goals")
    st.write(f"Manage your savings goals. User ID: {user_id}")
    
    tab1, tab2 = st.tabs(["View Goals", "Add Goal"])
    
    with tab1:
        st.info("No savings goals yet.")
    
    with tab2:
        st.subheader("Create a New Goal")
        goal_name = st.text_input("Goal Name")
        target_amount = st.number_input("Target Amount (PKR)")
        if st.button("Save Goal"):
            st.success("Goal created successfully!")
