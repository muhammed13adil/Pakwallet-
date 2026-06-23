"""Analytics page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy.orm import Session


def render_analytics(session: Session, user_id: int) -> None:
    """Render analytics page."""
    st.title("Analytics")
    st.write(f"View your financial analytics. User ID: {user_id}")
    
    tab1, tab2, tab3 = st.tabs(["Monthly Report", "Expense Breakdown", "Savings Trend"])
    
    with tab1:
        st.subheader("Monthly Report")
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Income": [100000, 105000, 102000, 110000, 108000, 112000],
            "Expenses": [70000, 72000, 68000, 75000, 71000, 73000],
        }
        df = pd.DataFrame(data)
        fig = px.line(df, x="Month", y=["Income", "Expenses"], title="Income vs Expenses")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Expense Breakdown")
        expense_data = {
            "Category": ["Housing", "Food", "Entertainment", "Utilities", "Transport"],
            "Amount": [25000, 15000, 8000, 5000, 10000],
        }
        df_expense = pd.DataFrame(expense_data)
        fig_pie = px.pie(df_expense, values="Amount", names="Category", title="Expense Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab3:
        st.subheader("Savings Trend")
        savings_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Savings": [30000, 33000, 34000, 35000, 37000, 39000],
        }
        df_savings = pd.DataFrame(savings_data)
        fig_savings = px.bar(df_savings, x="Month", y="Savings", title="Monthly Savings")
        st.plotly_chart(fig_savings, use_container_width=True)
