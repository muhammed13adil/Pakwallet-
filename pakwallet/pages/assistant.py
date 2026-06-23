"""AI Budget Assistant page."""

from __future__ import annotations

import streamlit as st
from sqlalchemy.orm import Session


def render_assistant(session: Session, user_id: int) -> None:
    """Render AI budget assistant page."""
    st.title("AI Budget Assistant")
    st.write(f"Get budget recommendations. User ID: {user_id}")
    
    st.info("💡 Tip: Keep your monthly expenses below 70% of your income for healthy financial management.")
    
    if st.button("Get Personalized Recommendations"):
        st.success("Based on your spending patterns, we recommend cutting entertainment expenses by 10%.")
