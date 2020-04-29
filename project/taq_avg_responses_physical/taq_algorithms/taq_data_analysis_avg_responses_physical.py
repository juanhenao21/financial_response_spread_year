'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions and the trade sign self- and
cross-correlator functions. This module reproduces the sections 3.1 and 3.2 of
the `paper
<https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.


This script requires the following modules:
    * numpy
    * pandas
    * pickle
    * taq_data_tools_avg_responses_physical

The module contains the following functions:
    * taq_tickers_spread_data - obtains the tickers and the spread for the
      classification.
    * taq_self_response_year_avg_responses_physical_data - computes the average
      self response for groups of tickers in a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import pandas as pd
import pickle

import taq_data_tools_avg_responses_physical

__tau__ = 10000

# ----------------------------------------------------------------------------


def taq_tickers_spread_data(year):
    """Obtains the tickers and the spread range for the classification.

    :param div: integer of the number of divisions in the tickers (i.e. 5).
    :param year: string of the year to be analyzed (i.e. '2016').
    :return: tuple -- The function returns a tuple with a numpy array and a
     list.
    """

    function_name = taq_tickers_spread_data.__name__
    taq_data_tools_avg_responses_physical \
        .taq_function_header_print_data(function_name, '', '', year, '', '')

    try:
        # load data
        spread_data = pd.read_csv(
            '../../taq_avg_spread/taq_avg_spread_2008.csv',
            usecols=['Ticker', 'Avg_Spread'])

        tickers = []

        g1 = spread_data[spread_data['Avg_Spread'] < 0.03]
        tickers_g1 = tuple(g1['Ticker'].tolist())
        g2 = spread_data[(spread_data['Avg_Spread'] >= 0.03)
                         & (spread_data['Avg_Spread'] < 0.06)]
        tickers_g2 = tuple(g2['Ticker'].tolist())
        g3 = spread_data[(spread_data['Avg_Spread'] >= 0.06)
                         & (spread_data['Avg_Spread'] < 0.09)]
        tickers_g3 = tuple(g3['Ticker'].tolist())
        g4 = spread_data[(spread_data['Avg_Spread'] >= 0.09)
                         & (spread_data['Avg_Spread'] < 0.15)]
        tickers_g4 = tuple(g4['Ticker'].tolist())
        g5 = spread_data[(spread_data['Avg_Spread'] >= 0.15)
                         & (spread_data['Avg_Spread'] < 0.4)]
        tickers_g5 = tuple(g5['Ticker'].tolist())

        tickers.append(tickers_g1)
        tickers.append(tickers_g2)
        tickers.append(tickers_g3)
        tickers.append(tickers_g4)
        tickers.append(tickers_g5)

        return tickers

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        raise Exception('Check the CSV file')

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_physical_data(tickers, year):
    """Computes the avg self-response for groups of tickers in a year.

    Using the taq_self_response_day_avg_responses_physical_data function
    computes the average of self-response functions for different tickers for a
    year.

    :param tickers: list of the string abbreviation of the stocks to be
     analyzed (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_avg_responses_physical_data.__name__
    taq_data_tools_avg_responses_physical \
        .taq_function_header_print_data(function_name, '', '', year, '', '')

    results_avg = []

    for ticker in tickers:
        sum_response = np.zeros(__tau__)

        for tick in ticker:
            # Load data
            response = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_self'
                + f'_response_year_responses_physical_data/taq_self_response'
                + f'_year_responses_physical_data_{year}_{tick}.pickle', 'rb'))

            sum_response += response

        avg_response = sum_response / len(ticker)
        results_avg.append(avg_response)

    results_avg = tuple(results_avg)

    # Saving data
    taq_data_tools_avg_responses_physical \
        .taq_save_data(function_name, results_avg, '', '', year, '', '')

    return results_avg

# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    pass

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
