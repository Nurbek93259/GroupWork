import os
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

# Define a valid path for saving the script
script_dir = os.path.join(os.getcwd(), "generated_scripts")
os.makedirs(script_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Technical Analysis Functions
def download_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        st.error(f"Error downloading data: {e}")
        return None

def calculate_moving_averages(data, short_window=50, long_window=200):
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

def calculate_macd(data, short_span=12, long_span=26, signal_span=9):
    data['MACD'] = data['Close'].ewm(span=short_span, adjust=False).mean() - data['Close'].ewm(span=long_span, adjust=False).mean()
    data['Signal_Line'] = data['MACD'].ewm(span=signal_span, adjust=False).mean()

def generate_recommendations(data):
    recommendations = []

    if not data['SMA_short'].isnull().iloc[-1] and not data['SMA_long'].isnull().iloc[-1]:
        if data['SMA_short'].iloc[-1] > data['SMA_long'].iloc[-1]:
            recommendations.append("BUY (SMA indicates upward trend)")
        else:
            recommendations.append("SELL (SMA indicates downward trend)")

    if not data['EMA_short'].isnull().iloc[-1] and not data['EMA_long'].isnull().iloc[-1]:
        if data['EMA_short'].iloc[-1] > data['EMA_long'].iloc[-1]:
            recommendations.append("BUY (EMA indicates upward trend)")
        else:
            recommendations.append("SELL (EMA indicates downward trend)")

    if not data['RSI'].isnull().iloc[-1]:
        if data['RSI'].iloc[-1] < 30:
            recommendations.append("BUY (RSI indicates oversold)")
        elif data['RSI'].iloc[-1] > 70:
            recommendations.append("SELL (RSI indicates overbought)")
        else:
            recommendations.append("HOLD (RSI in normal range)")

    if not data['MACD'].isnull().iloc[-1] and not data['Signal_Line'].isnull().iloc[-1]:
        if data['MACD'].iloc[-1] > data['Signal_Line'].iloc[-1]:
            recommendations.append("BUY (MACD indicates upward momentum)")
        else:
            recommendations.append("SELL (MACD indicates downward momentum)")

    return recommendations

def plot_analysis(data, ticker):
    st.write(f"### Technical Analysis for {ticker}")
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA_short'], label='SMA (50)', color='orange')
    plt.plot(data['SMA_long'], label='SMA (200)', color='green')
    plt.plot(data['EMA_short'], label='EMA (50)', linestyle='--', color='red')
    plt.plot(data['EMA_long'], label='EMA (200)', linestyle='--', color='purple')
    plt.title('Price and Moving Averages')
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(12, 4))
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', color='red', label='Overbought')
    plt.axhline(30, linestyle='--', color='green', label='Oversold')
    plt.title('RSI Indicator')
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(12, 4))
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal_Line'], label='Signal Line', color='orange')
    plt.axhline(0, linestyle='--', color='gray', label='Zero Line')
    plt.title('MACD Indicator')
    plt.legend()
    st.pyplot(plt)

# Sentiment Analysis Functions
def fetch_yahoo_finance_news(ticker):
    base_url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
    response = requests.get(base_url)
    if response.status_code != 200:
        st.error("Failed to fetch news articles.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    news_items = soup.find_all("li", class_="js-stream-content")
    news_data = []

    for item in news_items:
        try:
            headline = item.find("h3").text.strip()
            link = item.find("a")["href"]
            timestamp = item.find("time")["datetime"]
            news_data.append({
                "Headline": headline,
                "Link": "https://finance.yahoo.com" + link if link.startswith("/") else link,
                "Timestamp": timestamp
            })
        except:
            continue

    return news_data

def filter_recent_news(news_data):
    recent_news = []
    current_time = datetime.utcnow()
    for news in news_data:
        news_time = datetime.strptime(news["Timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        if current_time - news_time <= timedelta(hours=72):
            recent_news.append(news)
    return recent_news

def analyze_sentiment(news_data):
    for news in news_data:
        analysis = TextBlob(news["Headline"])
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            news["Sentiment"] = "Positive"
        elif polarity < 0:
            news["Sentiment"] = "Negative"
        else:
            news["Sentiment"] = "Neutral"
    return news_data

# Streamlit UI
st.title("Technical and Sentiment Analysis App")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start Date", datetime(2022, 1, 1))
end_date = st.date_input("End Date", datetime(2023, 1, 1))

if st.button("Perform Analysis"):
    # Technical Analysis
    st.write("### Technical Analysis")
    stock_data = download_data(ticker, start_date, end_date)
    if stock_data is not None:
        calculate_moving_averages(stock_data)
        calculate_rsi(stock_data)
        calculate_macd(stock_data)
        plot_analysis(stock_data, ticker)
        recommendations = generate_recommendations(stock_data)
        st.write("#### Recommendations")
        st.write(recommendations)

    # Sentiment Analysis
    st.write("### Sentiment Analysis")
    news_data = fetch_yahoo_finance_news(ticker)
    if news_data:
        recent_news = filter_recent_news(news_data)
        if recent_news:
            analyzed_news = analyze_sentiment(recent_news)
            df = pd.DataFrame(analyzed_news)
            st.write("#### Sentiment Analysis of Recent News")
            st.dataframe(df[["Headline", "Timestamp", "Sentiment", "Link"]])
        else:
            st.warning("No recent news found.")
    else:
        st.error("Failed to fetch news.")
