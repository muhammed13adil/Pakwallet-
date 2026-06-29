"""Dashboard page for PakWallet."""

import streamlit as st
from sqlalchemy.orm import Session
from pakwallet.services.database import Transaction
from pakwallet.utils.formatting import format_pkr
from pakwallet.utils.analytics import generate_income_expense_chart, generate_expense_category_chart

def render_dashboard(session: Session, user_id: int) -> None:
    """Render the dashboard page, showing metrics and charts."""
    
    st.title("Wallet Dashboard")
    st.write("Real-time summary of your personal finances.")
    
    # Fetch all transactions for this user
    transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    # Calculate stats
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    
    savings_rate = 0.0
    if total_income > 0:
        savings_rate = ((total_income - total_expense) / total_income) * 100
        
    # Financial Health Score
    health_score = 0
    if savings_rate > 0:
        # Savings rate contributes up to 60 points
        health_score += min(int(savings_rate * 1.5), 60)
    # Having active balance contributes up to 40 points
    if balance > 50000:
        health_score += 40
    elif balance > 0:
        health_score += int((balance / 50000) * 40)
        
    health_score = max(min(health_score, 100), 0)
    
    # Define health score text and color
    if health_score >= 80:
        health_status = "Excellent"
        health_color = "green"
    elif health_score >= 50:
        health_status = "Good"
        health_color = "gold"
    else:
        health_status = "Needs Attention"
        health_color = "red"
        
    # Stats Layout in columns using our custom CSS metric-card classes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Available Balance</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0.5rem 0;">{format_pkr(balance)}</div>
                <div style="font-size: 0.85rem; color: #2ecc71;">Keep it growing!</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Monthly Savings Rate</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #D4AF37; margin: 0.5rem 0;">{savings_rate:.1f}%</div>
                <div style="font-size: 0.85rem; color: #ffffff; opacity: 0.7;">Recommended: 20% +</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Financial Health Score</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0.5rem 0;">
                    {health_score} <span style="font-size: 1rem; opacity: 0.7;">/ 100</span>
                </div>
                <div style="font-size: 0.85rem; font-weight: bold;">
                    Status: <span class="text-{health_color}">{health_status}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.write("")
    
    # Charts Section
    st.subheader("Financial Analytics Visualizer")
    char_col1, char_col2 = st.columns(2)
    
    with char_col1:
        st.markdown("<div style='text-align: center; font-weight: bold; margin-bottom: 10px;'>Income vs Expenses</div>", unsafe_allow_html=True)
        fig_inc_exp = generate_income_expense_chart(transactions)
        st.plotly_chart(fig_inc_exp, use_container_width=True)
        
    with char_col2:
        st.markdown("<div style='text-align: center; font-weight: bold; margin-bottom: 10px;'>Expense Categories</div>", unsafe_allow_html=True)
        fig_cat = generate_expense_category_chart(transactions)
        st.plotly_chart(fig_cat, use_container_width=True)
