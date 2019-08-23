'''TAQ data main module

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * pandas
    * taq_data_analysis_responses_event_shift
    * taq_data_plot_responses_event_shift
    * taq_data_tools_responses_event_shift

The module contains the following functions:
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product
import os
import pandas as pd
import multiprocessing as mp
import pickle

import taq_data_analysis_responses_event_shift
import taq_data_plot_responses_event_shift
import taq_data_tools_responses_event_shift

__tau__ = 10000

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

    date_list = taq_data_tools_responses_event_shift.taq_bussiness_days(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Basic functions
        pool.starmap(taq_data_analysis_responses_event_shift
                     .taq_trade_signs_responses_event_shift_data,
                     product(tickers, date_list))

        # Especific functions
        pool.starmap(taq_data_analysis_responses_event_shift
                     .taq_self_response_year_responses_event_shift_data,
                     product(tickers, [year], shifts))
        pool.starmap(taq_data_analysis_responses_event_shift
                     .taq_cross_response_year_responses_event_shift_data,
                     product(tickers, tickers, [year], shifts))

        pool.starmap(taq_data_plot_responses_event_shift
                     .taq_self_response_year_avg_responses_event_shift_plot,
                     product(tickers, [year], [shifts]))
        pool.starmap(taq_data_plot_responses_event_shift
                     .taq_cross_response_year_avg_responses_event_shift_plot,
                     product(tickers, tickers, [year], [shifts]))

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
    shifts = [1, 5, 10, 50, 100, 500, 1000, 5000]

    # Basic folders
    taq_data_tools_responses_event_shift.taq_start_folders('2008')

    # Run analysis
    taq_data_plot_generator(tickers, year, shifts)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
