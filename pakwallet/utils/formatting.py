"""Formatting utilities."""

from __future__ import annotations


def format_currency(amount: float, currency: str = "PKR") -> str:
    """Format amount as currency."""
    return f"{currency} {amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value:.{decimals}f}%"
