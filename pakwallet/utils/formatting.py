"""Formatting utilities for PakWallet."""

def format_pkr(amount: float) -> str:
    """Format float/int to PKR currency format (e.g. Rs. 150,000.00)."""
    if amount is None:
        amount = 0.0
    return f"Rs. {amount:,.2f}"
