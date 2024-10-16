This project contains solutions for the Option and VaR programming questions in the Engineering
interview technical test. The project uses Python version 3.13.

Solution for the Option question is implemented as a GUI application inspired by the original Excel spreadsheet.
The application accepts spot price, strike price, risk-free interest rate, volatility, trade date, and expiration date
from the user. Then, the user can select the method they want to use for option pricing calculation
(spot price or forward). The calculations are done using the Black-Scholes model implemented in the Black_Scholes.py.
To run the application, you can simply run BlackScholes.exe in Option\dist folder. If you would like to run the code
from the scripts, please make sure to download the module stated in the requirements.txt file. test_black_scholes.py
is a unit test script which tests the program for in-the-money, at-the-money, and out-of-money situations. You can
run the script after downloading the required modules.

Solution for the VaR question consists of a class (VaR) that can import data from Excel and calculate 1-day VaR value
of the given FX portfolio with 0.99 confidence level. It is specifically designed to handle the data from the original
Excel spreadsheet and is not compatible with any other data. main.py script in VaR folder creates an instance of the
VaR class with the given spot prices of the currencies in the portfolio. It then calculates the 1-day VaR value with
historical method and prints it out to terminal. It also exports the dataFrame used in the calculation as an Excel
spreadsheet which contains columns for dates, historical market rates for the currencies, 1-day shift values of the
currencies, P&L vectors, and the total P&L values. test_var.py script runs a unit test for the VaR class to test if
it imports the data correctly, assigns spot prices correctly, and calculates the 1-day VaR value accurately. Values
from the original Excel spreadsheet is used to test the accuracy of the calculations. You can run main.py and
test_var.py as scripts after downloading the required