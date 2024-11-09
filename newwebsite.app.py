import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import wikipediaapi
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Minimalist black theme styling
st.markdown("""
    <style>
    body {
        background-color: #1c1c1c;
        color: #e0e0e0;
    }
    .css-1v3fvcr {
        background-color: #1c1c1c !important;
    }
    .stButton>button {
        background-color: #00BFFF !important;
        color: white !important;
    }
    .css-2trqyj {
        color: white !important;
    }
    h1, h2, h3, h4, h5 {
        color: #00BFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions for technical indicators
def calculate_sma(data, period=50):
    return data['Close'].rolling(window=period).mean()

def calculate_rsi(data, period=20):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data):
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    return ema_12 - ema_26

# Caching stock data fetching
@st.cache_data
def load_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")  # Temporarily reduce period to 1 year for faster loading

# Caching company information fetching
@st.cache_data
def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    return {
        "Sector": stock.info.get("sector", "N/A"),
        "Country": stock.info.get("country", "N/A"),
        "CEO": stock.info.get("ceo", "N/A"),
        "PE Ratio": stock.info.get("trailingPE", "N/A"),
        "Price to Cashflow": stock.info.get("priceToCashflow", "N/A"),
        "PB Ratio": stock.info.get("priceToBook", "N/A"),
        "EPS": stock.info.get("trailingEps", "N/A"),
    }

# Fetch CEO information from Wikipedia
@st.cache_data
def get_ceo_bio(ceo_name):
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(ceo_name)
    if page.exists():
        return page.summary
    else:
        return "Wikipedia information not available for the specified CEO."

# Caching model training
@st.cache_resource
def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=10)  # Reduced number of estimators for faster training
    model.fit(X_train, y_train)
    return model

# Main function
def main():
    # Sidebar for ticker input
    ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
    
    # Load stock data and company info
    stock_data = load_stock_data(ticker)
    company_info = get_company_info(ticker)
    
    # 1. Company Information
    st.header("Company Information")
    st.write("### Basic Info")
    st.write(f"**Sector:** {company_info['Sector']}")
    st.write(f"**Country:** {company_info['Country']}")
    st.write(f"**CEO:** {company_info['CEO']}")
    
    # CEO biography from Wikipedia
    if company_info["CEO"] != "N/A":
        ceo_bio = get_ceo_bio(company_info["CEO"])
        st.write(f"### CEO Biography\n{ceo_bio}")
    else:
        st.write("CEO information is not available.")

    # 2. Fundamental Analysis
    st.header("Fundamental Analysis")
    st.write(f"**P/E Ratio:** {company_info['PE Ratio']}")
    st.write(f"**Price to Operating Cash Flow:** {company_info['Price to Cashflow']}")
    st.write(f"**P/B Ratio:** {company_info['PB Ratio']}")
    st.write(f"**EPS:** {company_info['EPS']}")
    
    # Recommendations based on P/E ratio
    st.write("### Recommendation")
    if company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] < 15:
        recommendation = "Buy"
        description = "Undervalued"
    elif company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] > 25:
        recommendation = "Sell"
        description = "Overvalued"
    else:
        recommendation = "Hold"
        description = "Fairly Valued"
    
    st.write(f"**Recommendation:** {recommendation}")
    st.write(f"**Description:** {description}")
    
    # 3. Technical Analysis
    st.header("Technical Analysis")
    
    # Calculate SMA, RSI, MACD
    stock_data['SMA_50'] = calculate_sma(stock_data, 50)
    stock_data['SMA_200'] = calculate_sma(stock_data, 200)
    stock_data['RSI'] = calculate_rsi(stock_data, 20)
    stock_data['MACD'] = calculate_macd(stock_data)
    
    # Plotting with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stoc
