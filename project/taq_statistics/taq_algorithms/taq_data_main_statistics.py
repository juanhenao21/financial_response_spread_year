'''TAQ data main module.

The functions in the module run the complete analysis of the TAQ data.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * pandas
    * pickle
    * taq_data_analysis_statistics
    * taq_data_plot_statistics
    * taq_data_tools_statistics

The module contains the following functions:
    * taq_data_generator - generates all the analysis of the TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import pandas as pd

import taq_data_analysis_statistics
# import taq_data_plot_statistics
import taq_data_tools_statistics

# -----------------------------------------------------------------------------


def taq_data_generator(tickers, year):
    """Generates all the analysis of the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analyzed (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Statistics of the quotes and trades
    taq_data_analysis_statistics \
        .taq_quotes_trades_year_statistics_data(tickers, year)
    # Statistics midpoint
    taq_data_analysis_statistics \
        .taq_midpoint_year_statistics_data(tickers, year)

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    # Tickers and days to analyze
    # year, tickers = taq_data_tools_statistics.taq_initial_data()
    year = '2008'
    tickers = ['AAPL', 'MSFT', 'GS', 'JPM', 'CVX', 'XOM',
               'GOOG', 'MA', 'CME', 'RIG', 'APA']

    # Basic folders
    # taq_data_tools_statistics.taq_start_folders(year)

    # Run analysis
    # Analysis and plot
    taq_data_generator(tickers, year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
