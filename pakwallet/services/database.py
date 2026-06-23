"""Database configuration and models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from pakwallet.config import settings

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    transaction_pin_hash = Column(String(255), nullable=True)
    otp_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    """Transaction model."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(80), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)


class SavingsGoal(Base):
    """Savings goal model."""

    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0)
    monthly_contribution = Column(Float, nullable=False)
    target_date = Column(Date, nullable=False)


class Bill(Base):
    """Bill model."""

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(120), nullable=False)
    bill_type = Column(String(80), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(20), default="pending")
    reference_number = Column(String(80), nullable=False)


def initialize_database() -> None:
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
