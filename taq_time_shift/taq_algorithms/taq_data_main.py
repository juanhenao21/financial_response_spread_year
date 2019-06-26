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

    # subprocess.call(['./TAQ_extraction.sh'])

    # taq_data_source(tickers, '2008')

    folder_path = '../../taq_data/pickle_dayly_data_2008/'
    year = '2008'
    # (months,
    #  days) = taq_data_tools.months_days_list(folder_path, tickers[0], year)

    # taq_data_plot_generator(tickers, year)
    # with mp.Pool(processes=mp.cpu_count()) as pool:
    #     pool.starmap(taq_data_plot.taq_self_response_year_avg_plot,
    #                  product(tickers, [year], [months], [days]))
    #     pool.starmap(taq_data_plot.taq_cross_response_year_avg_plot,
    #                  product(tickers, tickers, [year], [months], [days]))
    taq_data_analysis.taq_trade_sign_self_correlator_year_data(tickers[0], year)
    taq_data_analysis.taq_trade_sign_self_correlator_year_data(tickers[1], year)
    taq_data_analysis.taq_trade_sign_cross_correlator_year_data(tickers[0], tickers[1],                                                                  year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
