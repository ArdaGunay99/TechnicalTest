from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Black_Scholes import BlackScholes

"""
This script creates a GUI application that calculates the call an put option prices of an asset 
using the tkinter library and the Black-Scholes model, inspired from the original Excel spreadsheet.
The application accepts spot price, strike price, risk free interest rate, volatility, trade date, and expiration date
from the user. Then, the user can select the method they want to use for option pricing calculation 
(spot price or forward). The calculations are done using the BlackScholes class.  
"""

# function to validate entry type
def validate_entry(value):
    """
    function used to validate the entered values to the entry widgets.
    It is called when user presses a key to enter a value to an entry widget.
    Only accepts float values, dot for decimal place, and empty string.

    :param value: value entered by the user
    :type value: str
    :return: whether the entered value is valid
    :rtype: bool
    """
    # checking if the entered value is an empty string or a decimal dot
    if value == "" or value == ".":
        return True
    # checking if the entered value can be converted to float.
    try:
        float(value)
        return True
    except ValueError:
        return False

# function to validate entry type
def validate_entry_negative(value):
    """
    function used to validate the entered values to the entry widgets.
    It is called when user presses a key to enter a value to an entry widget.
    Only accepts float values, dot for decimal place, negative values, and empty string.
    Used to support negative interest rates.

    :param value: value entered by the user
    :type value: str
    :return: whether the entered value is valid
    :rtype: bool
    """
    # checking if the entered value is an empty string or a decimal dot
    if value == "" or value == "." or value == "-":
        return True
    # checking if the entered value can be converted to float.
    try:
        float(value)
        return True
    except ValueError:
        return False

# function to validate dates
def validate_dates(date_picker):
    """
    Validates that the start date is before or at least the same date as expiration date and vice versa.

    :param date_picker: date picker widget to be reset if the entry is invalid
    :type date_picker: DateEntry
    """
    trade_date = trade_date_picker.get_date()
    expiration_date =expiration_date_picker.get_date()

    # Check if start date is before expiration date
    if trade_date > expiration_date:
        messagebox.showerror("Invalid Dates", "The trade date cannot be after the expiration date.")
        # resetting the changed date picker
        if date_picker == trade_date_picker:
            trade_date_picker.set_date(datetime.today()) # reset the start date to current date
        else:
            expiration_date_picker.set_date(trade_date_picker.get_date().replace(year=trade_date_picker.get_date().year+1)) # reset the expiration date to a year after the trade date


def calculate_prices(method):
    """
    Called when a calculate button is pressed. Checks if all the values are entered. If so, initialises
    a Black-Scholes model with the entered values and calculates the call and put option prices with respected to
    the requested calculation method.

    :param method: calculation method. It can be "spot" or "forward"
    :type method: str
    """
    # checking if all the entry boxes are filled
    try:
        spot_price = float(spot_price_entry.get())
        strike_price = float(strike_price_entry.get())
        interest_rate = float(interest_rate_entry.get())
        volatility = float(volatility_entry.get())
        trade_date = trade_date_picker.get_date()
        expiration_date = expiration_date_picker.get_date()
    except ValueError:
        messagebox.showerror("Value Error", "Please make sure to fill all the values.")
        return None


    # creating a Black-Scholes model
    black_scholes = BlackScholes(trade_date, expiration_date, spot_price, strike_price, interest_rate, volatility)

    # calculating the call and put option prices with respect to the requested method
    try:
        if method == "spot":
            call_price, put_price = black_scholes.calculation_with_spot_price()
        elif method == "forward":
            call_price, put_price = black_scholes.calculation_with_forward_price()
        else:
            return None
    # checking for division by zero
    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Division by zero. Please make sure all the prices correct.")
        return None

    #show the price in GUI
    call_price_var.set(f"{call_price:3f}")
    put_price_var.set(f"{put_price:3f}")


# creating the main window
window = tk.Tk()
window.title("Black-Scholes Option Pricing")
window.config(bg="#FF6200")


# creating a frame to contain rest of the widgets
frame = tk.Frame(window, bg="#FF6200")
frame.pack()

# creating validate commands
validate = (frame.register(validate_entry),"%P")
validate_negative = (frame.register(validate_entry_negative),"%P")

# Configure rows and columns of the window to be resizable
window.grid_columnconfigure(0,minsize=10,weight=10, pad=10)
window.grid_columnconfigure(1,minsize=10,weight=10, pad=10)
for i in range(9):
    window.grid_rowconfigure(i,minsize=10,weight=10, pad=10)

# Configure rows and columns of the frame to be resizable
frame.grid_columnconfigure(0,minsize=10,weight=10, pad=10)
frame.grid_columnconfigure(1,minsize=10,weight=10, pad=10)
for i in range(9):
    frame.grid_rowconfigure(i,minsize=10,weight=10, pad=10)

# creating and placing the input fields and labels
ttk.Label(frame, text="Spot Price (S):").grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
spot_price_entry = ttk.Entry(frame, validate="key", validatecommand=validate)
spot_price_entry.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

ttk.Label(frame, text="Strike Price (K):").grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
strike_price_entry = ttk.Entry(frame, validate="key", validatecommand=validate)
strike_price_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

ttk.Label(frame, text="Interest Rate (r%) :").grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
interest_rate_entry = ttk.Entry(frame, validate="key", validatecommand=validate_negative)
interest_rate_entry.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)

ttk.Label(frame, text="Volatility (σ) :").grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
volatility_entry = ttk.Entry(frame, validate="key", validatecommand=validate)
volatility_entry.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)

# initializing Date Pickers
ttk.Label(frame, text="Trade Date:").grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
trade_date_picker = DateEntry(frame, date_pattern="dd/mm/y" , width=12, background='#FF6200', foreground='white', borderwidth=2)
trade_date_picker.grid(row=4, column=1,sticky="nsew", padx=10, pady=5)
trade_date_picker.bind("<<DateEntrySelected>>", lambda e:  validate_dates(trade_date_picker)) # triggering a validation check when a date is selected

ttk.Label(frame, text="Expiration Date:").grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
expiration_date_picker = DateEntry(frame, date_pattern="dd/mm/y" ,year=datetime.now().year+1, width=12, background='#FF6200', foreground='white', borderwidth=2)
expiration_date_picker.grid(row=5, column=1, sticky="nsew", padx=10, pady=5)
expiration_date_picker.bind("<<DateEntrySelected>>", lambda e: validate_dates(expiration_date_picker)) # triggering a validation check when a date is selected

# initializing buttons for spot price and forward price calculation
spot_calculate_button = ttk.Button(frame, text="Calculate With Spot Price", command=lambda: calculate_prices("spot"))
spot_calculate_button.grid(row=6, column=0,sticky="nsew", pady=10)

forward_calculate_button = ttk.Button(frame, text="Calculate With Forward Price", command=lambda: calculate_prices("forward"))
forward_calculate_button.grid(row=6, column=1,sticky="nsew", pady=10)

# creating variables to set output values
call_price_var = tk.StringVar()
put_price_var = tk.StringVar()

# creating output fields for call and put prices
ttk.Label(frame, text="Call Price:").grid(row=7, column=0,sticky="nsew", padx=10, pady=5)
call_price_entry = ttk.Entry(frame, textvariable=call_price_var, state="readonly")
call_price_entry.grid(row=7, column=1,sticky="nsew", padx=10, pady=5)

ttk.Label(frame, text="Put Price:").grid(row=8, column=0,sticky="nsew", padx=10, pady=5)
put_price_entry = ttk.Entry(frame, textvariable=put_price_var, state="readonly")
put_price_entry.grid(row=8, column=1,sticky="nsew", padx=10, pady=5)

# running the main loop
frame.mainloop()