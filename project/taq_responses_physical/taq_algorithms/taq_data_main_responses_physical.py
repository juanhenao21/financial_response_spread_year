'''TAQ data main module.

The functions in the module run the complete extraction, analysis and plot of
the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * os
    * pandas
    * pickle
    * subprocess
    * taq_data_analysis_responses_physical
    * taq_data_plot_responses_physical
    * taq_data_tools_responses_physical

The module contains the following functions:
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import os
import pandas as pd
import pickle
import subprocess

import taq_data_analysis_responses_physical
import taq_data_plot_responses_physical
import taq_data_tools_responses_physical

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analyzed (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_responses_physical.taq_bussiness_days(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Basic functions
        pool.starmap(taq_data_analysis_responses_physical
                     .taq_midpoint_physical_data,
                     iprod(tickers, date_list))
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Basic functions
        pool.starmap(taq_data_analysis_responses_physical
                     .taq_trade_signs_physical_data,
                     iprod(tickers, date_list))

    # Specific functions
    # Self-response and self-correlator
    for ticker in tickers:

        taq_data_analysis_responses_physical \
            .taq_self_response_year_responses_physical_data(ticker, year)
        taq_data_analysis_responses_physical \
            .taq_trade_sign_self_correlator_year_responses_physical_data(
                ticker, year)

    ticker_prod = iprod(tickers, tickers)
    # ticker_prod = [('AAPL', 'MSFT'), ('MSFT', 'AAPL'),
    #                ('GS', 'JPM'), ('JPM', 'GS'),
    #                ('CVX', 'XOM'), ('XOM', 'CVX'),
    #                ('GOOG', 'MA'), ('MA', 'GOOG'),
    #                ('CME', 'GS'), ('GS', 'CME'),
    #                ('RIG', 'APA'), ('APA', 'RIG')]

    # Cross-response and cross-correlator
    for ticks in ticker_prod:

        taq_data_analysis_responses_physical \
            .taq_cross_response_year_responses_physical_data(ticks[0],
                                                             ticks[1], year)
        taq_data_analysis_responses_physical \
            .taq_trade_sign_cross_correlator_year_responses_physical_data(
                ticks[0], ticks[1], year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_responses_physical
                     .taq_self_response_year_avg_responses_physical_plot,
                     iprod(tickers, [year]))
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_responses_physical
                     .taq_cross_response_year_avg_responses_physical_plot,
                     iprod(tickers, tickers, [year]))
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_responses_physical
            .taq_trade_sign_self_correlator_year_avg_responses_physical_plot,
            iprod(tickers, [year]))
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_responses_physical
            .taq_trade_sign_cross_correlator_year_avg_responses_physical_plot,
            iprod(tickers, tickers, [year]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    # Initial message
    taq_data_tools_responses_physical.taq_initial_message()

    # Tickers and days to analyze
    year = '2008'
    tickers = ['AAPL', 'GOOG']

    # Basic folders
    taq_data_tools_responses_physical.taq_start_folders(year)

    # Run analysis
    # Comment the function taq_build_from_scratch if you do not have the C++
    # modules
    taq_data_analysis_responses_physical.taq_build_from_scratch(tickers, year)
    taq_data_analysis_responses_physical.taq_daily_data_extract(tickers, year)

    # Analysis and plot
    taq_data_plot_generator(tickers, year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
