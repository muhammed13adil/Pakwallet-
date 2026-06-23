"""Authentication service."""

from __future__ import annotations

from datetime import datetime

import streamlit as st
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from pakwallet.services.database import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """Authenticate a user."""
    user = session.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def login_user(user: User) -> None:
    """Set session state for logged-in user."""
    st.session_state["user_id"] = str(user.id)
    st.session_state["user_name"] = user.name
    st.session_state["user_email"] = user.email


def logout_user() -> None:
    """Clear session state."""
    for key in ["user_id", "user_name", "user_email"]:
        if key in st.session_state:
            del st.session_state[key]


def require_authentication() -> bool:
    """Check if user is authenticated."""
    return "user_id" in st.session_state
