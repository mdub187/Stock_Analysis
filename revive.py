from __imports__ import CTk, LnR, fcta, timedelta, datetime, plt, yf, mpf, mse, tts
def run_main_app():
    root = CTk.CTk()
    root.title('StockerStockerson')
    root.geometry("800x600")

    def candle_window():
        if candlestick_frame:
            for widget in candlestick_frame.winfo_children():
                widget.destroy()

            start_date = start_entry.get()
            end_date = end_entry.get()
            data = yf.download(ticker_entry.get(), start=start_date, end=end_date)
            data = data[['Close']]
            data['MA5'] = data['Close'].rolling(window=5).mean()
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['Volatility'] = data['Close'].rolling(window=20).std()
            data = data.dropna()
            data['Target'] = data['Close'].shift(-1)
            data = data.dropna()

            X = data[['Close', 'MA5', 'MA20', 'Volatility']]
            y = data['Target']
            X_train, X_test, y_train, y_test = tts(X, y, test_size=100, shuffle=False)

            model = LnR()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse(y_test, predictions)
            print(f"Mean Squared Error: {mse:.2f}")

            mpf.plot(data, type='candle', style='charles', volume=False)

    def open_graph_window(fig):
        slave = CTk.CTkToplevel()
        slave.title('Bar')
        slave.geometry("1000x600")
        CTk.CTkButton(slave, text="Back", command=slave.destroy).pack(pady=10)

        canvas = fcta(fig, master=slave)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def error_window():
        error = CTk.CTkToplevel()
        error.title('Error')
        error.geometry("300x150")
        CTk.CTkLabel(error, text="An error occurred:\nPlease enter a ticker symbol.").pack(pady=20)
        CTk.CTkButton(error, text="Back", command=error.destroy).pack(pady=10)

    def graphic_window():
        ticker = ticker_entry.get()
        if not ticker:
            error_window()
            return

        start_date = start_entry.get()
        end_date = end_entry.get()
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data[['Close']]
        data['MA5'] = data['Close'].rolling(window=5).mean()
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['Volatility'] = data['Close'].rolling(window=20).std()
        data = data.dropna()
        data['Target'] = data['Close'].shift(-1)
        data = data.dropna()

        X = data[['Close', 'MA5', 'MA20', 'Volatility']]
        y = data['Target']
        X_train, X_test, y_train, y_test = tts(X, y, test_size=100, shuffle=False)

        model = LnR()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mse(y_test, predictions)
        print(f"Mean Squared Error: {mse:.2f}")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(y_test.index, y_test, label='Actual Price', color='b')
        ax.plot(y_test.index, predictions, label='Predicted Price', color='r')
        ax.set_title(f'{ticker} Stock Price Prediction')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        open_graph_window(fig)

    main_frame = CTk.CTkFrame(root)
    main_frame.pack(pady=20, expand=True)

    CTk.CTkButton(main_frame, text="Analyze Stock Data", command=graphic_window).pack(pady=10)
    CTk.CTkButton(main_frame, text="Review", command=candle_window).pack()
    CTk.CTkButton(main_frame, text="Exit", command=root.destroy).pack(pady=10)

    CTk.CTkLabel(main_frame, text="Enter Stock Ticker:").pack(pady=5)
    global ticker_entry
    ticker_entry = CTk.CTkEntry(main_frame)
    ticker_entry.pack(pady=5)

    date_frame = CTk.CTkFrame(main_frame)
    date_frame.pack(pady=5, fill="x")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    default_start = start_date.strftime("%Y-%m-%d")
    default_end = end_date.strftime("%Y-%m-%d")

    global start_entry, end_entry
    CTk.CTkLabel(main_frame, text="Start Date:").pack(side="left", padx=5)
    start_entry = CTk.CTkEntry(main_frame)
    start_entry.pack(side="left", padx=5)
    start_entry.insert(0, default_start)

    CTk.CTkLabel(main_frame, text="End Date:").pack(side="left", padx=5)
    end_entry = CTk.CTkEntry(main_frame)
    end_entry.pack(side="left", padx=5)
    end_entry.insert(0, default_end)

    global graph_frame, candlestick_frame
    graph_frame = CTk.CTkFrame(root)
    graph_frame.pack(fill="both", expand=True, pady=10)

    candlestick_frame = CTk.CTkFrame(root)
    candlestick_frame.pack(fill="both", expand=True, pady=10)

    root.mainloop()


# Nothing runs on import
if __name__ == "__main__":
    run_main_app()
