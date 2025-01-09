# Import necessary libraries
from tkinter import Pack
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as CTk

# Create main application window
root = CTk.CTk()
root.title('Anal Rider')
root.geometry("800x600")

# Step 1: Define the data analysis function
def analyze_stock_data():
    ticker = "AAPL"
    data = yf.download(ticker, start="2015-01-01", end="2023-01-01")
    data = data[['Close']]  # Use 'Close' price for simplicity

    # Data Preprocessing
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['Volatility'] = data['Close'].rolling(window=20).std()
    data = data.dropna()

    # Define Features and Target
    data['Target'] = data['Close'].shift(-1)
    data = data.dropna()

    X = data[['Close', 'MA5', 'MA20', 'Volatility']]
    y = data['Target']

    # Split Data into Training and Testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model Prediction
    predictions = model.predict(X_test)

    # Model Evaluation
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse:.2f}")

    # Plot Actual vs Predicted
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(y_test.index, y_test, label='Actual Price', color='b')
    ax.plot(y_test.index, predictions, label='Predicted Price', color='r')
    ax.set_title(f'{ticker} Stock Price Prediction')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

    # Embed the plot in the customtkinter frame
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)  # Embed figure in `graph_frame`
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Create main frame and graph frame
main_frame = CTk.CTkFrame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

graph_frame = CTk.CTkFrame(main_frame)
graph_frame.pack(fill="both", expand=True, pady=10)

# Add an analyze button to trigger stock analysis
analyze_button = CTk.CTkButton(main_frame, text="Analyze Stock Data", command=analyze_stock_data)
analyze_button.pack(pady=10)

# Run the main application loop
root.mainloop()
