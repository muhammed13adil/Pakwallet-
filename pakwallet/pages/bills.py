"""Bill payments page for PakWallet."""

import streamlit as st
import datetime
from sqlalchemy.orm import Session
from pakwallet.services.database import Bill, Transaction
from pakwallet.utils.formatting import format_pkr

def render_bills(session: Session, user_id: int) -> None:
    """Render bill payments tracking and mock payments interface."""
    st.title("Bill Payments")
    st.write("Track and pay your utility bills, internet connections, and tuition fees online.")
    
    # Fetch bills
    bills = session.query(Bill).filter(Bill.user_id == user_id).all()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("##### Your Invoices")
        
        tabs = st.tabs(["⚠️ Outstanding Bills", "✅ Paid Invoices"])
        
        unpaid_bills = [b for b in bills if not b.is_paid]
        paid_bills = [b for b in bills if b.is_paid]
        
        # Unpaid Bills
        with tabs[0]:
            if not unpaid_bills:
                st.success("No outstanding bills! You are all caught up.")
            else:
                for bill in unpaid_bills:
                    due_date_str = bill.due_date.strftime("%Y-%m-%d")
                    days_left = (bill.due_date.date() - datetime.date.today()).days
                    
                    if days_left < 0:
                        status_msg = f"<span class='text-red'>OVERDUE by {abs(days_left)} days</span>"
                    elif days_left <= 3:
                        status_msg = f"<span class='text-gold'>Due in {days_left} days</span>"
                    else:
                        status_msg = f"Due in {days_left} days"
                        
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="metric-card" style="margin-bottom: 1.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 1.1rem; font-weight: bold; color: white;">{bill.provider} ({bill.type})</span>
                                    <span style="font-size: 0.85rem; opacity: 0.85;">{status_msg}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.8rem;">
                                    <span style="font-size: 1.5rem; font-weight: 800; color: var(--pak-gold);">{format_pkr(bill.amount)}</span>
                                    <span style="font-size: 0.85rem; opacity: 0.7;">Due Date: {due_date_str}</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Payment button with PIN verification placeholder
                        btn_col1, btn_col2 = st.columns([3, 1])
                        with btn_col2:
                            if st.button(f"Pay Bill", key=f"pay_btn_{bill.id}"):
                                # Mark as paid
                                bill.is_paid = True
                                
                                # Add transaction
                                new_t = Transaction(
                                    user_id=user_id,
                                    type="expense",
                                    category="Utilities",
                                    amount=bill.amount,
                                    date=datetime.datetime.utcnow(),
                                    description=f"Bill Payment: {bill.provider} ({bill.type})"
                                )
                                session.add(new_t)
                                session.commit()
                                st.success(f"Bill for {bill.provider} paid successfully!")
                                st.rerun()
                                
        # Paid Bills
        with tabs[1]:
            if not paid_bills:
                st.info("No paid invoices recorded yet.")
            else:
                table_data = []
                for bill in paid_bills:
                    table_data.append({
                        "Provider": bill.provider,
                        "Type": bill.type,
                        "Amount": format_pkr(bill.amount),
                        "Due Date": bill.due_date.strftime("%Y-%m-%d")
                    })
                st.dataframe(table_data, use_container_width=True)
                
    with col2:
        st.write("##### Add Utility Bill")
        with st.form("add_bill_form", clear_on_submit=True):
            providers = [
                "K-Electric", "LESCO", "SNGPL", "SSGC", "PTCL", 
                "StormFiber", "Nayatel", "Wateen", "The City School", 
                "Beaconhouse", "Mobilink Jazz", "Telenor", "Zong", "Ufone"
            ]
            bill_provider = st.selectbox("Provider", providers)
            
            bill_types = ["Electricity", "Gas", "Internet", "Water", "School Fees", "Mobile Postpaid"]
            bill_type = st.selectbox("Bill Type", bill_types)
            
            bill_amount = st.number_input("Bill Amount (PKR)", min_value=1.0, step=100.0)
            bill_due = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=15))
            
            submitted = st.form_submit_button("Add Invoice", use_container_width=True)
            if submitted:
                new_bill = Bill(
                    user_id=user_id,
                    provider=bill_provider,
                    type=bill_type,
                    amount=bill_amount,
                    due_date=datetime.datetime.combine(bill_due, datetime.time.min),
                    is_paid=False
                )
                session.add(new_bill)
                session.commit()
                st.success("Utility invoice created successfully!")
                st.rerun()
