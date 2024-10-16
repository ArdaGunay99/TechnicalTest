#%%
import pandas as pd
import numpy as np

class VaR:
    """
    This class is specifically designed to calculate the 1-day VaR value of the FX portfolio of the bank.
    It uses the spot prices and the historical market rate data of the currencies in the portfolio.
    When an instance of this class is initialized with the spot prices of the currencies in the portfolio,
    it automatically imports the historical market rate data, calculates the 1-day shift and P&L vectors, and the total
    P&L. After initialization, calculate_one_day_var() function can be called to calculate the 1-day VaR.

    """
    
    def __init__(self, spot_price_ccy1: float, spot_price_ccy2: float):
        """
        Constructor for VaR class. Imports data, calculates 1-day shift and P&L vectors 
        as well as the total P&L vector. Adds the calculated vectors to the original dataframe.

        :param spot_price_ccy1: spot portfolio value for currency 1
        :type spot_price_ccy1: float
        :param spot_price_ccy2: spot portfolio value for currency 2
        :type spot_price_ccy2: float
        """
        self.spot_price_ccy1 = spot_price_ccy1
        self.spot_price_ccy2 = spot_price_ccy2
        
        # initializing 1-day shift columns
        self.one_day_shift_ccy1 = np.array([])
        self.one_day_shift_ccy2 = np.array([])
        
        # initializing PnL vector columns
        self.pnl_ccy1 = np.array([])
        self.pnl_ccy2 = np.array([])
        self.pnl_sum = np.array([])
        
        # importing data
        self.data = self.import_data()
        
        # calculating 1-day shift
        self.calculate_one_day_shift()
        
        # calculating P&L vectors
        self.calculate_pnl_vectors()
        
        # calculating total P&L
        self.calculate_pnl_sum()
        
        # adding the calculated values to the dataframe as new columns
        self.fill_data_frame()
        
    def import_data(self):
        """
        imports data from excel file as a pandas dataframe.
        :return: data in dataframe 
        :rtype: DataFrame
        """
        # reading Excel file
        data = pd.read_excel("FX portfolio data.xlsx", sheet_name="VaR Calculation", skiprows=[0], usecols="D:G",
                             header=4, names=["date","portfolio","ccy1","ccy2"])
        # dropping the last row which is empty
        data.drop(data.tail(1).index, inplace=True)

        return data
    
    def calculate_one_day_shift(self):
        """
        Calculates 1-day shift for the FX portfolio.
        
        """
        # looping until the last data point
        for i in range(len(self.data.index)-1):
            self.one_day_shift_ccy1 = np.append(self.one_day_shift_ccy1, np.exp(np.log(self.data.iat[i,2]/self.data.iat[i+1,2]))-1)
            self.one_day_shift_ccy2 = np.append(self.one_day_shift_ccy2, np.exp(np.log(self.data.iat[i,3]/self.data.iat[i+1,3]))-1)
            
        
    
    def calculate_pnl_vectors(self):
        """
        Calculates P&L vectors for the FX portfolio.

        """
        for i in range(len(self.data.index)-1):
            self.pnl_ccy1 = np.append(self.pnl_ccy1, self.one_day_shift_ccy1[i] * self.spot_price_ccy1)
            self.pnl_ccy2 = np.append(self.pnl_ccy2, self.one_day_shift_ccy2[i] * self.spot_price_ccy2)
    
    def calculate_pnl_sum(self):
        """
        Calculates P&L sum for the FX portfolio.

        """
        self.pnl_sum = np.add(self.pnl_ccy1, self.pnl_ccy2)
        
    def fill_data_frame(self):
        """
        Generates new columns from 1-day shift, P&L vectors, and P&L sum and adds them to the original DataFrame.
        
        """
        # converting 1-day shift arrays to pandas series
        one_day_shift_ccy1_column = pd.Series(self.one_day_shift_ccy1)
        one_day_shift_ccy2_column = pd.Series(self.one_day_shift_ccy2)
        
        # converting P&L arrays to pandas series
        pnl_ccy1_column  = pd.Series(self.pnl_ccy1)
        pnl_ccy2_column  = pd.Series(self.pnl_ccy2)
        pnl_sum_column = pd.Series(self.pnl_sum)
        
        # assigning the converted series to the original DataFrame as new columns
        self.data = self.data.assign(one_day_shift_ccy1=one_day_shift_ccy1_column,
                                     one_day_shift_ccy2=one_day_shift_ccy2_column, pnl_ccy1=pnl_ccy1_column,
                                     pnl_ccy2=pnl_ccy2_column, pnl_sum=pnl_sum_column)
        
    def calculate_one_day_var(self)-> float:
        """
        Calculates 1-day VaR for the FX portfolio with 0.99 confidence level.
        :return: 1-day VaR for the FX portfolio.
        :rtype: float
        """
        one_day_var = 0.4 * self.data.pnl_sum.nsmallest(2).max() + 0.6 * self.data.pnl_sum.nsmallest(3).max()
        return one_day_var
        
        
