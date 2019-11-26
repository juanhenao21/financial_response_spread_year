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
        # print('No data')
        # print(e)
        # print()

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
    :return: tuple -- The function returns a value.
    """

    date_list = taq_bussiness_days(year)
    # date_list = ['2008-01-02', '2008-01-03', '2008-01-04']
    data = []
    args_prod = product([ticker], date_list)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        data.append(pool.starmap(taq_event_weight_day, args_prod))
        # pool.starmap(taq_event_weight_day, args_prod)

    total = np.sum(data[0], axis=0)

    weight = total[1] / total[0]

    return weight

# ----------------------------------------------------------------------------


def taq_event_time_self_response_relation_year(ticker, year):
    """Compute the relation between the event and time self response

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: tuple -- The function returns a value.
    """

    try:

        self_response_event = np.abs(pickle.load(open(''.join((
            f'../../taq_data/responses_event_data_{year}/taq_self_response'
            + f'_year_responses_event_data/taq_self_response_year_responses'
            + f'_event_data_{year}_{ticker}.pickle').split()), 'rb')))
        self_response_time = np.abs(pickle.load(open(''.join((
            f'../../taq_data/article_reproduction_data_{year}/taq_self'
            + f'_response_year_data/taq_self_response_year_data_{year}'
            + f'_{ticker}.pickle').split()), 'rb')))

        relation = self_response_event / self_response_time
        rel_value = np.mean(relation)

        return rel_value

    except FileNotFoundError as e:
        # print('No data')
        # print(e)
        # print()
        return None

# ----------------------------------------------------------------------------


def taq_event_time_cross_response_relation_year(ticker_i, ticker_j, year):
    """Compute the relation between the event and time self response

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: tuple -- The function returns a value.
    """

    try:

        cross_response_event = np.abs(pickle.load(open(''.join((
            f'../../taq_data/responses_event_data_{year}/taq_cross_response'
            + f'_year_responses_event_data/taq_cross_response_year_responses'
            + f'_event_data_{year}_{ticker_i}i_{ticker_j}j.pickle').split()),
            'rb')))
        cross_response_time = np.abs(pickle.load(open(''.join((
            f'../../taq_data/article_reproduction_data_{year}/taq_cross'
            + f'_response_year_data/taq_cross_response_year_data_{year}'
            + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb')))

        relation = cross_response_event / cross_response_time
        rel_value = np.mean(relation)

        return rel_value

    except FileNotFoundError as e:
        # print('No data')
        # print(e)
        # print()
        return None

# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    tickers_i = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    ticker_j = 'AAPL'
    year = '2008'

    # weight_j = taq_event_weight_year(ticker_j, year)
    # pickle.dump(weight_j, open(f'weight_{ticker_j}.pickle', 'wb'))
    weight_j = pickle.load(open(f'weight_{ticker_j}.pickle', 'rb'))

    for t_idx, ticker_i in enumerate(tickers_i):

        if (ticker_i == ticker_j):

            self_rel = \
                taq_event_time_self_response_relation_year(ticker_i, year)
            rel_error = np.abs(weight_j - self_rel) / weight_j * 100

            print(f'Self-response {ticker_j}')
            print(f'Weight = {weight_j :.5f}')
            print(f'Self-response relation = {self_rel :.5f}')
            print(f'Relative error = {rel_error :.3f}%')
            print()

        else:

            try:
                cross_rel = \
                    taq_event_time_cross_response_relation_year(ticker_i,
                                                                ticker_j,
                                                                year)
                rel_error = np.abs(weight_j - cross_rel) / weight_j * 100

                print(f'Cross-response ticker_i {ticker_i} - ticker_j '
                      + f'{ticker_j}')
                print(f'Weight = {weight_j :.5f}')
                print(f'Cross-response relation = {cross_rel :.5f}')
                print(f'Relative error = {rel_error :.3f}%')
                print()

            except TypeError:
                pass

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
