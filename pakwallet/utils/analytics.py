"""Analytics visualization helpers using Plotly."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List
from pakwallet.services.database import Transaction

def generate_income_expense_chart(transactions: List[Transaction]) -> go.Figure:
    """Generate double bar or pie chart comparing total income and total expenses."""
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    
    df = pd.DataFrame({
        "Type": ["Total Income", "Total Expenses"],
        "Amount (PKR)": [total_income, total_expense]
    })
    
    fig = px.bar(
        df, 
        x="Type", 
        y="Amount (PKR)", 
        color="Type",
        color_discrete_map={"Total Income": "#2ecc71", "Total Expenses": "#e74c3c"},
        text_auto=".2s"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="",
        yaxis_title="Amount (PKR)"
    )
    
    return fig

def generate_expense_category_chart(transactions: List[Transaction]) -> go.Figure:
    """Generate donut chart showing expense category breakdown."""
    expenses = [t for t in transactions if t.type == "expense"]
    
    if not expenses:
        # Return empty figure with warning message
        fig = go.Figure()
        fig.add_annotation(text="No expenses recorded yet.", showarrow=False, font=dict(size=16, color="white"))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        return fig
        
    df = pd.DataFrame([{
        "Category": t.category,
        "Amount": t.amount
    } for t in expenses])
    
    df_grouped = df.groupby("Category").sum().reset_index()
    
    fig = px.pie(
        df_grouped, 
        values="Amount", 
        names="Category", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#11221b', width=2)))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig

def generate_monthly_trend_chart(transactions: List[Transaction]) -> go.Figure:
    """Generate monthly line chart showing income vs expense trend."""
    if not transactions:
        fig = go.Figure()
        fig.add_annotation(text="No transaction data available.", showarrow=False, font=dict(size=16, color="white"))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        return fig

    df = pd.DataFrame([{
        "Date": t.date.strftime("%Y-%m"),
        "Type": "Income" if t.type == "income" else "Expense",
        "Amount": t.amount
    } for t in transactions])
    
    df_grouped = df.groupby(["Date", "Type"]).sum().reset_index()
    
    fig = px.line(
        df_grouped, 
        x="Date", 
        y="Amount", 
        color="Type",
        color_discrete_map={"Income": "#2ecc71", "Expense": "#e74c3c"},
        markers=True
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Month",
        yaxis_title="Amount (PKR)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig

def generate_net_worth_trend(transactions: List[Transaction]) -> go.Figure:
    """Generate line area chart showing net worth progression over time."""
    if not transactions:
        fig = go.Figure()
        fig.add_annotation(text="No data available.", showarrow=False, font=dict(size=16, color="white"))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        return fig
        
    df = pd.DataFrame([{
        "Date": t.date,
        "NetChange": t.amount if t.type == "income" else -t.amount
    } for t in transactions])
    
    # Sort by date
    df = df.sort_values("Date")
    # Calculate cumulative sum
    df["NetWorth"] = df["NetChange"].cumsum()
    
    # Group by date for line display
    df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
    df_display = df.groupby("DateStr").last().reset_index()
    
    fig = px.area(
        df_display, 
        x="DateStr", 
        y="NetWorth",
        labels={"DateStr": "Date", "NetWorth": "Net Worth (PKR)"}
    )
    
    fig.update_traces(
        line_color="#D4AF37", 
        fillcolor="rgba(212, 175, 55, 0.2)",
        mode="lines+markers"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Date",
        yaxis_title="Net Worth (PKR)"
    )
    
    return fig
