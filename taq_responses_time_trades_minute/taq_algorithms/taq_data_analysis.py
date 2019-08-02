'''
TAQ data analysis

Module to compute the following data

- Trade signs all transactions: using the model obtain the trade signs
  for all the transactions in a day.

- Self response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the self response of a stock.

- Cross response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the cross response between two
  stocks.

Compare the differences between the two definitions of returns (midpoint price
returns and midpoint price log-returns).

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os

import pandas as pd
import pickle
import traceback
import taq_data_tools

__tau__ = 10000

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_time_trades_minute_data(ticker, date,
                                                             tau):
    """
    Obtain the self response function and the trades per minute using the
    midpoint price returns and trade signs of the ticker during different time
    lags. Return an array with the self response for a day and an array of the
    number of trades for a constant value of tau.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_day_responses_time_trades_minute_data. \
        __name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Load data
        midpoint = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_full_time_data/taq_midpoint_full_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        time_t, _, trade_sign = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_full_time_data/taq_trade_signs_full_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        # As the data is loaded from the original reproduction data from the
        # article, the data have a shift of 1 second.

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s used by Wang
        # List to save the tuples with the response and rates.
        points = []
        # Minutes during the open market considering opening at 9:40 and
        # closing at 15:50
        time_minutes = np.array(range(370))

        # Obtain the midpoint log return. Displace the numerator tau
        # values to the right and compute the return
        # Midpoint price returns
        log_return_sec = (midpoint[tau + 1:]
                          - midpoint[:-tau - 1]) \
            / midpoint[:-tau - 1]

        trade_sign_tau_ = trade_sign[:-tau - 1]
        time_t = time_t[:- tau - 1]

        assert len(trade_sign_tau_) == len(log_return_sec)

        # Depending on the tau value
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


def taq_self_response_year_responses_time_trades_minute_data(ticker, year,
                                                              tau):
    """
    Obtain the year average self response function using the midpoint
    price returns and trade signs of the ticker during different time
    lags. Return an array with the year average self response.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    function_name = \
        taq_self_response_year_responses_time_trades_minute_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '', '')

    dates = taq_data_tools.taq_bussiness_days(year)

    points = []

    for date in dates:

        try:

            points.extend(
                taq_self_response_day_responses_time_trades_minute_data(
                          ticker, date, tau))

        except TypeError:
            print('error')
            pass

    # Saving data
    taq_data_tools.taq_save_data('{}_tau_{}'.format(function_name, tau),
                                 points, ticker, ticker, year, '', '')

    return None

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_trades_minute_data(ticker, year,
                                                                  tau):
    """
    Load the list of tuples with the rate of trades per minute and the
    responses. Average the responses and return an array with the averaged
    responses.
        :param ticker: string of the abbreviation of the midpoint stock to
            be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param tau: int of the tau value to be analized (i. e. 50)
    """

    function_name = \
        taq_self_response_year_avg_responses_time_trades_minute_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '', '')

    try:

        # Load data
        responses = pickle.load(open(''.join((
                '../../taq_data/responses_time_trades_minute_data_{1}/taq'
                + '_self_response_year_responses_time_trades_minute_data'
                + '_tau_{2}/taq_self_response_year_responses_time_trades'
                + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
                .format(ticker, year, tau), 'rb'))

        responses.sort(key=lambda tup: tup[0])
        res_list = [list(i) for i in zip(*responses)]
        rate = np.asarray(res_list[0])
        res = np.asarray(res_list[1])

        res_avg = []
        time = []

        for i in range(1, 11):
            condition = rate == i
            if (np.sum(condition)):
                res_avg.append(np.mean(res[condition]))
                time.append(i)
        inter1 = list(range(10, 101, 10))
        for i, v in enumerate(inter1):
            if (v == 10):
                pass
            else:
                condition = (rate <= inter1[i]) \
                            * (rate > inter1[i - 1])
                if (np.sum(condition)):
                    res_avg.append(np.mean(res[condition]))
                    time.append(v)
        inter2 = list(range(100, 1001, 100))
        for i, v in enumerate(inter2):
            if (v == 100):
                pass
            else:
                condition = (rate <= inter2[i]) \
                            * (rate > inter2[i-1])
                if (np.sum(condition)):
                    res_avg.append(np.mean(res[condition]))
                    time.append(v)
        inter3 = list(range(1000, 10001, 1000))
        for i, v in enumerate(inter3):
            if (v == 1000):
                pass
            else:
                condition = (rate <= inter3[i]) \
                            * (rate > inter3[i-1])
                if (np.sum(condition)):
                    res_avg.append(np.mean(res[condition]))
                    time.append(v)

    except TypeError as e:
        print(e)
        print(traceback.format_exc())
        pass

    assert len(res_avg) == len(time)
    # Saving data
    taq_data_tools.taq_save_data('{}_tau_{}'.format(function_name, tau),
                                 (time, res_avg), ticker, ticker, year, '', '')

    return (time, res_avg)

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_trades_minute_data_v2(ticker,
                                                                     year, tau):
    """
    Load the list of tuples with the rate of trades per minute and the
    responses. Average the responses and return an array with the averaged
    responses.
        :param ticker: string of the abbreviation of the midpoint stock to
            be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param tau: int of the tau value to be analized (i. e. 50)
    """

    function_name = \
        taq_self_response_year_avg_responses_time_trades_minute_data_v2 \
            .__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '', '')

    try:

        # Load data
        responses = pickle.load(open(''.join((
                '../../taq_data/responses_time_trades_minute_data_{1}/taq'
                + '_self_response_year_responses_time_trades_minute_data'
                + '_tau_{2}/taq_self_response_year_responses_time_trades'
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
    taq_data_tools.taq_save_data('{}_tau_{}'.format(function_name, tau),
                                 (time, res_avg), ticker, ticker, year, '', '')

    return (time, res_avg)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_time_trades_minute_data(ticker_i,
                                                              ticker_j, date,
                                                              tau):
    """
    Obtain the cross response function using the midpoint price returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each second. Return an array with the
    cross response function for a day.
        :param ticker_i: string of the abbreviation of the midpoint stock to
            be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
            be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
            (i.e. '2008-01-02')
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        try:

            date_sep = date.split('-')

            year = date_sep[0]
            month = date_sep[1]
            day = date_sep[2]

            function_name = \
                taq_cross_response_day_responses_time_trades_minute_data \
                .__name__
            taq_data_tools.taq_function_header_print_data(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq'
                    + '_midpoint_full_time_data/taq_midpoint_full_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))

            time_t, _, trade_sign_j = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_full_time_data/taq_trade_signs_full_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker_j, year, month, day), 'rb'))

            # As the data is loaded from the original reproduction data from
            # the article, the data have a shift of 1 second.

            assert len(midpoint_i) == len(trade_sign_j)

            # List to save the tuples with the response and rates
            points = []
            # Minutes during the open market considering opening at 9:40 and
            # closing at 15:50
            time_minutes = np.array(range(370))

            # Obtain the midpoint log return. Displace the numerator tau
            # values to the right and compute the return
            # Midpoint price returns
            log_return_sec = (midpoint_i[tau + 1:]
                              - midpoint_i[:-tau - 1]) \
                / midpoint_i[:-tau - 1]

            trade_sign_tau_ = trade_sign_j[:-tau - 1]
            time_t = time_t[:- tau - 1]

            assert len(trade_sign_tau_) == len(log_return_sec)

            # Depending on the tau value
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


def taq_cross_response_year_responses_time_trades_minute_data(ticker_i,
                                                               ticker_j, year,
                                                               tau):
    """
    Obtain the year average cross response function using the midpoint
    price returns and trade signs of the tickers during different time
    lags. Return an array with the year average cross response.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        function_name = \
            taq_cross_response_year_responses_time_trades_minute_data \
            .__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, '', '')

        dates = taq_data_tools.taq_bussiness_days(year)

        points = []

        for date in dates:

            try:

                points.extend(
                    taq_cross_response_day_responses_time_trades_minute_data(
                              ticker_i, ticker_j, date, tau))

            except TypeError:
                pass

        # Saving data
        taq_data_tools.taq_save_data('{}_tau_{}'.format(function_name, tau),
                                     points, ticker_i, ticker_j, year, '', '')

        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_trades_minute_data_v2(ticker_i,
                                                                      ticker_j,
                                                                      year,
                                                                      tau):
    """
    Load the list of tuples with the rate of trades per minute and the
    responses. Average the responses and return an array with the averaged
    responses.
        :param ticker_i: string of the abbreviation of the midpoint stock to
            be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
            be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param tau: int of the tau value to be analized (i. e. 50)
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        function_name = \
            taq_cross_response_year_avg_responses_time_trades_minute_data_v2 \
            .__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, '', '')

        try:

            # Load data
            responses = pickle.load(open(''.join((
                    '../../taq_data/responses_time_trades_minute_data_{2}/taq'
                    + '_cross_response_year_responses_time_trades_minute_data'
                    + '_tau_{3}/taq_cross_response_year_responses_time_trades'
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
        taq_data_tools.taq_save_data('{}_tau_{}'.format(function_name, tau),
                                    (time, res_avg), ticker_i, ticker_j, year, '', '')

        return (time, res_avg)

# ----------------------------------------------------------------------------


def main():

    ticker = 'AAPL'
    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    year = '2008'
    tau = 50

    x, y = \
     taq_cross_response_year_avg_responses_time_trades_minute_data_v2(ticker_i, ticker_j,
                                                                   year, tau)

    print(x)
    print(y)


if __name__ == "__main__":
    main()
