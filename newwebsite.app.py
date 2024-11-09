import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Title and Introduction
st.title("Stock Portfolio & Company Analysis Dashboard")
st.write("Analyze your portfolio or choose a company to view its financial metrics and performance.")

# Option for User to Select Mode: Portfolio Analysis or Single Company Analysis
mode = st.sidebar.radio("Select Mode", ("Portfolio Analysis", "Company Analysis"))

# Portfolio Analysis Section
if mode == "Portfolio Analysis":
    # Portfolio Data Upload
    uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"])
    if uploaded_file:
        portfolio_df = pd.read_csv(uploaded_file)
        st.write("### Portfolio Overview", portfolio_df)

        # List tickers in the portfolio
        tickers = portfolio_df['Ticker'].tolist()
        
        # Download stock data
        data = yf.download(tickers, period="1y")  # Example: Get data for the past year

        # Example Visualization: Sector Allocation
        if 'Sector' in portfolio_df.columns:
            st.write("### Sector Allocation")
            sector_counts = portfolio_df['Sector'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%')
            st.pyplot(fig)

        # Performance Line Graph
        st.write("### Portfolio Performance")
        portfolio_performance = data['Adj Close'].sum(axis=1)  # Sum of Adjusted Close Prices as a simple proxy
        st.line_chart(portfolio_performance)

        # Key Metrics for Each Stock
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            st.write(f"#### {ticker} - {info['shortName']}")
            st.metric("Price", f"${info['currentPrice']}")
            st.metric("P/E Ratio", info.get('trailingPE', 'N/A'))
            st.metric("Dividend Yield", info.get('dividendYield', 'N/A'))

# Company Analysis Section
elif mode == "Company Analysis":
    st.write("### Company Analysis")
    # Company selection with text input for ticker
    company_ticker = st.text_input("Enter a company ticker (e.g., AAPL for Apple Inc.)")
    if company_ticker:
        stock = yf.Ticker(company_ticker)
        
        # Fetch and display basic company info
        info = stock.info
        st.write(f"## {info.get('longName', company_ticker)}")
        
        # Key Financial Metrics
        st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        st.metric("P/E Ratio", info.get('trailingPE', 'N/A'))
        st.metric("Market Cap", f"${info.get('marketCap', 'N/A')}")
        st.metric("Dividend Yield", info.get('dividendYield', 'N/A'))

        # Performance Graph (Historical Prices)
        st.write("### Stock Price Performance")
        historical_data = stock.history(period="1y")  # 1 year of historical data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data['Close'], mode='lines', name='Close Price'))
        st.plotly_chart(fig)

        # Additional Information
        st.write("### Company Description")
        st.write(info.get('longBusinessSummary', 'Description not available.'))
