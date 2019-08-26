''' TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * numpy
    * pandas
    * traceback
    * taq_data_tools_responses_event_trades_minute

The module contains the following functions:
    * taq_self_response_day_responses_event_trades_minute_data - computes the
      self response of a day.
    * taq_self_response_year_responses_event_trades_minute_data - computes the
      self response of a year.
    * taq_self_response_year_avg_responses_event_trades_minute_data - computes
      the average self response of a year.
    * taq_cross_response_day_responses_event_trades_minute_data - computes the
      cross response of a day.
    * taq_cross_response_year_responses_event_trades_minute_data - computes the
      cross response of a year.
    * taq_cross_response_year_avg_responses_event_trades_minute_data - computes
      the average cross response of a year.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os
import pandas as pd
import pickle
import traceback

import taq_data_tools_responses_event_trades_minute

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_event_trades_minute_data(ticker, date,
                                                             tau):
    """Computes the self response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different trades per minute for a day. There is a constant
    :math:`\\tau` that must be set in the parameters.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param tau: integer great than zero (i.e. 10).
    :return: tuple -- The function returns a tuple with positions.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_day_responses_event_trades_minute_data. \
        __name__
    taq_data_tools_responses_event_trades_minute \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        midpoint_i = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_time_data/taq_midpoint_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        time_t, _, trade_sign_i = pickle.load(open("".join((
                '../../taq_data/responses_event_shift_data_{1}/taq_trade'
                + '_signs_responses_event_shift_data/taq_trade_signs'
                + '_responses_event_shift_data_{1}{2}{3}_{0}.pickle')
                .split())
                .format(ticker, year, month, day), 'rb'))

        # As the data is loaded from the article reproduction module results,
        # the data have a shift of 1 second.
        time_m = np.array(range(34801, 57001))

        assert not np.sum(trade_sign_i == 0)
        assert not np.sum(midpoint_i == 0)
        assert len(midpoint_i) == len(time_m)

        # Array of the average of each tau. 10^3 s used by Wang
        # List to save the tuples with the response and rates.
        points = []

        # Minutes during the open market considering opening at 9:40 and
        # closing at 15:50
        time_minutes = np.array(range(370))

        # Calculating the midpoint price return and the self response function
        midpoint_t = 0. * trade_sign_i

        # Filling with midpoint price values
        for t_idx, t_val in enumerate(time_m):
            condition = time_t == t_val
            len_c = np.sum(condition)
            midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

        assert not np.sum(midpoint_t == 0)

        # Obtain the midpoint price return. Displace the numerator tau
        # values to the right and compute the return
        # Midpoint price returns
        log_return_sec = (midpoint_t[tau + 1:]
                          - midpoint_t[:-tau - 1]) \
            / midpoint_t[:-tau - 1]

        trade_sign_tau_ = trade_sign_i[:-tau - 1]
        time_t = time_t[:- tau - 1]
        assert len(trade_sign_tau_) == len(log_return_sec)

        # Depending on the trades per minute value
        for t_idx, t_val in enumerate(time_minutes):

            if (t_idx):
                # Select the values in each minute
                condition = (time_t < 34800 + time_minutes[t_idx] * 60) \
                 * (time_t >= 34800 + time_minutes[t_idx - 1] * 60)
                trade_sign_tau = trade_sign_tau_[condition]
                log_return = log_return_sec[condition]
                trades_minute = np.sum(condition)

                # Obtain the self response value
                product = log_return * trade_sign_tau
                points.extend([(trades_minute, i) for i in product])

            else:
                pass

        return points

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_event_trades_minute_data(ticker, year,
                                                              tau):
    """Computes the self response of a year.

    Using the taq_self_response_day_responses_event_trades_minute_data function
    computes the self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: None – The function saves the data in a file and does not return
     a value.
    """

    function_name = \
        taq_self_response_year_responses_event_trades_minute_data.__name__
    taq_data_tools_responses_event_trades_minute \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_event_trades_minute \
        .taq_bussiness_days(year)

    points = []

    for date in dates:

        try:
            points.extend(
                taq_self_response_day_responses_event_trades_minute_data(
                          ticker, date, tau))

        except TypeError:
            pass

    # Saving data
    taq_data_tools_responses_event_trades_minute \
        .taq_save_data('{}_tau_{}'.format(function_name, tau), points, ticker,
                       ticker, year, '', '')

    return None

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_event_trades_minute_data(ticker, year,
                                                                  tau):
    """Computes the average self response of a year.

    Using the taq_self_response_day_responses_event_trades_minute_data function
    computes the average self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = \
        taq_self_response_year_avg_responses_event_trades_minute_data \
        .__name__
    taq_data_tools_responses_event_trades_minute \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    try:
        # Load data
        responses = pickle.load(open(''.join((
                '../../taq_data/responses_event_trades_minute_data_{1}/taq'
                + '_self_response_year_responses_event_trades_minute_data'
                + '_tau_{2}/taq_self_response_year_responses_event_trades'
                + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
                .format(ticker, year, tau), 'rb'))

        responses.sort(key=lambda tup: tup[0])
        res_list = [list(i) for i in zip(*responses)]
        rate = np.asarray(res_list[0])
        res = np.asarray(res_list[1])

        res_avg = []
        time = []
        avg_num = len(res)

        for i in range(1, 11):
            condition = rate == i
            if (np.sum(condition)):
                res_avg.append(np.sum(res[condition]) / avg_num)
                time.append(i)

        inter1 = list(range(10, 101, 10))
        for i, v in enumerate(inter1):
            if (v == 10):
                pass
            else:
                condition = (rate <= inter1[i]) \
                            * (rate > inter1[i - 1])
                if (np.sum(condition)):
                    res_avg.append(np.sum(res[condition]) / avg_num)
                    time.append(v)

        inter2 = list(range(100, 1001, 100))
        for i, v in enumerate(inter2):
            if (v == 100):
                pass
            else:
                condition = (rate <= inter2[i]) \
                            * (rate > inter2[i-1])
                if (np.sum(condition)):
                    res_avg.append(np.sum(res[condition]) / avg_num)
                    time.append(v)

        inter3 = list(range(1000, 10001, 1000))
        for i, v in enumerate(inter3):
            if (v == 1000):
                pass
            else:
                condition = (rate <= inter3[i]) \
                            * (rate > inter3[i-1])
                if (np.sum(condition)):
                    res_avg.append(np.sum(res[condition]) / avg_num)
                    time.append(v)

    except TypeError as e:
        print(e)
        print(traceback.format_exc())
        pass

    assert len(res_avg) == len(time)

    # Saving data
    taq_data_tools_responses_event_trades_minute \
        .taq_save_data('{}_tau_{}'.format(function_name, tau), (time, res_avg),
                       ticker, ticker, year, '', '')

    return (time, res_avg)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_event_trades_minute_data(ticker_i,
                                                              ticker_j, date,
                                                              tau):
    """Computes the cross response of a day.

    Using the midpoint price of ticker i and trade signs of ticker j computes
    the cross-response during different event shifts for a day. There is a
    constant :math:`\\tau` that most be set in the parameters.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with positions.
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
                taq_cross_response_day_responses_event_trades_minute_data \
                .__name__
            taq_data_tools_responses_event_trades_minute \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq'
                    + '_midpoint_time_data/taq_midpoint_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))

            time_t, _, trade_sign_j = pickle.load(open("".join((
                '../../taq_data/responses_event_shift_data_{1}/taq_trade'
                + '_signs_responses_event_shift_data/taq_trade_signs'
                + '_responses_event_shift_data_{1}{2}{3}_{0}.pickle')
                .split())
                .format(ticker_j, year, month, day), 'rb'))

            # As the data is loaded from the article reproduction module
            # results, the data have a shift of 1 second.
            time_m = np.array(range(34801, 57001))

            assert not np.sum(trade_sign_j == 0)
            assert not np.sum(midpoint_i == 0)
            assert len(midpoint_i) == len(time_m)

            # List to save the tuples with the response and rates
            points = []

            # Minutes during the open market considering opening at 9:40 and
            # closing at 15:50
            time_minutes = np.array(range(370))

            # Calculating the midpoint price return and the cross response
            # function
            midpoint_t = 0. * trade_sign_j

            # Filling with midpoint price values
            for t_idx, t_val in enumerate(time_m):
                condition = time_t == t_val
                len_c = np.sum(condition)
                midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

            assert not np.sum(midpoint_t == 0)

            # Obtain the midpoint price return. Displace the numerator tau
            # values to the right and compute the return
            # Midpoint price returns
            log_return_sec = (midpoint_t[tau + 1:]
                              - midpoint_t[:-tau - 1]) \
                / midpoint_t[:-tau - 1]

            trade_sign_tau_ = trade_sign_j[:-tau - 1]
            time_t = time_t[:- tau - 1]
            assert len(trade_sign_tau_) == len(log_return_sec)

            # Depending on the trades per minute value
            for t_idx, t_val in enumerate(time_minutes):

                if (t_idx):
                    # Select the values in each minute
                    condition = (time_t < 34800 + time_minutes[t_idx] * 60) \
                            * (time_t >= 34800 + time_minutes[t_idx - 1] * 60)
                    trade_sign_tau = trade_sign_tau_[condition]
                    log_return = log_return_sec[condition]
                    trades_minute = np.sum(condition)

                    # Obtain the self response value
                    product = log_return * trade_sign_tau
                    points.extend([(trades_minute, i) for i in product])

                else:
                    pass

            return points

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_event_trades_minute_data(ticker_i,
                                                               ticker_j, year,
                                                               tau):
    """Computes the cross response of a year.

    Using the taq_cross_response_day_responses_event_trades_minutes_data
    function computes the cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: None – The function saves the data in a file and does not return a
     value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = \
            taq_cross_response_year_responses_event_trades_minute_data \
            .__name__
        taq_data_tools_responses_event_trades_minute \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_event_trades_minute \
            .taq_bussiness_days(year)

        points = []

        for date in dates:

            try:
                points.extend(
                    taq_cross_response_day_responses_event_trades_minute_data(
                              ticker_i, ticker_j, date, tau))

            except TypeError:
                pass

        # Saving data
        taq_data_tools_responses_event_trades_minute \
            .taq_save_data('{}_tau_{}'.format(function_name, tau), points,
                           ticker_i, ticker_j, year, '', '')

        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_event_trades_minute_data(ticker_i,
                                                                   ticker_j,
                                                                   year, tau):
    """Computes the average cross response of a year.

    Using the taq_cross_response_day_responses_event_trades_minute_data
    function computes the average cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = \
            taq_cross_response_year_avg_responses_event_trades_minute_data \
            .__name__
        taq_data_tools_responses_event_trades_minute \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        try:
            # Load data
            responses = pickle.load(open(''.join((
                    '../../taq_data/responses_event_trades_minute_data_{2}/taq'
                    + '_cross_response_year_responses_event_trades_minute_data'
                    + '_tau_{3}/taq_cross_response_year_responses_event_trades'
                    + '_minute_data_tau_{3}_{2}_{0}i_{1}j.pickle').split())
                    .format(ticker_i, ticker_j, year, tau), 'rb'))

            responses.sort(key=lambda tup: tup[0])
            res_list = [list(i) for i in zip(*responses)]
            rate = np.asarray(res_list[0])
            res = np.asarray(res_list[1])

            res_avg = []
            time = []
            avg_num = len(res)

            for i in range(1, 11):
                condition = rate == i
                if (np.sum(condition)):
                    res_avg.append(np.sum(res[condition]) / avg_num)
                    time.append(i)

            inter1 = list(range(10, 101, 10))
            for i, v in enumerate(inter1):
                if (v == 10):
                    pass
                else:
                    condition = (rate <= inter1[i]) \
                                * (rate > inter1[i - 1])
                    if (np.sum(condition)):
                        res_avg.append(np.sum(res[condition]) / avg_num)
                        time.append(v)

            inter2 = list(range(100, 1001, 100))
            for i, v in enumerate(inter2):
                if (v == 100):
                    pass
                else:
                    condition = (rate <= inter2[i]) \
                                * (rate > inter2[i-1])
                    if (np.sum(condition)):
                        res_avg.append(np.sum(res[condition]) / avg_num)
                        time.append(v)

            inter3 = list(range(1000, 10001, 1000))
            for i, v in enumerate(inter3):
                if (v == 1000):
                    pass
                else:
                    condition = (rate <= inter3[i]) \
                                * (rate > inter3[i-1])
                    if (np.sum(condition)):
                        res_avg.append(np.sum(res[condition]) / avg_num)
                        time.append(v)

        except TypeError as e:
            print(e)
            print(traceback.format_exc())
            pass

        assert len(res_avg) == len(time)

        # Saving data
        taq_data_tools_responses_event_trades_minute \
            .taq_save_data('{}_tau_{}'.format(function_name, tau),
                           (time, res_avg), ticker_i, ticker_j, year, '', '')

        return (time, res_avg)

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
