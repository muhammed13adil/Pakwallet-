"""Calculations logic for financial calculators."""

def calculate_sip(monthly_investment: float, annual_return_rate: float, years: int) -> dict:
    """Calculate Systematic Investment Plan (SIP) future value."""
    monthly_rate = (annual_return_rate / 100) / 12
    months = years * 12
    
    if monthly_rate == 0:
        future_value = monthly_investment * months
    else:
        future_value = monthly_investment * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
        
    total_invested = monthly_investment * months
    estimated_returns = future_value - total_invested
    
    return {
        "future_value": future_value,
        "total_invested": total_invested,
        "estimated_returns": estimated_returns
    }

def calculate_loan_emi(loan_amount: float, annual_interest_rate: float, years: int) -> dict:
    """Calculate Loan EMI (Home/Car loan) and interest details."""
    monthly_rate = (annual_interest_rate / 100) / 12
    months = years * 12
    
    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = loan_amount * monthly_rate * ((1 + monthly_rate)**months) / (((1 + monthly_rate)**months) - 1)
        
    total_payable = emi * months
    total_interest = total_payable - loan_amount
    
    return {
        "emi": emi,
        "total_payable": total_payable,
        "total_interest": total_interest
    }

def calculate_education_cost(current_cost: float, years_until_college: int, inflation_rate: float, annual_returns: float) -> dict:
    """Calculate future education cost adjusted for inflation and target monthly savings."""
    future_cost = current_cost * ((1 + (inflation_rate / 100))**years_until_college)
    
    # Calculate monthly savings required to reach target future_cost
    monthly_rate = (annual_returns / 100) / 12
    months = years_until_college * 12
    
    if months == 0:
        monthly_savings = future_cost
    elif monthly_rate == 0:
        monthly_savings = future_cost / months
    else:
        monthly_savings = future_cost * monthly_rate / (((1 + monthly_rate)**months - 1) * (1 + monthly_rate))
        
    return {
        "future_cost": future_cost,
        "monthly_savings_required": monthly_savings
    }

def calculate_zakat(gold_value: float, silver_value: float, cash_amount: float, other_assets: float, liabilities: float) -> dict:
    """Calculate Zakat (2.5% of net wealth if above Nisab threshold)."""
    total_wealth = gold_value + silver_value + cash_amount + other_assets
    net_wealth = total_wealth - liabilities
    
    # Approximate Nisab threshold in PKR (e.g. 52.5 tolas of silver is roughly PKR 135,000 - 150,000 depending on rates)
    nisab_threshold = 150000.0
    
    zakat_due = 0.0
    is_eligible = net_wealth >= nisab_threshold
    
    if is_eligible:
        zakat_due = net_wealth * 0.025
        
    return {
        "net_wealth": max(net_wealth, 0.0),
        "nisab_threshold": nisab_threshold,
        "is_eligible": is_eligible,
        "zakat_due": max(zakat_due, 0.0)
    }

def calculate_lump_sum(investment: float, annual_return_rate: float, years: int) -> dict:
    """Calculate Lump Sum investment future value."""
    rate = annual_return_rate / 100
    future_value = investment * ((1 + rate) ** years)
    estimated_returns = future_value - investment
    
    return {
        "future_value": future_value,
        "total_invested": investment,
        "estimated_returns": estimated_returns
    }

def calculate_loan_affordability(monthly_income: float, interest_rate: float, years: int) -> dict:
    """Calculate maximum affordable loan amount based on income (recommended EMI = 40% of income)."""
    max_emi = monthly_income * 0.40
    monthly_rate = (interest_rate / 100) / 12
    months = years * 12
    
    if monthly_rate == 0:
        max_loan = max_emi * months
    else:
        max_loan = max_emi * (((1 + monthly_rate) ** months) - 1) / (monthly_rate * ((1 + monthly_rate) ** months))
        
    return {
        "max_emi": max_emi,
        "max_loan": max_loan
    }

def calculate_freelance_tax(annual_income: float, is_pseb_registered: bool) -> dict:
    """Calculate Freelancer Tax based on FBR (Pakistan) Tax slabs (2024-25/2026)."""
    tax_due = 0.0
    effective_rate = 0.0
    
    if is_pseb_registered:
        # Export of IT services registered with PSEB has a concessional tax regime (0.25% of turnover)
        tax_due = annual_income * 0.0025
        effective_rate = 0.25
    else:
        # Non-registered IT export tax is 1% of turnover (Final tax regime)
        # However, if treated under normal tax slabs for non-salaried individuals:
        if annual_income <= 600000:
            tax_due = 0.0
        elif annual_income <= 1200000:
            tax_due = (annual_income - 600000) * 0.05
        elif annual_income <= 2200000:
            tax_due = 30000 + (annual_income - 1200000) * 0.15
        elif annual_income <= 3200000:
            tax_due = 180000 + (annual_income - 2200000) * 0.25
        elif annual_income <= 4100000:
            tax_due = 430000 + (annual_income - 3200000) * 0.30
        else:
            tax_due = 700000 + (annual_income - 4100000) * 0.35
            
        effective_rate = (tax_due / annual_income) * 100 if annual_income > 0 else 0.0
        
    net_income = annual_income - tax_due
    monthly_tax_reserve = tax_due / 12
    
    return {
        "tax_due": tax_due,
        "net_income": net_income,
        "effective_rate": effective_rate,
        "monthly_tax_reserve": monthly_tax_reserve
    }
