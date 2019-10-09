'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * numpy
    * pandas
    * taq_data_tools_responses_event

The module contains the following functions:
    * taq_self_response_day_responses_event_data - computes the self response
     of a day.
    * taq_self_response_year_responses_event_data - computes the self response
     of a year.
    * taq_cross_response_day_responses_event_data - computes the cross
     response of a day.
    * taq_cross_response_year_responses_event_data - computes the cross
     response of a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_responses_event

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_midpoint_day_responses_event_data(ticker, date):
    """Create the midpoint associated with the trades signs in event scale.

    Using the midpoint price in time scale, associate the value of each second
    to the value of each trade in event scale for a day.

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

    function_name = taq_midpoint_day_responses_event_data.__name__
    taq_data_tools_responses_event \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        midpoint = pickle.load(open(''.join((
                f'../../taq_data/article_reproduction_data_{year}/taq_midpoint'
                + f'_time_data/taq_midpoint_time_data_midpoint_{year}{month}'
                + f'{day}_{ticker}.pickle').split()), 'rb'))
        time_t, _, _= pickle.load(open("".join((
                f'../../taq_data/responses_event_shift_data_{year}/taq_trade'
                + f'_signs_responses_event_shift_data/taq_trade_signs'
                + f'_responses_event_shift_data_{year}{month}{day}_{ticker}'
                + f'.pickle').split()), 'rb'))

        assert not np.sum(midpoint == 0)
        assert not np.sum(time_t == 0)

        # Midpoint array with the length of the trade signs
        midpoint_t = 0. * time_t
        midpoint = midpoint[1:]
        time_scale = range(34801, 57000)

        # It is needed to associate each trade sign with a midpoint price
        for t_idx, t_val in enumerate(time_scale):
            condition = time_t == t_val
            len_c = np.sum(condition)
            midpoint_t[condition] = midpoint[t_idx] * np.ones(len_c)


        assert not np.sum(midpoint_t == 0)

        # Saving data
        taq_data_tools_responses_event.taq_save_data(function_name, midpoint_t,
                                                     ticker, ticker, year,
                                                     month, day)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_event_data(ticker, date):
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

    function_name = taq_self_response_day_responses_event_data.__name__
    taq_data_tools_responses_event \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        midpoint = pickle.load(open(''.join((
                f'../../taq_data/responses_event_data_{year}/taq_midpoint'
                + f'day_responses_event_data/taq_midpoint_day_responses_event'
                + f'_data_midpoint_{year}{month}{day}_{ticker}.pickle')
                .split()) , 'rb'))
        time_t, _, trade_sign = pickle.load(open("".join((
            f'../../taq_data/responses_event_shift_data_{year}/taq_trade'
            + f'_signs_responses_event_shift_data/taq_trade_signs'
            + f'_responses_event_shift_data_{year}{month}{day}_{ticker}'
            + f'.pickle').split()), 'rb'))

        assert len(midpoint) == len(time_t)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint price return and the self response function

        # Depending on the tau value
        for tau_idx in range(__tau__):
            for t_val in range(34800, 56999):

                trade_sign_tau = trade_sign[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len
                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return

                # midpoint price returns

                log_return_sec = (midpoint[tau_idx + 1:]
                                - midpoint[:-tau_idx - 1]) \
                    / midpoint[:-tau_idx - 1]

                # Obtain the self response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_sec * trade_sign_tau
                    self_response_tau[tau_idx] = np.sum(product)

        return (self_response_tau, num)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_event_data(ticker, year):
    """Computes the self response of a year.

    Using the taq_self_response_day_responses_event_data function computes the self-response
    function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_responses_event_data.__name__
    taq_data_tools_responses_event \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_event.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:
            data, avg_num = taq_self_response_day_responses_event_data(ticker, date)
            self_ += data
            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    taq_data_tools_responses_event \
        .taq_save_data(function_name, self_ / num_s_t, ticker, ticker, year,
                       '', '')

    return (self_ / num_s_t, num_s_t)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_event_data(ticker_i, ticker_j, date):
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
            function_name = taq_cross_response_day_responses_event_data.__name__
            taq_data_tools_responses_event \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/responses_event_data_{1}/taq'
                    + '_midpoint_time_data/taq_midpoint_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
            _, _, trade_sign_j = pickle.load(open("".join((
                    '../../taq_data/responses_event_data_2008/taq_trade_'
                    + 'signs_time_data/taq_trade_signs_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function

            # Depending on the tau value
            for tau_idx in range(__tau__):

                trade_sign_tau = 1 * trade_sign_j[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len
                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return

                log_return_i_sec = (midpoint_i[tau_idx + 1:]
                                    - midpoint_i[:-tau_idx - 1]) \
                    / midpoint_i[:-tau_idx - 1]

                # Obtain the cross response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_i_sec * trade_sign_tau
                    cross_response_tau[tau_idx] = np.sum(product)

            return (cross_response_tau, num)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_event_data(ticker_i, ticker_j, year):
    """Computes the cross response of a year.

    Using the taq_cross_response_day data function computes the cross-response
    function for a year.

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
        function_name = taq_cross_response_year_responses_event_data.__name__
        taq_data_tools_responses_event \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_event.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:
                data, avg_num = taq_cross_response_day_responses_event_data(ticker_i, ticker_j,
                                                            date)

                cross += data
                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        # midpoint price returns
        taq_data_tools_responses_event \
            .taq_save_data(function_name, cross / num_c_t, ticker_i, ticker_j,
                           year, '', '')

        return (cross / num_c_t, num_c_t)

# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    taq_midpoint_day_responses_event_data('AAPL', '2008-01-02')

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
