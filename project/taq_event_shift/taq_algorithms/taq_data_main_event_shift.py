'''TAQ data main module.

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * pandas
    * taq_data_analysis_event_shift
    * taq_data_plot_event_shift
    * taq_data_tools_event_shift

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
import pandas as pd
import pickle

import taq_data_analysis_event_shift
import taq_data_plot_event_shift
import taq_data_tools_event_shift

__tau__ = 1000

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, taus):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :param taus: list of integers great than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_event_shift.taq_bussiness_days(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Especific functions
        pool.starmap(taq_data_analysis_event_shift
                     .taq_self_response_year_event_shift_data,
                     product(tickers, [year], taus))
        pool.starmap(taq_data_analysis_event_shift
                     .taq_cross_response_year_event_shift_data,
                     product(tickers, tickers, [year], taus))

        pool.starmap(taq_data_plot_event_shift
                     .taq_self_response_year_avg_event_shift_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot_event_shift
                     .taq_cross_response_year_avg_event_shift_plot,
                     product(tickers, tickers, [year]))

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
    taus = [1, 10, 100, 1000]

    # Basic folders
    taq_data_tools_event_shift.taq_start_folders('2008')

    # Run analysis
    taq_data_plot_generator(tickers, year, taus)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
