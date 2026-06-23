"""Calculator utilities."""

from __future__ import annotations


def compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculate compound interest."""
    return principal * ((1 + rate / 100) ** years)


def calculate_zakat(wealth: float, threshold: float = 612000) -> float:
    """Calculate Zakat amount (2.5% of wealth above threshold)."""
    if wealth > threshold:
        return (wealth - threshold) * 0.025
    return 0


def calculate_emi(principal: float, rate: float, months: int) -> float:
    """Calculate EMI (Equated Monthly Installment)."""
    monthly_rate = rate / 100 / 12
    if monthly_rate == 0:
        return principal / months
    return (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
