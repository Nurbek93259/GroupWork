import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data[['Close']]
    stock_data['Date'] = stock_data.index
    return stock_data

# Fetching stock data for a particular stock
ticker = 'AAPL'  # Example: Apple stock
start_date = '2020-01-01'
end_date = '2023-01-01'
data = fetch_stock_data(ticker, start_date, end_date)

# Preparing the data for ML model
data['Day'] = np.arange(len(data))  # Convert date to integer for model input
X = data[['Day']].values
y = data['Close'].values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Create a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Visualizing the results
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label="Actual Price", color='blue')
plt.plot(data['Date'][len(X_train):], y_pred, label="Predicted Price", color='orange')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title(f'{ticker} Stock Price Prediction')
plt.legend()
plt.show()
