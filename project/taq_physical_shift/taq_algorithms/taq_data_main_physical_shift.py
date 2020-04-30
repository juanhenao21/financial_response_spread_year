'''TAQ data main module.

The functions in the module run the complete analysis and plot of the TAQ data
for the physical shift between returns and trade signs. To run this module it
is necessary to have the files of the midpoint prices and trade signs for
physical time scale from the TAQ Responses Physical module.

This script requires the following modules:
    * itertools
    * multiprocessing
    * pandas
    * taq_data_analysis_physical_shift
    * taq_data_plot_physical_shift
    * taq_data_tools_physical_shift

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

import taq_data_analysis_physical_shift
import taq_data_plot_physical_shift
import taq_data_tools_physical_shift

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, taus):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analyzed (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analyzed (i.e '2016').
    :param taus: list of integers great than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Specific functions
    # Self-response
    for ticker in tickers:
        for tau in taus:

            taq_data_analysis_physical_shift \
                .taq_self_response_year_physical_shift_data(ticker, year, tau)

    ticker_prod = iprod(tickers, tickers)
    # ticker_prod = [('AAPL', 'MSFT'), ('MSFT', 'AAPL'),
    #                ('GS', 'JPM'), ('JPM', 'GS'),
    #                ('CVX', 'XOM'), ('XOM', 'CVX'),
    #                ('GOOG', 'MA'), ('MA', 'GOOG'),
    #                ('CME', 'GS'), ('GS', 'CME'),
    #                ('RIG', 'APA'), ('APA', 'RIG')]

    # Cross-response
    for ticks in ticker_prod:
        for tau in taus:

            taq_data_analysis_physical_shift \
                .taq_cross_response_year_physical_shift_data(ticks[0],
                                                             ticks[1], year,
                                                             tau)
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_physical_shift
                     .taq_self_response_year_avg_physical_shift_plot,
                     iprod(tickers, [year], [taus]))
    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Plot
        pool.starmap(taq_data_plot_physical_shift
                     .taq_cross_response_year_avg_physical_shift_plot,
                     iprod(tickers, tickers, [year], [taus]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    # Initial message
    taq_data_tools_physical_shift.taq_initial_message()

    # Tickers and days to analyze
    year = '2008'
    tickers = ['AAPL', 'GOOG']
    taus = [1, 10, 100, 1000]

    # Basic folders
    taq_data_tools_physical_shift.taq_start_folders(year)

    # Run analysis
    # Analysis and plot
    taq_data_plot_generator(tickers, year, taus)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
