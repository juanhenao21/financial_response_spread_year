'''TAQ data main module

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * taq_data_analysis_responses_event_trades_minute
    * taq_data_plot_responses_event_trades_minute
    * taq_data_tools_responses_event_trades_minute

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

import taq_data_analysis_responses_event_trades_minute
import taq_data_plot_responses_event_trades_minute
import taq_data_tools_responses_event_trades_minute

__tau__ = 10000

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, taus):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Self-response
    self_parameters = product(tickers, [year], taus)
    # Cross-response
    cross_parameters = product(tickers, tickers, [year], taus)

    for self_ in self_parameters:

        taq_data_analysis_responses_event_trades_minute \
            .taq_self_response_year_responses_event_trades_minute_data(*self_)

    for self_ in self_parameters:

        taq_data_plot_responses_event_trades_minute \
            .taq_self_response_year_responses_event_trades_minute_plot(*self_)

    for self_ in self_parameters:

        taq_data_analysis_responses_event_trades_minute \
            .taq_self_response_year_avg_responses_event_trades_minute_data(
                *self_)

    for cross in cross_parameters:

        taq_data_analysis_responses_event_trades_minute \
            .taq_cross_response_year_responses_event_trades_minute_data(*cross)

    for cross in cross_parameters:

        taq_data_plot_responses_event_trades_minute \
            .taq_cross_response_year_responses_event_trades_minute_plot(*cross)

    for cross in cross_parameters:

        taq_data_analysis_responses_event_trades_minute \
            .taq_cross_response_year_avg_responses_event_trades_minute_data(
                *cross)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(
            taq_data_plot_responses_event_trades_minute
            .taq_self_response_year_avg_responses_event_trades_minute_plot,
            product(tickers, [year], taus))
        pool.starmap(
            taq_data_plot_responses_event_trades_minute
            .taq_cross_response_year_avg_responses_event_trades_minute_plot,
            product(tickers, tickers, [year], taus))

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
    taus = [5, 10, 50, 100, 500, 1000]

    # Basic folders
    taq_data_tools_responses_event_trades_minute.taq_start_folders('2008')

    # Run analysis
    taq_data_plot_generator(tickers, year, taus)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
