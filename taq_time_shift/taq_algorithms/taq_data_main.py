'''
TAQ data main

Script to analyze the TAQ data with the information of 6 stocks during a 2008.

For the first proyect I need to obtain the cross response functions between
individual stocks. To compute these values I need to calculate the midpoint
price, the midpoint log returns and the trade signs. Each task is specified
in each function.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''
# -----------------------------------------------------------------------------
# Modules

from itertools import product
import subprocess

import multiprocessing as mp
import pickle
import pandas as pd

import taq_data_analysis
import taq_data_plot
import taq_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    tickers = ['AAPL', 'MSFT']
    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    year = '2008'

    taus = [1, 10, 100, 1000]

    for ticker in tickers:
        for tau in taus:
            taq_data_analysis.taq_self_response_year_time_shift_data(ticker,
                                                                     year, tau)

    for tau in taus:
        taq_data_analysis.taq_cross_response_year_time_shift_data(ticker_i,
                                                                  ticker_j,
                                                                  year, tau)

    taq_data_plot.taq_cross_response_year_avg_time_shift_plot(ticker_i,
                                                              ticker_j, year,
                                                              taus)

    for ticker in tickers:
        taq_data_plot.taq_self_response_year_avg_time_shift_plot(ticker, year,
                                                                 taus)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
