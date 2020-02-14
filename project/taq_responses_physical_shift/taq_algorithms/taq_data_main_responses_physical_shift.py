'''TAQ data main module

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * pandas
    * taq_data_analysis_responses_physical_shift
    * taq_data_plot_responses_physical_shift
    * taq_data_tools_responses_physical_shift

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
import pandas as pd
import pickle

import taq_data_analysis_responses_physical_shift
import taq_data_plot_responses_physical_shift
import taq_data_tools_responses_physical_shift

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, shifts):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_responses_physical_shift \
        .taq_bussiness_days(year)

    # Especific functions
    # Self-response
    for ticker in tickers:
        for shift in shifts:

            taq_data_analysis_responses_physical_shift \
                .taq_self_response_year_responses_physical_shift_data(ticker,
                                                                      year,
                                                                      shift)

    # ticker_prod = iprod(tickers, tickers)
    ticker_prod = [('AAPL', 'MSFT'), ('MSFT', 'AAPL'),
                   ('GS', 'JPM'), ('JPM', 'GS'),
                   ('CVX', 'XOM'), ('XOM', 'CVX'),
                   ('GOOG', 'MA'), ('MA', 'GOOG'),
                   ('CME', 'GS'), ('GS', 'CME'),
                   ('RIG', 'APA'), ('APA', 'RIG')]

    # Cross-response
    for ticks in ticker_prod:
        for shift in shifts:

            taq_data_analysis_responses_physical_shift \
                .taq_cross_response_year_responses_physical_shift_data(
                    ticks[0], ticks[1], year, shift)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_responses_physical_shift
                     .taq_self_response_year_avg_responses_physical_shift_plot,
                     iprod(tickers, [year], [shifts]))
        pool.starmap(taq_data_plot_responses_physical_shift
                     .taq_cross_response_year_avg_responses_physical_shift_plot,
                     iprod(tickers, tickers, [year], [shifts]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    # Tickers and days to analyze
    # year, tickers, shifts = taq_data_tools_responses_physical_shift \
    #     .taq_initial_data()
    year = '2008'
    tickers = ['AAPL', 'MSFT', 'GS', 'JPM', 'CVX', 'XOM',
               'GOOG', 'MA', 'CME', 'RIG', 'APA']
    shifts = [1, 10, 100, 500]

    # Basic folders
    # taq_data_tools_responses_physical_shift.taq_start_folders('2008')

    # Run analysis
    # Analysis and plot
    taq_data_plot_generator(tickers, year, shifts)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
