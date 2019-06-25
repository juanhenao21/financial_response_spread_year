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


def taq_data_source(tickers, year):
    """
    docstring here
        :param tickers:
        :param year:
    """

    date_list = taq_data_tools.taq_bussiness_days('2008')

    # Parallel computing

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(taq_data_analysis.taq_data_extract,
                product(tickers, date_list))

    # for ticker in tickers:
    #     for date in date_list:

    #         try:
    #             date_sep = date.split('-')
    #             month = date_sep[1]
    #             day = date_sep[2]

    #             taq_data_analysis.taq_data_extract(ticker, year,
    #                                                month , day)
    #         except AssertionError:
    #             print('No data')
    #             print()

    return None

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year):
    """
    docstring here
        :param tickers: list of the strings of the abbreviations of the stock
                       to be analized (i.e. ['AAPL', 'MSFT'])
        :param year: string of the year to be analized (i.e '2008')
        :param months: list of the strings of the months to be analized
                       (i.e ['07', '08', '09'])
        :param days: list of lists of the strings of the days to be analized
                    in each month (i.e [['07', '08', '09'], ['01', '02']])
    """

    date_list = taq_data_tools.taq_bussiness_days(year)

    # Basic folders
    # taq_data_tools.taq_start_folders(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Basic functions
        pool.starmap(taq_data_analysis.taq_midpoint_full_time_data,
                        product(tickers, date_list))
        pool.starmap(taq_data_analysis.taq_trade_signs_full_time_data,
                        product(tickers, date_list))

        # Especific functions
        # pool.starmap(taq_data_analysis.taq_self_response_data,
        #                 product(tickers, date_list))
        # pool.starmap(taq_data_analysis.taq_cross_response_data,
        #                 product(tickers, tickers, date_list))
        # pool.starmap(taq_data_analysis.taq_trade_sign_self_correlator_data,
        #              product(tickers, [year], [month],
        #                      days[int(month) - 1]))
        # pool.starmap(taq_data_analysis
        #              .taq_trade_sign_cross_correlator_data,
        #              product(tickers, tickers, [year], [month],
        #                      days[int(month) - 1]))

            # Plot
            # pool.starmap(taq_data_plot.taq_self_response_month_avg_plot,
            #              product(tickers, [year], [month],
            #                      [days[int(month) - 1]]))
            # pool.starmap(taq_data_plot.taq_cross_response_month_avg_plot,
            #              product(tickers, tickers, [year], [month],
            #                      [days[int(month) - 1]]))

        # pool.starmap(taq_data_plot.taq_self_response_year_avg_plot,
        #              product(tickers, [year], [months], [days]))
        # pool.starmap(taq_data_plot.taq_cross_response_year_avg_plot,
        #              product(tickers, tickers, [year], [months], [days]))
        # pool.starmap(taq_data_plot
        #              .taq_trade_sign_self_correlator_year_avg_plot,
        #              product(tickers, [year], [months], [days]))
        # pool.starmap(taq_data_plot
        #              .taq_trade_sign_cross_correlator_year_avg_plot,
        #              product(tickers, tickers, [year], [months], [days]))

    return None

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

    taq_data_plot_generator(tickers, year)
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(taq_data_analysis.taq_self_response_year_data,
                     product(tickers, [year]))
        pool.starmap(taq_data_analysis.taq_cross_response_year_data,
                     product(tickers, tickers, [year]))
        pool.starmap(taq_data_plot.taq_self_response_year_avg_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot.taq_cross_response_year_avg_plot,
                     product(tickers, tickers, [year]))
        pool.starmap(taq_data_plot.taq_trade_sign_self_correlator_year_avg_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot.taq_trade_sign_cross_correlator_year_avg_plot,
                     product(tickers, tickers, [year]))

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
