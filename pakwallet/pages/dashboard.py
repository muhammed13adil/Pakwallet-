"""Dashboard page."""

from __future__ import annotations

import streamlit as st
from sqlalchemy.orm import Session


def render_dashboard(session: Session, user_id: int) -> None:
    """Render dashboard page."""
    st.title("Wallet Dashboard")
    st.write(f"Welcome! You are viewing the dashboard for user {user_id}.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Balance", "PKR 50,000")
    with col2:
        st.metric("Income", "PKR 100,000")
    with col3:
        st.metric("Expenses", "PKR 30,000")
    with col4:
        st.metric("Savings", "PKR 20,000")
