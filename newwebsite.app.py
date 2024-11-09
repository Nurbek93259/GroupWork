import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Load stock price data (assuming it's available as a CSV)
# data = pd.read_csv("stock_data.csv")

# Sample data for demonstration (comment out if loading actual data)
np.random.seed(0)
dates = pd.date_range("2022-01-01", periods=500)
prices = np.cumsum(np.random.randn(500)) + 100  # simulated prices
data = pd.DataFrame({"Date": dates, "Close": prices})

# Step 1: Calculate Moving Averages
data["50_MA"] = data["Close"].rolling(window=50).mean()
data["200_MA"] = data["Close"].rolling(window=200).mean()

# Step 2: Identify Golden Crosses
data["Golden_Cross"] = ((data["50_MA"].shift(1) < data["200_MA"].shift(1)) &
                        (data["50_MA"] >= data["200_MA"])).astype(int)

# Step 3: Feature Engineering
data["MA_Diff"] = data["50_MA"] - data["200_MA"]
data["Momentum"] = data["Close"].pct_change(periods=5)

# Drop rows with NaN values from moving averages
data.dropna(inplace=True)

# Step 4: Prepare Data for Modeling
X = data[["50_MA", "200_MA", "MA_Diff", "Momentum"]]
y = data["Golden_Cross"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Step 6: Visualization of Predictions and Golden Crosses
data["Pred_Golden_Cross"] = model.predict(X)  # Predict on the full dataset for visualization

# Plotting the Golden Cross Predictions
plt.figure(figsize=(14, 7))
plt.plot(data["Date"], data["Close"], label="Close Price")
plt.plot(data["Date"], data["50_MA"], label="50-Day MA", linestyle="--")
plt.plot(data["Date"], data["200_MA"], label="200-Day MA", linestyle="--")

# Highlight actual Golden Crosses
golden_crosses = data[data["Golden_Cross"] == 1]
plt.scatter(golden_crosses["Date"], golden_crosses["Close"], color="green", label="Actual Golden Cross", s=50)

# Highlight predicted Golden Crosses
predicted_crosses = data[data["Pred_Golden_Cross"] == 1]
plt.scatter(predicted_crosses["Date"], predicted_crosses["Close"], color="orange", label="Predicted Golden Cross", s=50, marker='x')

plt.legend()
plt.title("Golden Cross Prediction Model")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
