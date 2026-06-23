"""UI components for PakWallet."""

from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    """Inject global CSS styles."""
    st.markdown(
        """
        <style>
        .pak-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 2px solid #1f77b4;
        }
        .pak-header h1 {
            color: #1f77b4;
            margin: 0;
            font-size: 2.5rem;
        }
        .pak-tagline {
            color: #666;
            font-style: italic;
            margin-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
