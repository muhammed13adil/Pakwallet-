"""Database services and SQLAlchemy models for PakWallet."""

import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pakwallet.config import settings

# SQLite Database setup
DATABASE_URL = "sqlite:///pakwallet.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User database model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    transaction_pin = Column(String, default="1234")
    otp_code = Column(String, nullable=True)

class Transaction(Base):
    """Transaction database model."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # "income" or "expense"
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String, nullable=True)

class SavingsGoal(Base):
    """Savings goal database model."""
    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=False)

class Bill(Base):
    """Bill database model."""
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., "Electricity", "Gas", "Internet", "School Fees"
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, default=False)

def initialize_database() -> None:
    """Create database tables and insert demo data if empty."""
    Base.metadata.create_all(bind=engine)
    
    # Pre-populate demo user and mock data if database is empty
    session = SessionLocal()
    try:
        demo_email = settings.demo_user_email
        demo_user = session.query(User).filter(User.email == demo_email).first()
        
        if not demo_user:
            # Hash password using bcrypt
            import bcrypt
            pwd_bytes = settings.demo_user_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_pwd = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
            
            # Create user
            new_user = User(
                name="Muhammad Adil",
                email=demo_email,
                password_hash=hashed_pwd,
                transaction_pin="1234"
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            
            # Insert demo transactions
            demo_transactions = [
                # Income
                Transaction(user_id=new_user.id, type="income", category="Salary", amount=150000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=20), description="Monthly Salary"),
                Transaction(user_id=new_user.id, type="income", category="Freelance", amount=35000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=10), description="Web Dev Freelance Work"),
                Transaction(user_id=new_user.id, type="income", category="Investment", amount=12000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=5), description="Mutual Fund Dividend"),
                
                # Expenses
                Transaction(user_id=new_user.id, type="expense", category="Rent", amount=40000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=18), description="House Rent"),
                Transaction(user_id=new_user.id, type="expense", category="Groceries", amount=25000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=15), description="Metro Cash & Carry"),
                Transaction(user_id=new_user.id, type="expense", category="Utilities", amount=18000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=12), description="Electricity and Gas Bills"),
                Transaction(user_id=new_user.id, type="expense", category="Fuel", amount=12000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=8), description="PSO Fuel Refill"),
                Transaction(user_id=new_user.id, type="expense", category="Dining Out", amount=8500.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=3), description="Dinner at Kolachi"),
                Transaction(user_id=new_user.id, type="expense", category="Medical", amount=3000.0, date=datetime.datetime.utcnow() - datetime.timedelta(days=2), description="Pharmacy medicine"),
            ]
            session.add_all(demo_transactions)
            
            # Insert demo savings goals
            demo_savings = [
                SavingsGoal(user_id=new_user.id, name="Emergency Fund", target_amount=100000.0, current_amount=45000.0, target_date=datetime.datetime.utcnow() + datetime.timedelta(days=120)),
                SavingsGoal(user_id=new_user.id, name="Hajj Planning", target_amount=800000.0, current_amount=150000.0, target_date=datetime.datetime.utcnow() + datetime.timedelta(days=730)),
                SavingsGoal(user_id=new_user.id, name="Child Education Fund", target_amount=500000.0, current_amount=75000.0, target_date=datetime.datetime.utcnow() + datetime.timedelta(days=365)),
            ]
            session.add_all(demo_savings)
            
            # Insert demo bills
            demo_bills = [
                Bill(user_id=new_user.id, provider="K-Electric", type="Electricity", amount=14500.0, due_date=datetime.datetime.utcnow() + datetime.timedelta(days=5), is_paid=False),
                Bill(user_id=new_user.id, provider="Sui Southern Gas", type="Gas", amount=1850.0, due_date=datetime.datetime.utcnow() + datetime.timedelta(days=7), is_paid=False),
                Bill(user_id=new_user.id, provider="Nayatel", type="Internet", amount=3200.0, due_date=datetime.datetime.utcnow() + datetime.timedelta(days=3), is_paid=False),
                Bill(user_id=new_user.id, provider="The City School", type="School Fees", amount=12000.0, due_date=datetime.datetime.utcnow() + datetime.timedelta(days=10), is_paid=False),
            ]
            session.add_all(demo_bills)
            
            session.commit()
    finally:
        session.close()
