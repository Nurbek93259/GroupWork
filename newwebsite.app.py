import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

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

# Main function
def main():
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.title("Stock Financial Analysis & Prediction Dashboard")
    
    # Sidebar for ticker input
    ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
    
    # Fetch stock data
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="5y")
    
    # 1. Company Information
    st.header("Company Information")
    st.write("### Basic Info")
    st.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
    st.write(f"**Country:** {stock.info.get('country', 'N/A')}")
    st.write(f"**CEO:** {stock.info.get('ceo', 'N/A')}")
    
    # 2. Fundamental Analysis
    st.header("Fundamental Analysis")
    
    pe_ratio = stock.info.get("trailingPE", "N/A")
    price_to_cashflow = stock.info.get("priceToCashflow", "N/A")
    pb_ratio = stock.info.get("priceToBook", "N/A")
    eps = stock.info.get("trailingEps", "N/A")
    
    st.write(f"**P/E Ratio:** {pe_ratio}")
    st.write(f"**Price to Operating Cash Flow:** {price_to_cashflow}")
    st.write(f"**P/B Ratio:** {pb_ratio}")
    st.write(f"**EPS:** {eps}")
    
    # Recommendations based on fundamental analysis
    st.write("### Recommendation")
    if pe_ratio != "N/A" and pe_ratio < 15:
        recommendation = "Buy"
        description = "Undervalued"
    elif pe_ratio != "N/A" and pe_ratio > 25:
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
    
    # Plot closing price with SMA and MACD
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Close Price"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_50'], mode='lines', name="SMA 50"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_200'], mode='lines', name="SMA 200"))
    fig.update_layout(title="Close Price with SMA 50 and 200", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI
    st.write("### RSI (20)")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], mode='lines', name="RSI"))
    fig_rsi.update_layout(title="RSI (20)", template="plotly_dark")
    st.plotly_chart(fig_rsi, use_container_width=True)
    
    # MACD
    st.write("### MACD")
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], mode='lines', name="MACD"))
    fig_macd.update_layout(title="MACD", template="plotly_dark")
    st.plotly_chart(fig_macd, use_container_width=True)
    
    # 4. Prediction Model
    st.header("Prediction Model")
    stock_data['Target'] = np.where(stock_data['Close'].shift(-1) > stock_data['Close'], 1, 0)
    
    # Use relevant features for prediction
    features = stock_data[['SMA_50', 'SMA_200', 'RSI', 'MACD']].dropna()
    target = stock_data['Target'].dropna()
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    
    st.write(f"Prediction Model Accuracy: {accuracy:.2%}")
    st.write("Use the model predictions for additional insights into stock behavior.")

if __name__ == "__main__":
    main()
