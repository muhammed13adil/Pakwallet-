"""Analytics utilities."""

from __future__ import annotations


def calculate_savings_rate(income: float, expenses: float) -> float:
    """Calculate savings rate as percentage."""
    if income == 0:
        return 0
    return ((income - expenses) / income) * 100


def calculate_health_score(savings_rate: float, debt_to_income: float) -> int:
    """Calculate financial health score (0-100)."""
    score = min(100, int(savings_rate * 1.5))  # Savings rate component
    score -= int(debt_to_income * 10)  # Debt component
    return max(0, score)
