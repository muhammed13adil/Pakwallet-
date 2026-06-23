"""Analytics page for PakWallet."""

import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from pakwallet.services.database import Transaction
from pakwallet.utils.formatting import format_pkr
from pakwallet.utils.analytics import generate_monthly_trend_chart, generate_net_worth_trend

def render_analytics(session: Session, user_id: int) -> None:
    """Render transaction trends and monthly reporting sheets."""
    st.title("Financial Analytics")
    st.write("Understand your long-term wealth progression and cash flow trends.")
    
    # Fetch transactions
    transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    if not transactions:
        st.info("You need to add some transaction records on the Dashboard to generate analytics charts.")
        return
        
    # Stats summary
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    net_savings = total_income - total_expense
    savings_rate = ((total_income - total_expense) / total_income) * 100 if total_income > 0 else 0.0
    
    # Simple summary row
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1.5rem; border: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.85rem; opacity: 0.7; text-transform: uppercase;">Cumulative Income</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #2ecc71;">{format_pkr(total_income)}</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;">
                    <div style="font-size: 0.85rem; opacity: 0.7; text-transform: uppercase;">Cumulative Expenses</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #e74c3c;">{format_pkr(total_expense)}</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;">
                    <div style="font-size: 0.85rem; opacity: 0.7; text-transform: uppercase;">Net Saved</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--pak-gold);">{format_pkr(net_savings)}</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;">
                    <div style="font-size: 0.85rem; opacity: 0.7; text-transform: uppercase;">Lifetime Savings Rate</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #3498db;">{savings_rate:.1f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("##### Cash Flow Trend (Income vs Expense)")
        fig_trend = generate_monthly_trend_chart(transactions)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col2:
        st.write("##### Net Worth Progression")
        fig_nw = generate_net_worth_trend(transactions)
        st.plotly_chart(fig_nw, use_container_width=True)
        
    # Detailed Monthly Reports Table
    st.write("")
    st.subheader("Monthly Report Sheets")
    
    df_raw = pd.DataFrame([{
        "Month": t.date.strftime("%B %Y"),
        "MonthSort": t.date.strftime("%Y-%m"),
        "Type": t.type,
        "Amount": t.amount
    } for t in transactions])
    
    # Calculate monthly groups
    monthly_data = []
    months = df_raw["MonthSort"].unique()
    months.sort()
    
    for m_sort in months:
        m_df = df_raw[df_raw["MonthSort"] == m_sort]
        m_name = m_df["Month"].iloc[0]
        
        inc = m_df[m_df["Type"] == "income"]["Amount"].sum()
        exp = m_df[m_df["Type"] == "expense"]["Amount"].sum()
        bal = inc - exp
        rate = (bal / inc * 100) if inc > 0 else 0.0
        
        monthly_data.append({
            "Month": m_name,
            "Income": format_pkr(inc),
            "Expenses": format_pkr(exp),
            "Net Savings": format_pkr(bal),
            "Savings Rate": f"{rate:.1f}%"
        })
        
    df_report = pd.DataFrame(monthly_data)
    st.dataframe(df_report, use_container_width=True)
