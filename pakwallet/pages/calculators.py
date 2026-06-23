"""Calculators page."""

from __future__ import annotations

import streamlit as st


def render_calculators() -> None:
    """Render calculators page."""
    st.title("Financial Calculators")
    
    calculator = st.selectbox(
        "Choose a calculator",
        ["Mutual Funds", "Home Loan", "Car Financing", "Child Education", "Zakat", "Freelancer Tax"],
    )
    
    if calculator == "Mutual Funds":
        st.subheader("Mutual Fund Calculator")
        principal = st.number_input("Principal Amount (PKR)", value=10000)
        rate = st.number_input("Annual Return (%)", value=12.0)
        years = st.number_input("Years", value=10)
        amount = principal * ((1 + rate / 100) ** years)
        st.success(f"Future Value: PKR {amount:,.2f}")
