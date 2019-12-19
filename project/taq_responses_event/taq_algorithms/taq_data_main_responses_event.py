'''TAQ data main module.

The functions in the module run the complete extraction, analysis and plot of
the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * pandas
    * taq_data_analysis_responses_event
    * taq_data_plot_responses_event
    * taq_data_tools_responses_event

The module contains the following functions:
    * taq_build_from_scratch - extract data to dayly CSV files.
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
import subprocess

import taq_data_analysis_responses_event
import taq_data_plot_responses_event
import taq_data_tools_responses_event

__tau__ = 1000

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    for ticker_i in tickers:
        for ticker_j in tickers:

            if (ticker_i == ticker_j):
                # Self-response
                pass
            else:
                taq_data_analysis_responses_event. \
                    taq_cross_response_year_responses_event_data(ticker_i,
                                                                 ticker_j,
                                                                 year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        pool.starmap(taq_data_plot_responses_event
                     .taq_cross_response_year_avg_plot,
                     product(tickers, tickers, [year]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    # Tickers and days to analyze
    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    year = '2008'

    # Basic folders
    # taq_data_tools_responses_event.taq_start_folders(year)

    # Run analysis
    taq_data_plot_generator(tickers, year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
