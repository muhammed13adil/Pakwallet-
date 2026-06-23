"""Financial calculators page for PakWallet."""

import streamlit as st
from pakwallet.utils.formatting import format_pkr
from pakwallet.utils.calculators import (
    calculate_sip, 
    calculate_lump_sum,
    calculate_loan_emi, 
    calculate_loan_affordability,
    calculate_education_cost, 
    calculate_zakat, 
    calculate_freelance_tax
)

def render_calculators() -> None:
    """Render financial calculators tabs."""
    st.title("Financial Calculators")
    st.write("Plan and simulate your future financial decisions.")
    
    tabs = st.tabs([
        "📊 Mutual Fund Investment", 
        "🏠 Home Loan Planning", 
        "🚗 Car Financing", 
        "🎓 Child Education", 
        "🕌 Zakat Calculator", 
        "💼 Freelancer Tax"
    ])
    
    # --- Tab 1: SIP & Lump Sum ---
    with tabs[0]:
        st.subheader("Mutual Fund Investment Calculator")
        st.write("Estimate the growth of your mutual fund investments using SIP or Lump Sum options.")
        
        calc_type = st.radio("Investment Mode", ["SIP (Monthly)", "Lump Sum (One-Time)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if calc_type == "SIP (Monthly)":
                sip_amount = st.number_input("Monthly Investment Amount (PKR)", min_value=500, value=5000, step=500, key="sip_amt")
                sip_return = st.slider("Expected Annual Return Rate (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="sip_ret")
                sip_years = st.slider("Time Period (Years)", min_value=1, max_value=40, value=10, step=1, key="sip_yrs")
                res = calculate_sip(sip_amount, sip_return, sip_years)
            else:
                lump_amount = st.number_input("One-Time Investment Amount (PKR)", min_value=5000, value=50000, step=5000, key="lump_amt")
                lump_return = st.slider("Expected Annual Return Rate (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="lump_ret")
                lump_years = st.slider("Time Period (Years)", min_value=1, max_value=40, value=10, step=1, key="lump_yrs")
                res = calculate_lump_sum(lump_amount, lump_return, lump_years)
            
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Future Value</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #2ecc71; margin: 0.5rem 0;">{format_pkr(res["future_value"])}</div>
                    <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Total Invested:</span>
                        <span style="font-weight: bold;">{format_pkr(res["total_invested"])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                        <span>Estimated Returns:</span>
                        <span style="font-weight: bold; color: var(--pak-gold);">{format_pkr(res["estimated_returns"])}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # --- Tab 2: Home Loan EMI & Affordability ---
    with tabs[1]:
        st.subheader("Home Loan EMI & Affordability Calculator")
        st.write("Calculate your monthly mortgage payments or estimate your maximum loan eligibility.")
        
        mode = st.radio("Calculation Type", ["Calculate Monthly EMI", "Check Loan Affordability"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if mode == "Calculate Monthly EMI":
                home_amount = st.number_input("Loan Amount (PKR)", min_value=100000, value=3000000, step=100000, key="home_amt")
                home_interest = st.slider("Annual Interest Rate / KIBOR + Spread (%)", min_value=1.0, max_value=35.0, value=15.0, step=0.5, key="home_int")
                home_years = st.slider("Tenure (Years)", min_value=1, max_value=30, value=15, step=1, key="home_yrs")
                res = calculate_loan_emi(home_amount, home_interest, home_years)
            else:
                monthly_inc = st.number_input("Your Net Monthly Income (PKR)", min_value=20000, value=150000, step=5000, key="aff_inc")
                home_interest = st.slider("Annual Interest Rate (%)", min_value=1.0, max_value=35.0, value=15.0, step=0.5, key="aff_int")
                home_years = st.slider("Tenure (Years)", min_value=1, max_value=30, value=15, step=1, key="aff_yrs")
                res = calculate_loan_affordability(monthly_inc, home_interest, home_years)
            
        with col2:
            if mode == "Calculate Monthly EMI":
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Monthly EMI</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0.5rem 0;">{format_pkr(res["emi"])}</div>
                        <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                            <span>Principal Amount:</span>
                            <span style="font-weight: bold;">{format_pkr(home_amount)}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                            <span>Total Interest Payable:</span>
                            <span style="font-weight: bold; color: #e74c3c;">{format_pkr(res["total_interest"])}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                            <span>Total Amount Payable:</span>
                            <span style="font-weight: bold;">{format_pkr(res["total_payable"])}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Max Affordable Loan</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: #2ecc71; margin: 0.5rem 0;">{format_pkr(res["max_loan"])}</div>
                        <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                            <span>Recommended Max EMI (40% of income):</span>
                            <span style="font-weight: bold; color: var(--pak-gold);">{format_pkr(res["max_emi"])}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
    # --- Tab 3: Car Financing ---
    with tabs[2]:
        st.subheader("Car Financing Calculator")
        st.write("Simulate auto leasing and monthly EMIs.")
        
        col1, col2 = st.columns(2)
        with col1:
            car_price = st.number_input("Car Price (PKR)", min_value=500000, value=2500000, step=50000, key="car_prc")
            car_down_pct = st.slider("Down Payment (%)", min_value=10, max_value=80, value=30, step=5, key="car_down")
            car_interest = st.slider("Financing Interest Rate (%)", min_value=1.0, max_value=35.0, value=17.0, step=0.5, key="car_int")
            car_years = st.slider("Financing Tenure (Years)", min_value=1, max_value=7, value=5, step=1, key="car_yrs")
            
            down_payment = car_price * (car_down_pct / 100)
            loan_amount = car_price - down_payment
            
        with col2:
            res = calculate_loan_emi(loan_amount, car_interest, car_years)
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Monthly EMI</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0.5rem 0;">{format_pkr(res["emi"])}</div>
                    <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Down Payment:</span>
                        <span style="font-weight: bold;">{format_pkr(down_payment)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Financed Amount:</span>
                        <span style="font-weight: bold;">{format_pkr(loan_amount)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Total Interest Payable:</span>
                        <span style="font-weight: bold; color: #e74c3c;">{format_pkr(res["total_interest"])}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # --- Tab 4: Child Education ---
    with tabs[3]:
        st.subheader("Child Education Planning Calculator")
        st.write("Plan and save for your child's higher education cost adjusted for inflation.")
        
        col1, col2 = st.columns(2)
        with col1:
            curr_cost = st.number_input("Current Cost of Degree (PKR)", min_value=10000, value=800000, step=50000, key="edu_cost")
            edu_years = st.slider("Years Until College", min_value=1, max_value=25, value=10, key="edu_yrs")
            inflation = st.slider("Expected Annual Inflation Rate (%)", min_value=1.0, max_value=30.0, value=8.0, step=0.5, key="edu_inf")
            edu_return = st.slider("Expected Investment Annual Returns (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="edu_ret")
            
        with col2:
            res = calculate_education_cost(curr_cost, edu_years, inflation, edu_return)
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Future Adjusted Cost</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #e74c3c; margin: 0.5rem 0;">{format_pkr(res["future_cost"])}</div>
                    <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Required Monthly Savings</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #2ecc71; margin: 0.3rem 0;">{format_pkr(res["monthly_savings_required"])}</div>
                    <div style="font-size: 0.8rem; opacity: 0.7;">Calculated using compound growth at {edu_return}% annual returns.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # --- Tab 5: Zakat ---
    with tabs[4]:
        st.subheader("Zakat Calculator")
        st.write("Calculate your annual Zakat contribution (2.5% of net wealth).")
        
        col1, col2 = st.columns(2)
        with col1:
            gold_val = st.number_input("Value of Gold Assets (PKR)", min_value=0.0, value=0.0, step=5000.0, key="zak_gold")
            silver_val = st.number_input("Value of Silver Assets (PKR)", min_value=0.0, value=0.0, step=2000.0, key="zak_silv")
            cash_val = st.number_input("Cash on hand & Bank Balance (PKR)", min_value=0.0, value=150000.0, step=5000.0, key="zak_cash")
            other_val = st.number_input("Other Investments & Assets (PKR)", min_value=0.0, value=0.0, step=5000.0, key="zak_oth")
            liab_val = st.number_input("Debts & Immediate Liabilities (PKR)", min_value=0.0, value=0.0, step=5000.0, key="zak_liab")
            
        with col2:
            res = calculate_zakat(gold_val, silver_val, cash_val, other_val, liab_val)
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Zakat Due</div>
                    <div style="font-size: 2rem; font-weight: 800; color: #2ecc71; margin: 0.5rem 0;">
                        {format_pkr(res["zakat_due"])}
                    </div>
                    <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Net Wealth Subject to Zakat:</span>
                        <span style="font-weight: bold;">{format_pkr(res["net_wealth"])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Nisab Threshold (approx):</span>
                        <span style="font-weight: bold; color: var(--pak-gold);">{format_pkr(res["nisab_threshold"])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                        <span>Nisab Met?</span>
                        <span style="font-weight: bold; color: {'#2ecc71' if res['is_eligible'] else '#e74c3c'};">
                            {'YES' if res['is_eligible'] else 'NO'}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # --- Tab 6: Freelancer Tax ---
    with tabs[5]:
        st.subheader("Freelancer & IT Export Income Tax Calculator")
        st.write("Simulate tax liabilities based on FBR (Pakistan) regulations.")
        
        col1, col2 = st.columns(2)
        with col1:
            annual_inc = st.number_input("Annual Income (PKR)", min_value=0.0, value=1800000.0, step=50000.0, key="tax_inc")
            pseb_reg = st.checkbox("Registered with Pakistan Software Export Board (PSEB)?", value=True, key="tax_pseb")
            
        with col2:
            res = calculate_freelance_tax(annual_inc, pseb_reg)
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.7; text-transform: uppercase;">Annual Tax Due</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #e74c3c; margin: 0.5rem 0;">{format_pkr(res["tax_due"])}</div>
                    <hr style="margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Monthly Tax Reserve:</span>
                        <span style="font-weight: bold; color: #e74c3c;">{format_pkr(res["monthly_tax_reserve"])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Net Take-home Annual Income:</span>
                        <span style="font-weight: bold; color: #2ecc71;">{format_pkr(res["net_income"])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem;">
                        <span>Effective Tax Rate:</span>
                        <span style="font-weight: bold;">{res["effective_rate"]:.2f}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                        <span>Tax Regime Type:</span>
                        <span style="font-weight: bold; color: var(--pak-gold);">
                            {'PSEB Concessional Final (0.25%)' if pseb_reg else 'Normal non-salaried slabs'}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
