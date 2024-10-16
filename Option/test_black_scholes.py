import unittest
import datetime
import random
from Black_Scholes import BlackScholes

class TestBlackScholes(unittest.TestCase):
    """
    This class tests the Black-Scholes model for in the money, out of money, and at the money
    situations. Every situation is tested 100 times with randomly generated spot and strike prices, using both
    the spot price method and the forward price method.

    """

    def calculate_option_prices(self, spot: float, strike: float, r: float, sigma: float, trade_date: datetime.date, expiration_date: datetime.date, method: str) -> tuple:
        """
        helper function to calculate option prices.
        Initializes a Black-Scholes model and calculates option prices with respect to
        the requested method.

        :param spot: spot price of the asset.
        :type spot: float
        :param strike: strike price of the asset.
        :type strike: float
        :param r: risk-free interest rate.
        :type r: float
        :param sigma: volatility of the asset.
        :type sigma: float
        :param trade_date: start date of the trade in DD/MM/YYYY format
        :type trade_date: date
        :param expiration_date: expiration date of the option in DD/MM/YYYY format
        :type expiration_date: date
        :param method: calculation method. It can either be spot or forward.
        :type method: str
        :return: call and put option prices
        :rtype: tuple(float, float)
        """
        # initializing black-scholes model
        black_scholes = BlackScholes(trade_date,expiration_date,spot, strike, r, sigma)
        # calculating the call and put option prices with respect to the requested method
        if method == "spot":
            call_price, put_price = black_scholes.calculation_with_spot_price()
        elif method == "forward":
            call_price, put_price = black_scholes.calculation_with_forward_price()
        else:
            return None

        return call_price, put_price

    def test_in_the_money(self):
        """
        Test case where spot price is higher than the strike price (In-the-money)

        """
        r = 0.5  # interest rate
        sigma = 0.3  # volatility
        trade_date = datetime.date.today()
        expiration_date = trade_date + datetime.timedelta(days=100)  # expiration in 100 days

        # test for 100 random values
        for i in range(100):
            strike = random.uniform(0.1,1000)  # random strike price
            spot = strike + random.uniform(0.1, 1000)  # random spot price (higher than strike)

            # calculate with spot price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date,"spot")

            # Check that the call price is non-zero (in-the-money for call option)
            self.assertGreater(call_price, 0, "Call option should be in the money.")
            self.assertLess(put_price, strike, "Put option should be out of the money.")

            # calculate with forward price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date,"forward")

            # Check that the call price is non-zero (in-the-money for call option)
            self.assertGreater(call_price, 0, "Call option should be in the money.")
            self.assertLess(put_price, strike, "Put option should be out of money.")


    def test_out_of_money(self):
        """
        Test case where spot price is lower than the strike price (Out-of-money)

        """
        r = 0.5  # interest rate
        sigma = 0.3  # volatility
        trade_date = datetime.date.today()
        expiration_date = trade_date + datetime.timedelta(days=100)  # expiration in 100 days

        # test for 100 random values
        for i in range(100):
            spot =  random.uniform(0.1,1000) # spot price
            strike = spot + random.uniform(0.1,1000)  # strike price (higher than spot)

            # calculate with spot price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date, "spot")

            # checking that the call price is close to zero (out-of-the-money for call option)
            self.assertLess(call_price, strike, "Call option should be out of money.")
            self.assertGreater(put_price, 0, "Put option should be in the money.")

            # calculate with forward price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date,"forward")

            # checking that the call price is close to zero (out-of-the-money for call option)
            self.assertLess(call_price, strike, "Call option should be out of money.")
            self.assertGreater(put_price, 0, "Put option should be in the money.")

    def test_at_the_money(self):
        """
        Test case where spot price equals strike price (At-the-money)

        """
        r = 0.5  # interest rate
        sigma = 0.3  # volatility
        trade_date = datetime.date.today()
        expiration_date = trade_date + datetime.timedelta(days=100)  # expiration in 100 days

        # test for 100 random values
        for i in range(100):
            spot = random.uniform(0.1,1000)  # spot price
            strike = spot  # strike price (equal to spot)

            # calculate with spot price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date, "spot")

            # checking that the call and put prices are reasonable for an at-the-money option
            self.assertGreater(call_price, 0, "Call option should have a non-zero value at the money.")
            self.assertGreater(put_price, 0, "Put option should have a non-zero value at the money.")

            # calculate with forward price
            call_price, put_price = self.calculate_option_prices(spot, strike, r, sigma, trade_date, expiration_date,"forward")

            # checking that the call and put prices are reasonable for an at-the-money option
            self.assertGreater(call_price, 0, "Call option should have a non-zero value at the money.")
            self.assertGreater(put_price, 0, "Put option should have a non-zero value at the money.")

# running the test. Every function starting with test_ will run automatically.
if __name__ == '__main__':
    unittest.main()
