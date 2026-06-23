"""Authentication services for PakWallet."""

import bcrypt
import streamlit as st
from sqlalchemy.orm import Session
from pakwallet.services.database import User

def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """Authenticate user with email and password using bcrypt."""
    user = session.query(User).filter(User.email == email.strip().lower()).first()
    if not user:
        return None
    
    # Verify hashed password
    password_bytes = password.encode('utf-8')
    hashed_bytes = user.password_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hashed_bytes):
        return user
    return None

def login_user(user: User) -> None:
    """Store authenticated user details in Streamlit session state."""
    st.session_state["authenticated"] = True
    st.session_state["user_id"] = user.id
    st.session_state["user_name"] = user.name
    st.session_state["user_email"] = user.email

def logout_user() -> None:
    """Clear user session details from Streamlit session state."""
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["user_name"] = None
    st.session_state["user_email"] = None

def require_authentication() -> bool:
    """Check if the user is logged in by validating session state."""
    return st.session_state.get("authenticated", False)
