"""Rule-based AI Budget Assistant page for PakWallet."""

import streamlit as st
import datetime
from sqlalchemy.orm import Session
from pakwallet.services.database import Transaction
from pakwallet.utils.formatting import format_pkr

def render_assistant(session: Session, user_id: int) -> None:
    """Render rule-based AI Budget Assistant chat interface."""
    st.title("AI Budget Assistant")
    st.write("Ask questions about your wallet balance, expenses, savings rate, Zakat, or tax slabs in Pakistan.")
    
    # Initialize message list in session state
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Assalam-o-Alaikum! I am your PakWallet Smart Assistant. Ask me about your budget, Zakat eligibility, freelancer tax rates, or your current balance!"}
        ]
        
    # Render chat history
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Get user input
    user_query = st.chat_input("Ask a question...")
    
    if user_query:
        # Display user message
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state["chat_messages"].append({"role": "user", "content": user_query})
        
        # Process query and get response
        response = get_assistant_response(session, user_id, user_query)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state["chat_messages"].append({"role": "assistant", "content": response})

def get_assistant_response(session: Session, user_id: int, query: str) -> str:
    """Analyze user query and return a contextual rule-based response."""
    query_lower = query.lower().strip()
    
    # Fetch user data to make it dynamic
    transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    savings_rate = ((total_income - total_expense) / total_income) * 100 if total_income > 0 else 0.0
    
    # 1. Greetings
    if any(greet in query_lower for greet in ["hello", "hi", "assalam", "salam", "hey", "aalaikum"]):
        return "Wa Alaikum Assalam! Hope you are doing well. How can I help you manage your finances today?"
        
    # 2. Balance & Financial Status
    elif "balance" in query_lower or "how much money" in query_lower:
        return f"Your current available wallet balance is **{format_pkr(balance)}** (Total Income: {format_pkr(total_income)} | Total Expenses: {format_pkr(total_expense)})."
        
    # 3. Expense / Spending analysis
    elif "spending" in query_lower or "expensive" in query_lower or "spent" in query_lower or "expense" in query_lower:
        if not transactions:
            return "You haven't recorded any transactions yet. Add some on the Dashboard to get an analysis!"
            
        # Group by category
        categories = {}
        for t in transactions:
            if t.type == "expense":
                categories[t.category] = categories.get(t.category, 0.0) + t.amount
                
        if not categories:
            return "You haven't recorded any expenses yet! Keep up the good work and maintain a high savings rate."
            
        top_category = max(categories, key=categories.get)
        top_amount = categories[top_category]
        
        response = f"You have spent a total of **{format_pkr(total_expense)}** this month.\n\n"
        response += f"Your highest expense category is **{top_category}** at **{format_pkr(top_amount)}**.\n\n"
        
        if savings_rate < 15.0:
            response += f"⚠️ Your current savings rate is **{savings_rate:.1f}%**, which is lower than the recommended 20%. Consider reducing discretionary spending on categories like **{top_category}**."
        else:
            response += f"🎉 Your current savings rate is **{savings_rate:.1f}%**, which is excellent! You are on track."
            
        return response
        
    # 4. Savings advice
    elif "save" in query_lower or "saving" in query_lower:
        return (
            "Here are some helpful tips for saving money in Pakistan:\n\n"
            "1. **Follow the 50/30/20 Rule**: Allocate 50% of your income for Needs (Rent, Utilities, Food), 30% for Wants (Dining Out, Shopping), and 20% directly into Savings.\n"
            "2. **Automate Deposits**: Set aside a portion of your salary as soon as it is credited to your bank account.\n"
            "3. **Invest in Shariah-Compliant Mutual Funds**: Check out our Mutual Fund SIP calculator to simulate compounding gains.\n"
            "4. **Control Fuel & Dining**: Fuel and dining out are often the largest discretionary expenses in urban centers."
        )
        
    # 5. Zakat rules
    elif "zakat" in query_lower or "nisab" in query_lower:
        return (
            "🕌 **Zakat Guidelines**:\n\n"
            "Zakat is obligatory at **2.5%** on wealth that meets or exceeds the Nisab threshold and has been held for one lunar year.\n\n"
            "**Nisab thresholds**:\n"
            "- Gold: 7.5 Tolas (approx 87.48 grams)\n"
            "- Silver: 52.5 Tolas (approx 612.36 grams) - commonly used for cash equivalents (approx Rs. 135,000 - 150,000 depending on current silver prices).\n\n"
            "You can use our **Zakat Calculator** tab on the Financial Calculators page to enter your assets and calculate the exact amount due."
        )
        
    # 6. Tax guidelines
    elif "tax" in query_lower or "fbr" in query_lower or "freelancer tax" in query_lower:
        return (
            "💼 **Freelancer & IT Export Tax in Pakistan**:\n\n"
            "- **Registered with PSEB**: If you register with the Pakistan Software Export Board, you qualify for a concessional Final Tax Regime (FTR) of **0.25%** of your export remittance.\n"
            "- **Non-Registered IT Exports**: Taxed at **1%** of export remittance.\n"
            "- **Local Income / Non-Exports**: Taxed under normal non-salaried tax slabs (starting at 0% below 6 Lakhs per year up to 35% above 41 Lakhs per year).\n\n"
            "Use our **Freelancer Tax** tab on the Financial Calculators page to run a detailed simulation."
        )
        
    # 7. Default fall-through
    else:
        return "I can help you with your budget! Try asking me:\n- 'What is my current balance?'\n- 'Analyze my spending'\n- 'Give me tips on how to save'\n- 'What are the rules for Zakat?'\n- 'What is the freelancer tax rate?'"
