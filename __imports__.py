# __imprts__.py
#
import matplotlib as mtp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fcta
from sklearn.linear_model import LinearRegression as LnR
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split as tts
import mplfinance as mpf
import yfinance as yf
import customtkinter as CTk
import pandas as pd
import bcrypt as bcr


# revive imports
from datetime import datetime, timedelta

if __name__ == "__main__":
    print("home")
