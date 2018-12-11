'''
Script to analyze the ITCH data with the information of 96 stocks during a
week in 2016.

The 96 stocks are shown in the list used in main and the week values used are
from the week of the 7 - 11 March, 2016.

For the first proyect I need to obtain the cross response functions between
individual stocks. To compute these values I need to calculate the midpoint
price, the midpoint log returns and the trade signs. Each task is specified
in each function.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''
# -----------------------------------------------------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
from itertools import product
import os

import gzip
import pickle
import multiprocessing as mp

import itch_data_generator

# -----------------------------------------------------------------------------------------------------------------------


def midpoint_plot(ticker, day):
    """
    Plot the midpoint behavior using the price vs time. The data is loaded
    from the mipoint data results.
        :param ticker: String of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: String of the day to be analized (i.e '07')
    """

    # Load data

    print('Processing data for the stock', ticker, 'the day', day +
          ' March, 2016')

    midpoint = pickle.load(open(
        '../Data/midpoint_data/midpoint_201603%s_%s.pickl' % (day, ticker),
        'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Plotting

    plt.title('%s' % ticker, fontsize=40)
    plt.plot(time, midpoint, label=('Day %s' % day))
    plt.xlabel(r'Time $[hour]$', fontsize=25)
    plt.ylabel(r'Price $ [\$] $', fontsize=25)
    plt.legend(loc=0, fontsize=20)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def midpoint_plot_week(ticker, days):
    """
    Plot the midpoint behavior using the price vs time during a time period.
    The data is loaded from the mipoint data results.
        :param ticker: String of the abbreviation of the stock to be analized
        (i.e. 'AAPL')
        :param days: List of the days that will be plotted (i.e ['07', '08',
        '09'])
    """

    print('Plotting the behavior of the stock' + ticker + 'in the week of '
          + days[1] + '-' + days[-1] + 'March, 2016')

    plt.figure(figsize=(16, 9))

    for day in days:
        midpoint_plot(ticker, day)

    plt.tight_layout()
    plt.grid(True)
    plt.savefig('../Data/midpoint_plot/midpoint_plot_%s.png' % ticker)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze
    # tickers = ["AAL", "AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN", "AMAT", "AMGN",
    #            "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB", "BMRN", "CA",  "CELG", "CERN",
    #            "CHKP", "CHRW", "CHTR", "CMCSA", "COST", "CSCO", "CTSH", "CTXS", "DISCA", "DISH",
    #            "DLTR", "EA",  "EBAY", "EQIX", "ESRX", "EXPD", "FAST", "FB",  "FISV", "FOXA",
    #            "GILD", "GOOG", "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "JD",  "KHC",
    #            "KLAC", "LBTYA", "LLTC", "LMCA", "LRCX", "LVNTA", "MAR", "MAT", "MDLZ", "MNST",
    #            "MSFT", "MU",  "MYL", "NFLX", "NTAP", "NVDA", "NXPI", "ORLY", "PAYX", "PCAR",
    #            "PCLN", "QCOM", "REGN", "ROST", "SBAC", "SBUX", "SIRI", "SNDK", "SPLS", "SRCL",
    #            "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP", "VOD", "VRSK",
    #            "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO"]

    days = ['07', '08', '09', '10', '11']

    tickers = ['AAPL', 'MSFT']

    print('Ay vamos!!')

    return None


if __name__ == '__main__':
    main()
