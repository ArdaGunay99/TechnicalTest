from var import VaR
import numpy as np

"""
This script uses the VaR class to calculate the 1-day VaR value with 0.99 confidence level, with respect to the given 
spot prices of the currencies in the FX portfolio. Then, it exports the calculated 1-day shifts and P&L vectors as well
as the original market rates as an Excel spreadsheet.
"""


if __name__ == '__main__':
    # initializing a VaR object with the spot prices of the FX portfolio
    var = VaR(153084.81, 95891.51)
    # calculating and printing the 1-day VaR value with .99 confidence level
    print("1-day VaR value for the FX portfolio:", var.calculate_one_day_var())
    #exporting the dataFrame that has the market rates, 1-day shifts, and P&L vectors as an Excel spreadsheet.
    var.data.to_excel('VaR.xlsx')
