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

import taq_data_tools

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_trade_signs_responses_event_shift_data(ticker, date):
    """
    Obtain the trade signs from the TAQ data. The trade signs are calculated
    using the equation (1) of https://arxiv.org/pdf/1603.01580.pdf.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices. For further calculations we use the whole
    time range from the opening of the market at 9h40 to the closing at 15h50
    in seconds (22200 seconds).
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """''

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_trade_signs_responses_event_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Load data
        time_t, ask_t, _ = pickle.load(open(''.join((
            '../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_trades_{1}{2}{3}'
            + '.pickle').split())
            .format(ticker, year, month, day), 'rb'))

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        condition = (time_t >= 34801) * (time_t < 57000)

        time_t = time_t[condition]
        ask_t = ask_t[condition]

        # All the trades must have a price different to zero
        assert not np.sum(ask_t == 0)

        # Trades identified using equation (1)
        identified_trades = np.zeros(len(time_t))
        identified_trades[-1] = 1

        # Implementation of equation (1). Sign of the price change between
        # consecutive trades

        for t_idx, t_val in enumerate(time_t):

            diff = ask_t[t_idx] - ask_t[t_idx - 1]

            if (diff):

                identified_trades[t_idx] = np.sign(diff)

            else:

                identified_trades[t_idx] = identified_trades[t_idx - 1]

        # All the identified trades must be different to zero
        assert not np.sum(identified_trades == 0)

        # Saving data

        taq_data_tools.taq_save_data(function_name, (time_t, ask_t,
                                     identified_trades), ticker,
                                     ticker, year, month, day)

        return (time_t, ask_t, identified_trades)

    except FileNotFoundError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_event_shift_data(ticker, date, shift):
    """
    Obtain the self response function using the midpoint price returns
    and trade signs of the ticker during different time lags. Return an
    array with the self response for a day and an array of the number of
    trades for each value of tau.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_day_responses_event_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Load data
        midpoint_i = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_full_time_data/taq_midpoint_full_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        time_t, _, trade_sign_i = pickle.load(open("".join((
                '../../taq_data/responses_event_shift_data_{1}/taq_trade'
                + '_signs_responses_event_shift_data/taq_trade_signs'
                + '_responses_event_shift_data_{1}{2}{3}_{0}.pickle')
                .split())
                .format(ticker, year, month, day), 'rb'))
        # As the data is loaded from the original reproduction data from the
        # article, the data have a shift of 1 second. To correct this I made
        # both data to have the same time [34801, 56999]
        midpoint_i = midpoint_i[1:]
        time_m = np.array(range(34801, 57000))

        assert not np.sum(trade_sign_i == 0)
        assert not np.sum(midpoint_i == 0)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint log return and the self response function

        midpoint_t = 0. * trade_sign_i

        for t_idx, t_val in enumerate(time_m):
            condition = time_t == t_val
            len_c = np.sum(condition)
            midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

        assert not np.sum(midpoint_t == 0)

        # Depending on the tau value
        for tau_idx in range(__tau__):

            if (shift != 0):
                midpoint_shift = midpoint_t[:-shift]
                trade_sign_shift = trade_sign_i[shift:]
            else:
                midpoint_shift = midpoint_t
                trade_sign_shift = trade_sign_i

            trade_sign_tau = trade_sign_shift[:-tau_idx-1]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            num[tau_idx] = trade_sign_no_0_len
            # Obtain the midpoint log return. Displace the numerator tau
            # values to the right and compute the return

            # Midpoint price returns
            log_return_sec = (midpoint_shift[tau_idx + 1:]
                              - midpoint_shift[:-tau_idx - 1]) \
                / midpoint_shift[:-tau_idx - 1]

            # Obtain the self response value
            if (trade_sign_no_0_len != 0):
                product = log_return_sec * trade_sign_tau
                self_response_tau[tau_idx] = np.sum(product)

        return self_response_tau, num

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_event_shift_data(ticker, year, shift):
    """
    Obtain the year average self response function using the midpoint
    price returns and trade signs of the ticker during different time
    lags. Return an array with the year average self response.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    function_name = taq_self_response_year_responses_event_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '', '')

    dates = taq_data_tools.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:

            (data,
             avg_num) = taq_self_response_day_responses_event_shift_data(
                                ticker, date, shift)

            self_ += data

            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                 shift), self_ / num_s_t, ticker, ticker,
                                 year, '', '')

    return self_ / num_s_t, num_s_t

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_event_shift_data(ticker_i, ticker_j,
                                                      date, shift):
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

            function_name = taq_cross_response_day_responses_event_shift_data\
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
                '../../taq_data/responses_event_shift_data_{1}/taq_trade'
                + '_signs_responses_event_shift_data/taq_trade_signs'
                + '_responses_event_shift_data_{1}{2}{3}_{0}.pickle')
                .split())
                .format(ticker_j, year, month, day), 'rb'))

            # As the data is loaded from the original reproduction data from
            # the article, the data have a shift of 1 second. To correct this
            # I made both data to have the same time [34801, 56999]
            midpoint_i = midpoint_i[1:]
            time_m = np.array(range(34801, 57000))

            assert not np.sum(trade_sign_j == 0)
            assert not np.sum(midpoint_i == 0)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint log return and the cross response
            # function

            midpoint_t = 0. * trade_sign_j

            for t_idx, t_val in enumerate(time_m):
                condition = time_t == t_val
                len_c = np.sum(condition)
                midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

            assert not np.sum(midpoint_t == 0)

            # Depending on the tau value
            for tau_idx in range(__tau__):

                if (shift != 0):
                    midpoint_shift = midpoint_t[:-shift]
                    trade_sign_shift = trade_sign_j[shift:]
                else:
                    midpoint_shift = midpoint_t
                    trade_sign_shift = trade_sign_j

                trade_sign_tau = trade_sign_shift[:-tau_idx-1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len
                # Obtain the midpoint log return. Displace the numerator tau
                # values to the right and compute the return

                # Midpoint price returns

                log_return_sec = (midpoint_shift[tau_idx + 1:]
                                  - midpoint_shift[:-tau_idx - 1]) \
                    / midpoint_shift[:-tau_idx - 1]

                # Obtain the cross response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_sec * trade_sign_tau
                    cross_response_tau[tau_idx] = np.sum(product)

            return cross_response_tau, num

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_event_shift_data(ticker_i, ticker_j,
                                                       year, shift):
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

        function_name = taq_cross_response_year_responses_event_shift_data \
            .__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, '', '')

        dates = taq_data_tools.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:

                (data,
                 avg_num) = taq_cross_response_day_responses_event_shift_data(
                     ticker_i, ticker_j, date, shift)

                cross += data

                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data

        taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                     shift), cross / num_c_t, ticker_i,
                                     ticker_j, year, '', '')

        return cross / num_c_t, num_c_t
# ----------------------------------------------------------------------------
