"""Dashboard page for PakWallet."""

import streamlit as st
import datetime
from sqlalchemy.orm import Session
from pakwallet.services.database import Transaction
from pakwallet.utils.formatting import format_pkr
from pakwallet.utils.analytics import generate_income_expense_chart, generate_expense_category_chart

def render_dashboard(session: Session, user_id: int) -> None:
    """Render the dashboard page, showing metrics, charts, and transaction management."""
    
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
        
    # Transaction Management
    st.write("")
    st.subheader("Transaction Management")
    
    t_col1, t_col2 = st.columns([2, 1])
    
    with t_col1:
        st.write("##### Recent Transactions")
        recent = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]
        
        if not recent:
            st.info("No transactions recorded yet.")
        else:
            # Table formatting
            table_data = []
            for t in recent:
                date_str = t.date.strftime("%Y-%m-%d")
                amt_str = format_pkr(t.amount)
                type_color = "text-green" if t.type == "income" else "text-red"
                sign = "+" if t.type == "income" else "-"
                
                table_data.append({
                    "Date": date_str,
                    "Description": t.description or t.category,
                    "Category": t.category,
                    "Type": t.type.capitalize(),
                    "Amount": f"<span class='{type_color}'>{sign} {amt_str}</span>"
                })
                
            df_table = pd.DataFrame(table_data)
            st.write(df_table.to_html(escape=False, index=False), unsafe_allow_html=True)
            
    with t_col2:
        st.write("##### Add New Transaction")
        with st.form("new_transaction_form", clear_on_submit=True):
            t_type = st.selectbox("Type", ["Expense", "Income"])
            t_amount = st.number_input("Amount (PKR)", min_value=1.0, step=100.0)
            
            categories = ["Salary", "Freelance", "Rent", "Groceries", "Utilities", "Fuel", "Dining Out", "Medical", "Education", "Shopping", "Other"]
            t_category = st.selectbox("Category", categories)
            t_desc = st.text_input("Description (optional)")
            t_date = st.date_input("Date", datetime.date.today())
            
            submitted = st.form_submit_button("Add Record", use_container_width=True)
            if submitted:
                new_t = Transaction(
                    user_id=user_id,
                    type=t_type.lower(),
                    category=t_category,
                    amount=t_amount,
                    date=datetime.datetime.combine(t_date, datetime.time.min),
                    description=t_desc if t_desc.strip() else t_category
                )
                session.add(new_t)
                session.commit()
                st.success("Transaction added successfully!")
                st.rerun()
