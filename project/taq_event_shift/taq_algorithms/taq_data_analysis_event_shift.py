'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * numpy
    * pandas
    * taq_data_tools_event_shift

The module contains the following functions:
    * taq_self_response_day_event_shift_data - computes the self response of a
      day.
    * taq_self_response_year_event_shift_data - computes the self response of
      a year.
    * taq_cross_response_day_event_shift_data - computes the cross response of
      a day.
    * taq_cross_response_year_event_shift_data - computes the cross response
      of a year.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_event_shift

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_day_event_shift_data(ticker, date, tau):
    """Computes the self response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different event shifts for a day. There is a constant
    :math:`\\tau` that most be set in the parameters.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_day_event_shift_data.__name__
    taq_data_tools_event_shift.taq_function_header_print_data(function_name,
                                                              ticker, ticker,
                                                              year, month, day)

    try:
        # Load data
        midpoint = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_time_data/taq_midpoint_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        time_t, _, trade_sign = pickle.load(open("".join((
                '../../taq_data/responses_event_shift_data_{1}/taq_trade'
                + '_signs_responses_event_shift_data/taq_trade_signs'
                + '_responses_event_shift_data_{1}{2}{3}_{0}.pickle')
                .split())
                .format(ticker, year, month, day), 'rb'))

        # As the data is loaded from the article reproduction module results,
        # the data have a shift of 1 second. To correct this I changed both
        # data to have the same time [34801, 56999]
        midpoint = midpoint[1:]
        time_m = np.array(range(34801, 57000))

        assert not np.sum(trade_sign == 0)
        assert not np.sum(midpoint == 0)

        # Array of the average of each tau. 10^3 s used by Wang
        shift_val = range(- 10 * tau, 10 * tau, 1)
        self_response_shift = np.zeros(len(shift_val))
        num = np.zeros(len(shift_val))

        # Calculating the midpoint price return and the self response function
        midpoint_t = 0. * trade_sign

        # It is needed to associate each trade sign with a midpoint price
        for t_idx, t_val in enumerate(time_m):
            condition = time_t == t_val
            len_c = np.sum(condition)
            midpoint_t[condition] = midpoint[t_idx] * np.ones(len_c)

        assert not np.sum(midpoint_t == 0)

        # Depending on the event shift value
        for s_idx, s_val in enumerate(shift_val):

            if (s_val < 0):
                midpoint_shift = midpoint_t[np.abs(s_val):]
                trade_sign_shift = trade_sign[:-np.abs(s_val)]

            elif (s_val > 0):
                midpoint_shift = midpoint_t[:-s_val]
                trade_sign_shift = trade_sign[s_val:]

            else:
                midpoint_shift = midpoint_t
                trade_sign_shift = trade_sign

            trade_sign_tau = trade_sign_shift[:-tau - 1]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            num[s_idx] = trade_sign_no_0_len

            # Obtain the midpoint price return. Displace the numerator tau
            # values to the right and compute the return

            # Midpoint price returns
            log_return_sec = (midpoint_shift[tau + 1:]
                              - midpoint_shift[:-tau - 1]) \
                / midpoint_shift[:-tau - 1]

            # Obtain the self response value
            if (trade_sign_no_0_len != 0):
                product = log_return_sec * trade_sign_tau
                self_response_shift[s_idx] = np.sum(product)

        return (self_response_shift, num)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_event_shift_data(ticker, year, tau):
    """Computes the self response of a year.

    Using the taq_self_response_day_event_shift_data function computes the
    self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_event_shift_data.__name__
    taq_data_tools_event_shift.taq_function_header_print_data(function_name,
                                                              ticker, ticker,
                                                              year, '', '')

    dates = taq_data_tools_event_shift.taq_bussiness_days(year)

    shift_val = range(- 10 * tau, 10 * tau, 1)
    self_ = np.zeros(len(shift_val))
    num_s = []

    for date in dates:

        try:
            data, avg_num = taq_self_response_day_event_shift_data(ticker,
                                                                   date, tau)
            self_ += data
            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    taq_data_tools_event_shift.taq_save_data('{}_tau_{}'.format(function_name,
                                             tau), self_ / num_s_t, ticker,
                                             ticker, year, '', '')

    return (self_ / num_s_t, num_s_t)

# ----------------------------------------------------------------------------


def taq_cross_response_day_event_shift_data(ticker_i, ticker_j, date, tau):
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
            function_name = taq_cross_response_day_event_shift_data.__name__
            taq_data_tools_event_shift \
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
            # results, the data have a shift of 1 second. To correct this
            # I changed both data to have the same time [34801, 56999]
            midpoint_i = midpoint_i[1:]
            time_m = np.array(range(34801, 57000))

            assert not np.sum(trade_sign_j == 0)
            assert not np.sum(midpoint_i == 0)

            # Array of the average of each tau. 10^3 s used by Wang
            shift_val = range(- 10 * tau, 10 * tau, 1)
            cross_response_shift = np.zeros(len(shift_val))
            num = np.zeros(len(shift_val))

            # Calculating the midpoint return and the cross response function
            midpoint_t = 0. * trade_sign_j

            # It is needed to associate each trade sign with a midpoint price
            for t_idx, t_val in enumerate(time_m):
                condition = time_t == t_val
                len_c = np.sum(condition)
                midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

            assert not np.sum(midpoint_t == 0)

            # Depending on the event shift value
            for s_idx, s_val in enumerate(shift_val):

                if (s_val < 0):
                    midpoint_shift = midpoint_t[np.abs(s_val):]
                    trade_sign_shift = trade_sign_j[:-np.abs(s_val)]

                elif (s_val > 0):
                    midpoint_shift = midpoint_t[:-s_val]
                    trade_sign_shift = trade_sign_j[s_val:]

                else:
                    midpoint_shift = midpoint_t
                    trade_sign_shift = trade_sign_j

                trade_sign_tau = 1 * trade_sign_shift[:-tau - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[s_idx] = trade_sign_no_0_len

                # Obtain the midpoint return. Displace the numerator tau
                # values to the right and compute the return

                # Midpoint price returns
                log_return_i_sec = (midpoint_shift[tau + 1:]
                                    - midpoint_shift[:-tau - 1]) \
                    / midpoint_shift[:-tau - 1]

                # Obtain the cross response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_i_sec * trade_sign_tau
                    cross_response_shift[s_idx] = np.sum(product)

            return (cross_response_shift, num)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_event_shift_data(ticker_i, ticker_j, year, tau):
    """Computes the cross response of a year.

    Using the taq_cross_response_day_event_shift_data function computes the
    cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Cross-response
        return None

    else:
        function_name = taq_cross_response_year_event_shift_data.__name__
        taq_data_tools_event_shift \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_event_shift.taq_bussiness_days(year)

        shift_val = range(- 10 * tau, 10 * tau, 1)
        cross = np.zeros(len(shift_val))
        num_c = []

        for date in dates:

            try:
                (data,
                 avg_num) = taq_cross_response_day_event_shift_data(ticker_i,
                                                                    ticker_j,
                                                                    date, tau)
                cross += data
                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        taq_data_tools_event_shift \
            .taq_save_data('{}_tau_{}'.format(function_name, tau),
                           cross / num_c_t, ticker_i, ticker_j, year, '', '')

        return (cross / num_c_t, num_c_t)

# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """
    import multiprocessing as mp
    from itertools import product

    taus = [1, 10, 100, 1000]
    year = '2008'

    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Especific functions
        pool.starmap(taq_self_response_year_event_shift_data,
                     product(['GS'], [year], taus))
        pool.starmap(taq_self_response_year_event_shift_data,
                     product(['JPM'], [year], taus))
        pool.starmap(taq_cross_response_year_event_shift_data,
                     product(['GS'], ['JPM'], [year], taus))
        pool.starmap(taq_cross_response_year_event_shift_data,
                     product(['JPM'], ['GS'], [year], taus))

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
