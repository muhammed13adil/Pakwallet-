"""Savings goals page for PakWallet."""

import streamlit as st
import datetime
from sqlalchemy.orm import Session
from pakwallet.services.database import SavingsGoal, Transaction
from pakwallet.utils.formatting import format_pkr

def render_savings(session: Session, user_id: int) -> None:
    """Render the savings goals management page."""
    st.title("Savings Goals")
    st.write("Track your targets, contribute regularly, and achieve financial security.")
    
    # Fetch goals
    goals = session.query(SavingsGoal).filter(SavingsGoal.user_id == user_id).all()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("##### Your Savings Targets")
        if not goals:
            st.info("You don't have any active savings goals. Create one on the right!")
        else:
            for goal in goals:
                progress_pct = (goal.current_amount / goal.target_amount) * 100 if goal.target_amount > 0 else 0.0
                progress_pct = min(progress_pct, 100.0)
                
                # Render a card for each goal
                with st.container():
                    st.markdown(
                        f"""
                        <div class="metric-card" style="margin-bottom: 1.5rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.2rem; font-weight: bold; color: var(--pak-gold);">{goal.name}</span>
                                <span style="font-size: 0.85rem; opacity: 0.7;">Target: {goal.target_date.strftime("%Y-%m-%d")}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 1rem; margin: 0.5rem 0;">
                                <span>{format_pkr(goal.current_amount)} saved</span>
                                <span style="font-weight: bold;">{format_pkr(goal.target_amount)} goal</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.progress(progress_pct / 100.0)
                    
                    # Add contribution form inside an expander
                    with st.expander(f"Add Contribution to {goal.name}"):
                        contrib_amount = st.number_input(f"Contribution amount for {goal.name} (PKR)", min_value=100.0, step=500.0, key=f"contrib_amt_{goal.id}")
                        if st.button(f"Contribute Funds", key=f"contrib_btn_{goal.id}"):
                            if contrib_amount > 0:
                                goal.current_amount += contrib_amount
                                
                                # Add corresponding transaction record (expense type, category Savings)
                                new_t = Transaction(
                                    user_id=user_id,
                                    type="expense",
                                    category="Savings",
                                    amount=contrib_amount,
                                    date=datetime.datetime.utcnow(),
                                    description=f"Savings Contribution: {goal.name}"
                                )
                                session.add(new_t)
                                session.commit()
                                st.success("Contribution recorded!")
                                st.rerun()
                                
    with col2:
        st.write("##### Create New Target")
        with st.form("create_goal_form", clear_on_submit=True):
            goal_name = st.text_input("Goal Name (e.g. Hajj 2027, Emergency Fund)")
            target_amt = st.number_input("Target Amount (PKR)", min_value=1000.0, step=5000.0)
            initial_contrib = st.number_input("Initial Deposit (optional, PKR)", min_value=0.0, step=1000.0)
            target_date = st.date_input("Target Date", datetime.date.today() + datetime.timedelta(days=365))
            
            submitted = st.form_submit_button("Create Savings Goal", use_container_width=True)
            if submitted:
                if not goal_name.strip():
                    st.error("Please enter a goal name.")
                else:
                    new_goal = SavingsGoal(
                        user_id=user_id,
                        name=goal_name,
                        target_amount=target_amt,
                        current_amount=initial_contrib,
                        target_date=datetime.datetime.combine(target_date, datetime.time.min)
                    )
                    session.add(new_goal)
                    
                    # Add initial transaction if deposited
                    if initial_contrib > 0:
                        new_t = Transaction(
                            user_id=user_id,
                            type="expense",
                            category="Savings",
                            amount=initial_contrib,
                            date=datetime.datetime.utcnow(),
                            description=f"Initial Deposit: {goal_name}"
                        )
                        session.add(new_t)
                        
                    session.commit()
                    st.success(f"Goal '{goal_name}' created successfully!")
                    st.rerun()
