#!/usr/bin/env python3.12
# Import necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as CTk
from datetime import datetime, timedelta

# Create main application window
root = CTk.CTk()
root.title('Anal Rider')
root.geometry("800x600")


def open_graph_window():
    slave = CTk.CTkToplevel()
    slave.title('Graph')
    slave.geometry("800x600")
    back_btn = CTk.CTkButton(slave, text="Back", command=slave.destroy)
    back_btn.pack(pady=10)

# Step 1: Define the data analysis function
def analyze_stock_data():
    ticker = ticker_entry.get()
    if not ticker_entry.get():
        raise ValueError("requires ticker symbol")
    else:
        start_date = start_entry.get()
        end_date = end_entry.get()
    data = yf.download(ticker, start=start_date, end=end_date)
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
analyze_button = CTk.CTkButton(main_frame, text="Analyze Stock Data", command=analyze_stock_data)
analyze_button.pack(pady=10)

graph_frame = CTk.CTkFrame(root)
graph_frame.pack(fill="both", expand=True, pady=10)
clear_button = CTk.CTkButton(main_frame, text="Clear Graph", command=lambda: graph_frame.winfo_children()[0].destroy())
clear_button.pack(pady=10)
# Step 2: Create a user interface for the application
# Create input field for ticker symbol
ticker_label = CTk.CTkLabel(main_frame, text="Enter Stock Ticker:")
ticker_label.pack(pady=5)
ticker_entry = CTk.CTkEntry(main_frame)
ticker_entry.pack(pady=5)
ticker_entry.insert(0, '')  # Fixed the f-string syntax error

# Create date range inputs
date_frame = CTk.CTkFrame(main_frame)
date_frame.pack(pady=5)

# Calculate default dates
end_date = datetime.now()
start_date = end_date - timedelta(days=365)  # Default to 1 year of data
default_start = start_date.strftime("%Y-%m-%d")
default_end = end_date.strftime("%Y-%m-%d")

start_label = CTk.CTkLabel(date_frame, text="Start Date:")
start_label.pack(side="left", padx=5)
start_entry = CTk.CTkEntry(date_frame)
start_entry.pack(side="left", padx=5)
start_entry.insert(0, default_start)

end_label = CTk.CTkLabel(date_frame, text="End Date:")
end_label.pack(side="left", padx=5)
end_entry = CTk.CTkEntry(date_frame)
end_entry.pack(side="left", padx=5)
end_entry.insert(0, default_end)


# Run the main application loop
root.mainloop()