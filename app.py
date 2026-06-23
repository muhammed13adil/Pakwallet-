"""PakWallet Streamlit entry point."""

from __future__ import annotations

import streamlit as st

from pakwallet.components.ui import inject_global_css
from pakwallet.config import settings
from pakwallet.pages.analytics import render_analytics
from pakwallet.pages.assistant import render_assistant
from pakwallet.pages.bills import render_bills
from pakwallet.pages.calculators import render_calculators
from pakwallet.pages.dashboard import render_dashboard
from pakwallet.pages.savings import render_savings
from pakwallet.pages.security import render_security
from pakwallet.services.auth import authenticate_user, login_user, logout_user, require_authentication
from pakwallet.services.database import SessionLocal, initialize_database


st.set_page_config(
    page_title=f"{settings.app_name} - {settings.tagline}",
    page_icon=":credit_card:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
initialize_database()


def render_login() -> None:
    """Render login screen."""

    st.markdown(
        f"""
        <div class="pak-header">
            <h1>{settings.app_name}</h1>
            <div class="pak-tagline">{settings.tagline}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("Sign in to access your wallet dashboard.")
    with st.form("login_form"):
        email = st.text_input("Email", value=settings.demo_user_email)
        password = st.text_input("Password", type="password", value=settings.demo_user_password)
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        if submitted:
            session = SessionLocal()
            try:
                user = authenticate_user(session, email, password)
                if user:
                    login_user(user)
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            finally:
                session.close()
    st.caption("Demo credentials are pre-filled for local evaluation.")


def render_app() -> None:
    """Render authenticated application shell."""

    st.sidebar.title(settings.app_name)
    st.sidebar.caption(settings.tagline)
    st.sidebar.write(f"Signed in: {st.session_state.get('user_name', 'User')}")
    page = st.sidebar.radio(
        "Navigate",
        [
            "Wallet Dashboard",
            "Financial Calculators",
            "Savings Goals",
            "Bill Payments",
            "AI Budget Assistant",
            "Analytics",
            "Security",
        ],
    )
    if st.sidebar.button("Sign Out", use_container_width=True):
        logout_user()
        st.rerun()

    session = SessionLocal()
    try:
        user_id = int(st.session_state["user_id"])
        if page == "Wallet Dashboard":
            render_dashboard(session, user_id)
        elif page == "Financial Calculators":
            render_calculators()
        elif page == "Savings Goals":
            render_savings(session, user_id)
        elif page == "Bill Payments":
            render_bills(session, user_id)
        elif page == "AI Budget Assistant":
            render_assistant(session, user_id)
        elif page == "Analytics":
            render_analytics(session, user_id)
        elif page == "Security":
            render_security(session, user_id)
    finally:
        session.close()


if require_authentication():
    render_app()
else:
    render_login()
