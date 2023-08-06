""" This module provides a public class ``Asset`` that holds and calculates quantities of a single asset.
It is designed to be used for stocks and/or market indices.
"""

import numpy as np
import pandas as pd
from finquant.returns import daily_returns, historical_mean_return


class Asset:
    """Object that contains information about an asset.
    To initialise the object, it requires data, e.g. daily closing prices as a
    ``pandas.Series``, a name as string and a type as string.

    ``data`` is required to contain the closing price, hence it is required to
    contain one column label ``<stock_name> - Adj. Close`` which is used to
    compute the return of investment.
    """

    def __init__(self, data: pd.Series, name: str, asset_type: str) -> None:
        """
        :Input:
         :data: ``pandas.Series`` of asset prices
         :name: Name of the asset
         :asset_type: Type of the asset (e.g., "Stock" or "Market")
        """
        self.name = name
        self.data = data
        self.expected_return = self.comp_expected_return()
        self.volatility = self.comp_volatility()
        self.skew = self._comp_skew()
        self.kurtosis = self._comp_kurtosis()
        self.daily_returns = self.comp_daily_returns()
        self.asset_type = asset_type


    # functions to compute quantities
    def comp_daily_returns(self) -> pd.Series:
        """Computes the daily returns (percentage change) of the asset."""
        return daily_returns(self.data)

    def comp_expected_return(self, freq=252) -> float:
        """Computes the Expected Return of the asset."""
        return historical_mean_return(self.data, freq=freq)

    def comp_volatility(self, freq=252) -> float:
        """Computes the Volatility of the asset."""
        return self.comp_daily_returns().std() * np.sqrt(freq)

    def _comp_skew(self) -> float:
        """Computes and returns the skewness of the asset."""
        return self.data.skew()

    def _comp_kurtosis(self) -> float:
        """Computes and returns the kurtosis of the asset."""
        return self.data.kurt()

    def properties(self):
        """Nicely prints out the properties of the asset."""
        string = "-" * 50
        string += "\nAsset: {}".format(self.name)
        string += "\nExpected Return: {:0.3f}".format(self.expected_return)
        string += "\nVolatility: {:0.3f}".format(self.volatility)
        string += "\nSkewness: {:0.5f}".format(self.skew)
        string += "\nKurtosis: {:0.5f}".format(self.kurtosis)
        string += "\n" + "-" * 50
        print(string)

    def __str__(self):
        string = "Contains information about {}".format(self.name)
        return string