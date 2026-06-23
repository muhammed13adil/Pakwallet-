"""Security page."""

from __future__ import annotations

import streamlit as st
from sqlalchemy.orm import Session


def render_security(session: Session, user_id: int) -> None:
    """Render security page."""
    st.title("Security Settings")
    st.write(f"Manage your security settings. User ID: {user_id}")
    
    st.subheader("Two-Factor Authentication")
    otp_enabled = st.toggle("Enable OTP", value=False)
    if otp_enabled:
        st.success("OTP is now enabled for your account.")
    
    st.subheader("Transaction PIN")
    if st.button("Set Transaction PIN"):
        st.info("Enter a 4-digit PIN for transactions.")
        pin = st.text_input("PIN", type="password")
        if pin:
            st.success("PIN set successfully!")
