"""Bills page."""

from __future__ import annotations

import streamlit as st
from sqlalchemy.orm import Session


def render_bills(session: Session, user_id: int) -> None:
    """Render bills page."""
    st.title("Bill Payments")
    st.write(f"Manage your bill payments. User ID: {user_id}")
    
    tab1, tab2 = st.tabs(["View Bills", "Pay Bill"])
    
    with tab1:
        st.info("No bills available.")
    
    with tab2:
        st.subheader("Pay a Bill")
        provider = st.selectbox("Provider", ["Electricity", "Gas", "Internet", "School Fees"])
        amount = st.number_input("Amount (PKR)")
        if st.button("Pay Now"):
            st.success(f"Payment of PKR {amount} processed!")
