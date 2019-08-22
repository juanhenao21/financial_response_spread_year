'''TAQ data main module

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools
    * multiprocessing
    * pandas
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
import pandas as pd
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
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_responses_event_shift.taq_bussiness_days(year)

    for ticker in tickers:
        for tau in taus:

            taq_data_analysis.taq_self_response_year_responses_event_trades_minute_data(ticker, year, tau)

    for tau in taus:

        taq_data_analysis.taq_cross_response_year_responses_event_trades_minute_data(tickers[0], tickers[1], year, tau)
        taq_data_analysis.taq_cross_response_year_responses_event_trades_minute_data(tickers[1], tickers[0], year, tau)

        taq_data_plot.taq_self_response_year_responses_event_trades_minute_plot(tickers[0], year, tau)
        taq_data_plot.taq_self_response_year_responses_event_trades_minute_plot(tickers[1], year, tau)
        taq_data_plot.taq_cross_response_year_responses_event_trades_minute_plot(tickers[0], tickers[1], year, tau)
        taq_data_plot.taq_cross_response_year_responses_event_trades_minute_plot(tickers[1], tickers[0], year, tau)

        taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data(tickers[0], year, tau)
        taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data(tickers[1], year, tau)
        taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data(tickers[0], tickers[1], year, tau)
        taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data(tickers[1], tickers[0], year, tau)

        taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot(tickers[0], year, tau)
        taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot(tickers[1], year, tau)
        taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot(tickers[0], tickers[1], year, tau)
        taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot(tickers[1], tickers[0], year, tau)

        taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data_v2(tickers[0], year, tau)
        taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data_v2(tickers[1], year, tau)
        taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data_v2(tickers[0], tickers[1], year, tau)
        taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data_v2(tickers[1], tickers[0], year, tau)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot_v2,
        product(tickers, [year], taus))
        pool.starmap(taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot_v2,
        product(tickers, tickers, [year], taus))


    return None

# -----------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    tickers = ['AAPL', 'MSFT']
    year = '2008'
    taus = [5, 10, 50, 100, 500, 1000]

    # for ticker in tickers:
    #     for tau in taus:

    #         taq_data_analysis.taq_self_response_year_responses_event_trades_minute_data(ticker, year, tau)

    # for tau in taus:

        # taq_data_analysis.taq_cross_response_year_responses_event_trades_minute_data(tickers[0], tickers[1], year, tau)
        # taq_data_analysis.taq_cross_response_year_responses_event_trades_minute_data(tickers[1], tickers[0], year, tau)

        # taq_data_plot.taq_self_response_year_responses_event_trades_minute_plot(tickers[0], year, tau)
        # taq_data_plot.taq_self_response_year_responses_event_trades_minute_plot(tickers[1], year, tau)
        # taq_data_plot.taq_cross_response_year_responses_event_trades_minute_plot(tickers[0], tickers[1], year, tau)
        # taq_data_plot.taq_cross_response_year_responses_event_trades_minute_plot(tickers[1], tickers[0], year, tau)

        # taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data(tickers[0], year, tau)
        # taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data(tickers[1], year, tau)
        # taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data(tickers[0], tickers[1], year, tau)
        # taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data(tickers[1], tickers[0], year, tau)

        # taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot(tickers[0], year, tau)
        # taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot(tickers[1], year, tau)
        # taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot(tickers[0], tickers[1], year, tau)
        # taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot(tickers[1], tickers[0], year, tau)

        # taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data_v2(tickers[0], year, tau)
        # taq_data_analysis.taq_self_response_year_avg_responses_event_trades_minute_data_v2(tickers[1], year, tau)
        # taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data_v2(tickers[0], tickers[1], year, tau)
        # taq_data_analysis.taq_cross_response_year_avg_responses_event_trades_minute_data_v2(tickers[1], tickers[0], year, tau)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(taq_data_plot.taq_self_response_year_avg_responses_event_trades_minute_plot_v2,
        product(tickers, [year], taus))
        pool.starmap(taq_data_plot.taq_cross_response_year_avg_responses_event_trades_minute_plot_v2,
        product(tickers, tickers, [year], taus))

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
