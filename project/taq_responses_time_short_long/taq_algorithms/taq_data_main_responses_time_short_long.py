'''TAQ data main module

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * taq_data_analysis_responses_time_short_long
    * taq_data_plot_responses_time_short_long
    * taq_data_tools_responses_time_short_long

The module contains the following functions:
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product
import multiprocessing as mp
import os
import pickle

import taq_data_analysis_responses_time_short_long
import taq_data_plot_responses_time_short_long
import taq_data_tools_responses_time_short_long

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, taus, taus_p):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :param taus: Integer great than zero (i.e. 1000).
    :param taus_p: list of integers great than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Especific functions
        pool.starmap(taq_data_analysis_responses_time_short_long
                     .taq_self_response_year_time_short_long_tau_data,
                     product(tickers, [year], [taus], taus_p))
        pool.starmap(taq_data_analysis_responses_time_short_long
                     .taq_cross_response_year_time_short_long_tau_data,
                     product(tickers, tickers, [year], [taus], taus_p))

        pool.starmap(taq_data_plot_responses_time_short_long
                     .taq_self_response_year_avg_time_short_long_plot,
                     product(tickers, [year], [taus], taus_p))
        pool.starmap(taq_data_plot_responses_time_short_long
                     .taq_cross_response_year_avg_time_short_long_plot,
                     product(tickers, tickers, [year], [taus], taus_p))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    # Tickers and days to analyze
    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    year = '2008'
    taus_p = [x for x in range(10, 101, 10)]
    taus = [1000]

    # Basic folders
    taq_data_tools_responses_time_short_long.taq_start_folders('2008')

    # Run analysis
    taq_data_plot_generator(tickers, year, taus, taus_p)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
