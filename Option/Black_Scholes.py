import numpy as np
from scipy.stats import norm
import datetime


class BlackScholes:
    """
    This class implements the Black-Scholes model for financial option pricing.
    It provides functions to calculate call and put option prices, using spot price method and forward price method.

    """

    def __init__(self, trade_date: datetime.date, expiration_date: datetime.date, spot_price: float, strike_price: float, interest_rate: float, volatility: float):
        """
        Initializes a Black-Scholes model with given parameters.
        Automatically calculates the time to expiration (in years) and forward price.

        :param trade_date: start date of the trade in DD/MM/YYYY format
        :type trade_date: date
        :param expiration_date: expiration date of the option in DD/MM/YYYY format
        :type expiration_date: date
        :param spot_price: current price of the underlying asset
        :type spot_price: float
        :param strike_price: price at which the option can be exercised
        :type strike_price: float
        :param interest_rate: Risk-free interest rate (annualized percentage)
        :type interest_rate: float
        :param volatility: Volatility of the underlying asset (annualized standard deviation of returns).
        :type volatility: float
        """
        self.trade_date = trade_date
        self.expiration_date = expiration_date
        self.time_to_expiration = (self.expiration_date - self.trade_date) / datetime.timedelta(days=365) # calculating time to expire in years
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate/100 # converting interest rate from percentage to decimal value
        self.volatility = volatility
        self.forward_price = self.spot_price * np.exp(self.interest_rate * self.time_to_expiration) # calculating forward price of the asset


    def calculation_with_spot_price(self):
        """
        Calculates the call and put option prices using the spot price of the asset.

        :return: call and put option prices
        :rtype: tuple(float, float)
        """
        d1 = (np.log(self.spot_price/self.strike_price) + (self.interest_rate + (self.volatility**2)/2)*self.time_to_expiration) / (self.volatility * np.sqrt(self.time_to_expiration))
        d2 = d1 - (self.volatility * np.sqrt(self.time_to_expiration))

        call_price = (self.spot_price * norm.cdf(d1)) - (self.strike_price * np.exp(-self.interest_rate*self.time_to_expiration) * norm.cdf(d2))
        put_price = (self.strike_price * np.exp(-self.interest_rate*self.time_to_expiration) * norm.cdf(-d2)) - (self.spot_price * norm.cdf(-d1))

        return call_price, put_price

    def calculation_with_forward_price(self):
        """
        Calculates the call and put option prices using the forward price of the asset.

        :return: call and put option prices
        :rtype: tuple(float, float)
        """
        d1 = (np.log(self.forward_price/self.strike_price) + (self.interest_rate + (self.volatility**2)/2)*self.time_to_expiration) / (self.volatility * np.sqrt(self.time_to_expiration))
        d2 = d1 - (self.volatility * np.sqrt(self.time_to_expiration))

        call_price = np.exp(-self.interest_rate*self.time_to_expiration) * (self.forward_price * norm.cdf(d1) - self.strike_price * norm.cdf(d2))
        put_price =  np.exp(-self.interest_rate*self.time_to_expiration) * (self.strike_price * norm.cdf(-d2) - self.forward_price * norm.cdf(-d1))

        return call_price, put_price





