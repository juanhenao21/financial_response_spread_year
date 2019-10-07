'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * numpy
    * pandas
    * taq_data_tools_responses_time_activity

The module contains the following functions:
    * taq_self_response_day_responses_time_activity_data - computes the self
     response of a day.
    * taq_self_response_year_responses_time_activity_data_data - computes the
     self response of a year.
    * taq_cross_response_day_responses_time_activity_data - computes the cross
     response of a day.
    * taq_cross_response_year_responses_time_activity_data_data - computes the
     cross response of a year.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_responses_time_activity

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_trades_count_responses_time_activity_data(ticker, date):
    """Counts the number of trades per second.

    Using the data obtained with the taq_trade_signs_responses_event_shift_data
    function, implemented in the taq_responses_event_shift, counts the number
    of trades per second.

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

    function_name = taq_trades_count_responses_time_activity_data.__name__
    taq_data_tools_responses_time_activity \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        time_t, _, trade_sign_i = pickle.load(open("".join((
            f'../../taq_data/responses_event_shift_data_{year}/taq_trade'
            + f'_signs_responses_event_shift_data/taq_trade_signs'
            + f'_responses_event_shift_data_{year}{month}{day}_{ticker}'
            + f'.pickle').split()), 'rb'))
        # Open market time [34801, 57000]
        full_time = np.array(range(34801, 57001))
        trades_count = np.zeros(len(full_time))

        # Count the number of trades in every second
        for t_idx, t_val in enumerate(full_time):
            condition = t_val == time_t
            trades_count[t_idx] = len(trade_sign_i[condition])

        # Save data
        taq_data_tools_responses_time_activity \
            .taq_save_data(function_name, (full_time, trades_count), ticker,
                           ticker, year, month, day)

        return (full_time, trades_count)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_time_activity_data(ticker, date):
    """Computes the self response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different time lags (:math:`\tau`) for a day.

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

    function_name = taq_self_response_day_responses_time_activity_data.__name__
    taq_data_tools_responses_time_activity \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        midpoint = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_time_data/taq_midpoint_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        _, _, trade_sign = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_time_data/taq_trade_signs_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        _, trade_count = pickle.load(open(''.join((
                f'../../taq_data/responses_time_activity_data_{year}/taq'
                + f'_trades_count_responses_time_activity_data/taq_trades'
                + f'_count_responses_time_activity_data_{year}{month}{day}'
                + f'_{ticker}.pickle').split()), 'rb'))

        assert len(midpoint) == len(trade_sign)
        assert len(midpoint) == len(trade_count)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint price return and the self response function

        # Depending on the tau value
        for tau_idx in range(__tau__):

            trade_sign_tau = trade_sign[:-tau_idx - 1]
            trade_count_tau = trade_count[:-tau_idx - 1]
            trade_count_len = np.sum(trade_count_tau)
            num[tau_idx] = trade_count_len
            # Obtain the midpoint price return. Displace the numerator tau
            # values to the right and compute the return

            # midpoint price returns

            log_return_sec = (midpoint[tau_idx + 1:]
                              - midpoint[:-tau_idx - 1]) \
                / midpoint[:-tau_idx - 1]

            # Obtain the self response value
            if (trade_count_len != 0):
                product = log_return_sec * trade_sign_tau * trade_count_tau
                self_response_tau[tau_idx] = np.sum(product)

        return (self_response_tau, num)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_time_activity_data(ticker, year):
    """Computes the self response of a year.

    Using the taq_self_response_day_responses_time_activity_data function
    computes the self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_responses_time_activity_data \
        .__name__
    taq_data_tools_responses_time_activity \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_time_activity.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:
            data, avg_num = \
                taq_self_response_day_responses_time_activity_data(ticker,
                                                                   date)
            self_ += data
            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    taq_data_tools_responses_time_activity \
        .taq_save_data(function_name, self_ / num_s_t, ticker, ticker, year,
                       '', '')

    return (self_ / num_s_t, num_s_t)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_time_activity_data(ticker_i, ticker_j,
                                                        date):
    """Computes the cross response of a day.

    Using the midpoint price of ticker i and trade signs of ticker j computes
    the cross-response during different time lags (:math:`\tau`) for a day.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = \
                taq_cross_response_day_responses_time_activity_data.__name__
            taq_data_tools_responses_time_activity \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq'
                    + '_midpoint_time_data/taq_midpoint_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
            _, _, trade_sign_j = pickle.load(open("".join((
                    '../../taq_data/article_reproduction_data_2008/taq_trade_'
                    + 'signs_time_data/taq_trade_signs_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))
            _, trade_count_j = pickle.load(open(''.join((
                    f'../../taq_data/responses_time_activity_data_{year}/taq'
                    + f'_trades_count_responses_time_activity_data/taq_trades'
                    + f'_count_responses_time_activity_data_{year}{month}{day}'
                    + f'_{ticker_j}.pickle').split()), 'rb'))

            assert len(midpoint_i) == len(trade_sign_j)
            assert len(midpoint_i) == len(trade_count_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function

            # Depending on the tau value
            for tau_idx in range(__tau__):

                trade_sign_tau = trade_sign_j[:-tau_idx - 1]
                trade_count_tau = trade_count_j[:-tau_idx - 1]
                trade_count_len = np.sum(trade_count_tau)
                num[tau_idx] = trade_count_len
                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return

                log_return_i_sec = (midpoint_i[tau_idx + 1:]
                                    - midpoint_i[:-tau_idx - 1]) \
                    / midpoint_i[:-tau_idx - 1]

                # Obtain the cross response value
                if (trade_count_len != 0):
                    product = log_return_i_sec * trade_sign_tau \
                        * trade_count_tau
                    cross_response_tau[tau_idx] = np.sum(product)

            return (cross_response_tau, num)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_time_activity_data(ticker_i, ticker_j,
                                                         year):
    """Computes the cross response of a year.

    Using the taq_cross_response_day_responses_activity_data function computes
    the cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = taq_cross_response_year_responses_time_activity_data \
            .__name__
        taq_data_tools_responses_time_activity \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_time_activity.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:
                data, avg_num = \
                    taq_cross_response_day_responses_time_activity_data(
                        ticker_i, ticker_j, date)

                cross += data
                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        # midpoint price returns
        taq_data_tools_responses_time_activity \
            .taq_save_data(function_name, cross / num_c_t, ticker_i, ticker_j,
                           year, '', '')

        return (cross / num_c_t, num_c_t)

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
