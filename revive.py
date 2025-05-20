# Import necessary libraries
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
import customtkinter as CTk
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mplfinance as mpf
import pandas as pd

# Create main application window
root = CTk.CTk()
root.title('Main')
root.geometry("800x600")
def candle_window():
    candle_window(master=candlestick_frame, width=800, height=400)


    if candlestick_frame:
            for widget in candlestick_frame.winfo_children():
                widget.destroy()

            # Download data
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
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=100, shuffle=False)

            # Model Training
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Model Prediction
            predictions = model.predict(X_test)

            # Model Evaluation
            mse = mean_squared_error(y_test, predictions)
            print(f"Mean Squared Error: {mse:.2f}")

            # After analysis, display line chart
            fig, ax = plt.plot.bar(figsize=(8, 5))
            ax(y_test.index, y_test, label='Actual Price', color='b')
            ax(y_test.index, predictions, label='Predicted Price', color='r')
            ax.set_title(f'{ticker} Stock Price Prediction')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()

            # Convert columns to numeric (floats)
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')

            # Drop rows with NaN values that result from conversion
            data.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)

            # Set index to datetime (already done), but reassert
            data.index = pd.to_datetime(data.index)

            # Plot candlestick with mplfinance
            fig, axlist = mpf.plot(data, type='candle', style='charles', returnfig=True, volume=False)

def open_graph_window(fig):
    slave = CTk.CTkToplevel()
    slave.title('Bar')
    slave.geometry("100%x100%")   # Make the window responsive
    back_btn = CTk.CTkButton(slave, text="Back", command=slave.destroy)
    back_btn.pack(pady=10)

    if slave:
        # Embed the provided figure
        canvas = FigureCanvasTkAgg(fig, master=slave)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



# Define error window
def error_window():
    error = CTk.CTkToplevel()
    error.title('Error')
    error.geometry("300x150")  # Smaller size for error
    message = CTk.CTkLabel(error, text="An error occurred:\nPlease enter a ticker symbol.")
    message.pack(pady=20)
    back_btn = CTk.CTkButton(error, text="Back", command=error.destroy)
    back_btn.pack(pady=10)


def graphic_window():
    ticker = ticker_entry.get()
    if not ticker:
        error_window()
        return
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=100, shuffle=False)

    # Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model Prediction
    predictions = model.predict(X_test)

    # Model Evaluation
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse:.2f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(y_test.index, y_test, label='Actual Price', color='b')
    ax.plot(y_test.index, predictions, label='Predicted Price', color='r')
    ax.set_title(f'{ticker} Stock Price Prediction')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

    open_graph_window(fig)

    # error window
    


def on_search():
    ticker = ticker_entry.get()
    if not ticker:
        error_window()
        return
    # Show candlestick in main window or separate window
    # show_candlestick(root)

    


# Create main frame and graph frame

main_frame = CTk.CTkFrame(root)
main_frame.pack(pady=20, expand=True)
analyze_button = CTk.CTkButton(main_frame, text="Analyze Stock Data", command=graphic_window)
analyze_button.pack(pady=10)
review_button = CTk.CTkButton(main_frame, text="Review", command=candle_window)
review_button.pack(pady=0)
clear_button = CTk.CTkButton(main_frame, text="Clear Graph", command=lambda: graph_frame.destroy())
clear_button.pack(pady=10)
exit_button = CTk.CTkButton(main_frame, text="Exit", command=root.destroy)
exit_button.pack(pady=10, padx=0)

# Initialize data variable
data = None


def show_candlestick_in_main(ticker):
    global candlestick_frame
    try:
        # Clear previous content
        for widget in candlestick_frame.winfo_children():
            widget.destroy()

        # Download data
        data = yf.download(ticker, period='30d')
        if data.empty:
            error_window()
            return

        # Convert columns to numeric (floats)
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

        # Drop rows with NaN values that result from conversion
        data.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)

        # Set index to datetime (already done), but reassert
        data.index = pd.to_datetime(data.index)

        # Plot candlestick with mplfinance
        fig, axlist = mpf.plot(data, type='candle', style='charles', returnfig=True, volume=False)
        show_candlestick_in_main(root, fig)
        # Embed figure
        # canvas = FigureCanvasTkAgg(fig, master=candlestick_frame, width=800, height=400)
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas.draw()
    except Exception as e:
        print(f"Error in show_candlestick_in_main: {e}")
        error_window()

graph_frame = CTk.CTkFrame(root)
graph_frame.pack(fill="both", expand=True, pady=10)
candlestick_frame = CTk.CTkFrame(root)
candlestick_frame.pack(fill="both", expand=True, pady=10)
# Step 2: Create a user interface for the application
# Create input field for ticker symbol
ticker_label = CTk.CTkLabel(main_frame, text="Enter Stock Ticker:")
ticker_label.pack(pady=5)
ticker_entry = CTk.CTkEntry(main_frame)
ticker_entry.pack(pady=5)
ticker_entry.insert(0, '')  # Fixed the f-string syntax error

# Create date range inputs
date_frame = CTk.CTkFrame(main_frame)
date_frame.pack(pady=5, fill="x")

# Calculate default dates
end_date = datetime.now()
start_date = end_date - timedelta(days=365)  # Default to 1 year of data

default_start = start_date.strftime("%Y-%m-%d")
default_end = end_date.strftime("%Y-%m-%d")

start_label = CTk.CTkLabel(main_frame, text="Start Date:")
start_label.pack(side="left", padx=5)
start_entry = CTk.CTkEntry(main_frame)
start_entry.pack(side="left", padx=5)
start_entry.insert(0, default_start)

end_label = CTk.CTkLabel(main_frame, text="End Date:")
end_label.pack(side="left", padx=5)
end_entry = CTk.CTkEntry(main_frame)
end_entry.pack(side="left", padx=5)
end_entry.insert(1, default_end)


# Run the main application loop
root.mainloop()