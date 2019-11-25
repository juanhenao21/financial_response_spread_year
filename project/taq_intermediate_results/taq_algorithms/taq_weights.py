'''TAQ weights analysis.

Analize the results of the weights (event, time and activity scale) of
different stocks for a year.

This script requires the following modules:
    * matplotlib
    * numpy
    * scipy

The module contains the following functions:
    * taq_trades_number_imbalance_day_data - obtain the number of trades and
     imbalance in every second for one day.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pickle
import scipy.stats as stats
from itertools import product

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_bussiness_days(year):
    """Generates a list with the dates of the bussiness days in a year

    :param year: string of the year to be analized (i.e '2008').
    :return: list.
    """

    init_date = '01/01/{}'.format(year)
    last_date = '12/31/{}'.format(year)

    # Use only the bussiness days
    dt = pd.date_range(start=init_date, end=last_date, freq='B')
    dt_df = dt.to_frame(index=False)
    date_list = dt_df[0].astype(str).tolist()

    return date_list

# -----------------------------------------------------------------------------
def taq_trades_number_imbalance_day_data(ticker, date):
    """ Compute the number of trades an imbalance for a day.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:

        time_t, ask_t, identified_trades = pickle.load(open(''.join((
            f'../../taq_data/responses_event_shift_data_{year}/taq_trade_signs'
            + f'_responses_event_shift_data/taq_trade_signs_responses _event'
            + f'_shift_data_{year}{month}{day}_{ticker}.pickle').split()),
            'rb'))

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        full_time = np.array(range(34801, 57001))

        # Arrays to store number of trades and imbalance of trades
        trades_sum = 0. * full_time
        trades_num = 0. * full_time

        # Implementation of equation (2). Trade sign in each second
        for t_idx, t_val in enumerate(full_time):

            condition = (time_t >= t_val) * (time_t < t_val + 1)
            # Empirical
            trades_same_t_exp = identified_trades[condition]
            t_sum = np.sum(trades_same_t_exp)
            t_num = np.sum(condition)
            trades_sum[t_idx] = t_sum
            trades_num[t_idx] = t_num

        return (trades_num, trades_sum)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()

        zeros = np.zeros(len(range(34801, 57001)))
        return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_event_weight_day(ticker, date):
    """Compute the event weight for a day.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """
    print(date)
    # Compute data
    trades_num, trades_sum = taq_trades_number_imbalance_day_data(ticker, date)
    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)
    # Filter trades and imbalance to only have seconds with activity
    condition_num_no_0 = trades_num != 0
    trades_num_no_0 = trades_num[condition_num_no_0]
    trades_sum_abs_no_0 = trades_sum_abs[condition_num_no_0]

    # Sum the trades and the imbalance
    trades_num_no_0_sum = np.sum(trades_num_no_0)
    trades_sum_abs_no_0_sum = np.sum(trades_sum_abs_no_0)

    return (trades_num_no_0_sum, trades_sum_abs_no_0_sum)

# ----------------------------------------------------------------------------


def taq_event_weight_year(ticker, year):
    """Compute the event weight for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: tuple -- The function returns a tuple with values.
    """

    date_list = taq_bussiness_days(year)
    # date_list = ['2008-01-02', '2008-01-03', '2008-01-04']
    weight = []
    args_prod = product([ticker], date_list)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        weight.append(pool.starmap(taq_event_weight_day, args_prod))
        # pool.starmap(taq_event_weight_day, args_prod)

    total = np.sum(weight[0], axis=0)

    print(total)
    print(f'Weight = {total[1] / total[0]}')

    return None
# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    dates = ['2008-01-02', '2008-04-08', '2008-08-14', '2008-12-18']

    ticker = 'AAPL'
    year = '2008'
    month = '01'
    day = '02'
    date = '2008-01-02'

    taq_event_weight_year(ticker, year)

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
