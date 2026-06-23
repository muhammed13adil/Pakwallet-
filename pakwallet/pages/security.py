"""Security settings page for PakWallet."""

import streamlit as st
import bcrypt
from sqlalchemy.orm import Session
from pakwallet.services.database import User

def render_security(session: Session, user_id: int) -> None:
    """Render password reset, Transaction PIN settings, and OTP settings."""
    st.title("Security Settings")
    st.write("Manage your password, transaction PIN, and session security.")
    
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        st.error("User not found.")
        return
        
    col1, col2 = st.columns(2)
    
    # Update Password
    with col1:
        st.write("##### Update Password")
        with st.form("update_password_form", clear_on_submit=True):
            curr_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            conf_pwd = st.text_input("Confirm New Password", type="password")
            
            pwd_submitted = st.form_submit_button("Update Password", use_container_width=True)
            if pwd_submitted:
                if not curr_pwd or not new_pwd or not conf_pwd:
                    st.error("Please fill in all fields.")
                elif new_pwd != conf_pwd:
                    st.error("New passwords do not match.")
                elif len(new_pwd) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    # Verify current password
                    curr_pwd_bytes = curr_pwd.encode('utf-8')
                    db_pwd_bytes = user.password_hash.encode('utf-8')
                    
                    if not bcrypt.checkpw(curr_pwd_bytes, db_pwd_bytes):
                        st.error("Incorrect current password.")
                    else:
                        # Hash and save new password
                        new_pwd_bytes = new_pwd.encode('utf-8')
                        hashed_pwd = bcrypt.hashpw(new_pwd_bytes, bcrypt.gensalt()).decode('utf-8')
                        
                        user.password_hash = hashed_pwd
                        session.commit()
                        st.success("Password updated successfully!")
                        
    # Transaction PIN & MFA
    with col2:
        st.write("##### Transaction PIN (4-Digits)")
        st.caption("Required for bill payments and fund transfers.")
        with st.form("update_pin_form", clear_on_submit=True):
            current_pin = user.transaction_pin or "Not Set"
            st.write(f"Current PIN: `{current_pin}`")
            new_pin = st.text_input("New 4-Digit PIN", type="password", max_chars=4)
            conf_pin = st.text_input("Confirm New PIN", type="password", max_chars=4)
            
            pin_submitted = st.form_submit_button("Update PIN", use_container_width=True)
            if pin_submitted:
                if not new_pin.isdigit() or len(new_pin) != 4:
                    st.error("PIN must be exactly 4 digits.")
                elif new_pin != conf_pin:
                    st.error("PINs do not match.")
                else:
                    user.transaction_pin = new_pin
                    session.commit()
                    st.success("Transaction PIN updated successfully!")
                    st.rerun()
                    
        st.write("")
        st.write("##### One-Time Password (OTP) Verification")
        st.caption("Receive a code via SMS/Email for high-value transactions.")
        
        mfa_enabled = st.toggle("Enable Two-Factor Authentication (MFA)", value=False)
        if mfa_enabled:
            st.info("MFA setup is currently in Demo mode. In production, this connects to an SMS gateway (e.g. Twilio) or Email OTP provider.")
