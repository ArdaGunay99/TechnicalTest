import unittest
from var import VaR
import pandas as pd


class TestVaR(unittest.TestCase):
    """
    This class tests the functionality of the VaR class.
    """


    def setUp(self):
        """
        Initializes an instance of VaR class with the spot price from the FX portfolio.
        """

        self.var = VaR(153084.81, 95891.51)

    def test_import(self):
        """
        testing if the imported market rates are correct
        """
        # importing the market rates
        market_rates = pd.read_excel("FX portfolio data.xlsx", sheet_name="VaR Calculation", skiprows=[0],
                                     usecols="F,G",header=4, names=["ccy1","ccy2"])

        # dropping the last row which is empty
        market_rates.drop(market_rates.tail(1).index,inplace=True)

        # converting columns from the market rates to lists for assertion
        ccy1 = market_rates["ccy1"].to_list()
        ccy2 = market_rates["ccy2"].to_list()

        # converting columns from the var.data to lists for assertion
        var_ccy1 = self.var.data["ccy1"].to_list()
        var_ccy2 = self.var.data["ccy2"].to_list()

        self.assertEqual(ccy1, var_ccy1)
        self.assertEqual(ccy2, var_ccy2)

    def test_spot_price(self):
        """
        testing if the spot prices are correctly assigned
        """
        self.assertEqual(self.var.spot_price_ccy1,153084.81)
        self.assertEqual(self.var.spot_price_ccy2,95891.51)

    def test_var_calculation(self):
        """
        testing if var is calculated correctly.
        """
        self.assertEqual(self.var.calculate_one_day_var(),-13572.733792468436) # 1-day VaR value from the original Excel spreadsheet

if __name__ == '__main__':
    unittest.main()
