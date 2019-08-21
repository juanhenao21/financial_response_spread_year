'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions and the trade sign self- and
cross-correlator functions.

This script requires the following modules:
    * numpy
    * pandas
    * taq_data_tools_article_reproduction

The module contains the following functions:
    * taq_data_extract - extracts the data for every day in a year.
    * taq_midpoint_event_data - computes the midpoint price of every event.
    * taq_midpoint_time_data - computes the midpoint price of every second.
    * taq_trade_signs_event_data - computes the trade signs of every event.
    * taq_trade_signs_time_data - computes the trade signs of every second.
    * taq_self_response_day_data - computes the self response of a day.
    * taq_self_response_year_data - computes the self response of a year.
    * taq_cross_response_day_data - computes the cross response of a day.
    * taq_cross_response_year_data - computes the cross response of a year.
    * taq_trade_sign_self_correlator_day_data - computes the trade sign self
      correlator of a day.
    * taq_trade_sign_self_correlator_year_data - computes the trade sign self
      correlator of a year.
    * taq_trade_sign_cross_correlator_day_data - computes the trade sign cross
      correlator of a day.
    * taq_trade_sign_cross_correlator_year_data - computes the trade sign cross
      correlator of a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_article_reproduction

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_data_extract(ticker, date):
    """Extracts the data for every day in a year.

    Extracts the trades and quotes (TAQ) data for a day from a CSV file with
    the information of a whole year. The time range for each day is from 9:30
    to 16:00, that means, the open market time.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function return a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_data_extract.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:

        # Load data
        # Date of the day to be saved
        date = '{}-{}-{}'.format(year, month, day)
        quotes_filename = ''.join(('../../taq_data/csv_year_data_{1}/{0}_{1}'
                                   + '_NASDAQ_quotes.csv')
                                  .split()).format(ticker, year)
        trades_filename = ''.join(('../../taq_data/csv_year_data_{1}/{0}_{1}'
                                   + '_NASDAQ_trades.csv')
                                  .split()).format(ticker, year)
        quotes_day_list = []
        trades_day_list = []

        # Read line per line
        # Quotes
        with open(quotes_filename) as f_quotes:
            for line in f_quotes:
                list_line = line.split()
                if (list_line[0] == date
                        and list_line[1] >= '34200'
                        and list_line[1] <= '57600'):
                    quotes_day_list.append(list_line[:6])

        assert len(quotes_day_list) != 0

        # Trades
        with open(trades_filename) as f_trades:
            for line in f_trades:
                list_line = line.split()
                if (list_line[0] == date
                        and list_line[1] >= '34200'
                        and list_line[1] <= '57600'):
                    trades_day_list.append(list_line[:4])

        assert len(trades_day_list) != 0

        # Pandas dataframes with the filtered data
        quotes_df = pd.DataFrame(quotes_day_list,
                                 columns=['Date', 'Time', 'Bid', 'Ask',
                                          'Vol_Bid', 'Vol_Ask'])
        trades_df = pd.DataFrame(trades_day_list,
                                 columns=['Date', 'Time', 'Ask', 'Vol_Ask'])

        # Dataframes to arrays
        time_q = np.array(quotes_df['Time']).astype(int)
        bid_q = np.array(quotes_df['Bid']).astype(int)
        ask_q = np.array(quotes_df['Ask']).astype(int)
        vol_bid_q = np.array(quotes_df['Vol_Bid']).astype(int)
        vol_ask_q = np.array(quotes_df['Vol_Ask']).astype(int)

        time_t = np.array(trades_df['Time']).astype(int)
        ask_t = np.array(trades_df['Ask']).astype(int)
        vol_ask_t = np.array(trades_df['Vol_Ask']).astype(int)

        # Save data
        if (not os.path.isdir('../../taq_data/pickle_dayly_data_{}/'
                              .format(year))):

            try:
                os.mkdir('../../taq_data/pickle_dayly_data_{}/'.format(year))
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        pickle.dump((time_q, bid_q, ask_q, vol_bid_q, vol_ask_q),
                    open(''.join(('../../taq_data/pickle_dayly_data_2008/'
                         + 'TAQ_{0}_quotes_{1}{2}{3}.pickle').split())
                         .format(ticker, year, month, day), 'wb'))

        pickle.dump((time_t, ask_t, vol_ask_t),
                    open(''.join(('../../taq_data/pickle_dayly_data_2008/'
                         + 'TAQ_{0}_trades_{1}{2}{3}.pickle').split())
                         .format(ticker, year, month, day), 'wb'))

        print('Data Saved')
        print()

        return (time_q, bid_q, ask_q, vol_bid_q, vol_ask_q,
                time_t, ask_t, vol_ask_t)

    except AssertionError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_midpoint_event_data(ticker, year, month, day):
    """Computes the midpoint price of every event.

    Using the dayly TAQ data computes the midpoint price of every event in a
    day.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param month: string of the month to be analized (i.e '07').
    :param day: string of the day to be analized (i.e '07').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_midpoint_event_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    # Load data
    # TAQ data gives directly the quotes data in every second that there is
    # a change in the quotes
    time_q_, bid_q_, ask_q_, _, _ = pickle.load(open(
        '../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_quotes_{1}{2}{3}.pickle'
        .format(ticker, year, month, day), 'rb'))

    # Some files are corrupted, so there are some zero values that
    # does not have sense
    condition_1 = ask_q_ != 0.
    time_q = time_q_[condition_1]
    bid_q = bid_q_[condition_1]
    ask_q = ask_q_[condition_1]

    assert len(bid_q) == len(ask_q)

    midpoint = (bid_q + ask_q) / 2
    spread = ask_q - bid_q

    return (time_q, bid_q, ask_q, midpoint, spread)

# ----------------------------------------------------------------------------


def taq_midpoint_time_data(ticker, date):
    """Computes the midpoint price of every second.

    Using the taq_midpoint_event_data function computes the midpoint price of
    every second. To fill the time spaces when nothing happens I replicate the
    last value calculated until a change in the price happens.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: numpy array.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_midpoint_time_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Calculate the values of the midpoint price for all the events
        (time_q, bid_q, ask_q,
         midpoint, spread) = taq_midpoint_event_data(ticker, year, month, day)

        # 34800 s = 9h40 - 57000 s = 15h50
        # Reproducing S. Wang values. In her results the time interval for the
        # midpoint is [34800, 56999]
        full_time = np.array(range(34800, 57000))

        # As there can be several values for the same second, we use the
        # last value of each second in the full time array as it behaves
        # quiet equal as the original input

        midpoint_last_val = 0. * full_time
        midpoint_last_val[-1] = midpoint[0]

        ask_last_val = 0. * full_time
        ask_last_val[-1] = ask_q[0]

        bid_last_val = 0. * full_time
        bid_last_val[-1] = bid_q[0]

        spread_last_val = 0. * full_time
        spread_last_val[-1] = spread[0]

        for t_idx, t_val in enumerate(full_time):

            condition = time_q == t_val

            if (np.sum(condition)):

                midpoint_last_val[t_idx] = midpoint[condition][-1]
                ask_last_val[t_idx] = ask_q[condition][-1]
                bid_last_val[t_idx] = bid_q[condition][-1]
                spread_last_val[t_idx] = spread[condition][-1]

            else:

                midpoint_last_val[t_idx] = midpoint_last_val[t_idx - 1]
                ask_last_val[t_idx] = ask_last_val[t_idx - 1]
                bid_last_val[t_idx] = bid_last_val[t_idx - 1]
                spread_last_val[t_idx] = spread_last_val[t_idx - 1]

        # There should not be 0 values in the midpoint array
        assert not np.sum(midpoint_last_val == 0)

        # Saving data

        if (not os.path.isdir(''.join(('../../taq_data/article_reproduction'
                                       + '_data_{1}/{0}/').split())
                              .format(function_name, year))):

            os.mkdir('../../taq_data/article_reproduction_data_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        pickle.dump(ask_last_val / 10000,
                    open(''.join((
                         '../../taq_data/article_reproduction_data_{2}/{0}/'
                         + '{0}_ask_{2}{3}{4}_{1}.pickle').split())
                         .format(function_name, ticker, year, month, day),
                         'wb'))
        pickle.dump(bid_last_val / 10000,
                    open(''.join((
                         '../../taq_data/article_reproduction_data_{2}/{0}/{0}'
                         + '_bid_{2}{3}{4}_{1}.pickle').split())
                         .format(function_name, ticker, year, month, day),
                         'wb'))
        pickle.dump(spread_last_val / 10000,
                    open(''.join((
                         '../../taq_data/article_reproduction_data_{2}/{0}/{0}'
                         + '_spread_{2}{3}{4}_{1}.pickle').split())
                         .format(function_name, ticker, year, month, day),
                         'wb'))
        pickle.dump(full_time,
                    open(''.join((
                         '../../taq_data/article_reproduction_data_{1}/{0}/{0}'
                         + '_time.pickle').split())
                         .format(function_name, year), 'wb'))
        pickle.dump(midpoint_last_val / 10000,
                    open(''.join((
                         '../../taq_data/article_reproduction_data_{2}/{0}/{0}'
                         '_midpoint_{2}{3}{4}_{1}.pickle').split())
                         .format(function_name, ticker, year, month, day),
                         'wb'))

        print('Data saved')
        print()

        return midpoint_last_val

    except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_signs_event_data(ticker, year, month, day):
    """Computes the trade signs of every event.

    Using the dayly TAQ data computes the trade signs of every event in a day.
    The trade signs are computed using the equation (1) of the
    `paper <https://arxiv.org/pdf/1603.01580.pdf>`_.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.

    :param ticker: string of the abbreviation of the stock to be analized
        (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param month: string of the month to be analized (i.e '07').
    :param day: string of the day to be analized (i.e '07').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_trade_signs_event_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    # Load data
    time_t, ask_t, _ = pickle.load(open(
        '../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_trades_{1}{2}{3}.pickle'
        .format(ticker, year, month, day), 'rb'))

    # All the trades must have a price different to zero
    assert not np.sum(ask_t == 0)

    # Trades identified using equation (1)
    identified_trades = np.zeros(len(time_t))
    identified_trades[-1] = 1

    # Implementation of equation (1). Sign of the price change between
    # consecutive trades

    for t_idx in range(len(time_t)):

        diff = ask_t[t_idx] - ask_t[t_idx - 1]

        if (diff):
            identified_trades[t_idx] = np.sign(diff)

        else:
            identified_trades[t_idx] = identified_trades[t_idx - 1]

    # All the identified trades must be different to zero
    assert not np.sum(identified_trades == 0)

    return (time_t, ask_t, identified_trades)

# ----------------------------------------------------------------------------


def taq_trade_signs_time_data(ticker, date):
    """Computes the trade signs of every second.

    Using the taq_trade_signs_event_data function computes the trade signs of
    every second.
    The trade signs are computed using the equation (2) of the
    `paper <https://arxiv.org/pdf/1603.01580.pdf>`_.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.
    To fill the time spaces when nothing happens I added zeros indicating that
    there were neither a buy nor a sell.

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

    function_name = taq_trade_signs_time_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Calculate the values of the trade signs for all the events
        (time_t, ask_t,
         identified_trades) = taq_trade_signs_event_data(ticker, year, month,
                                                         day)

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        full_time = np.array(range(34801, 57001))

        trade_signs = 0. * full_time
        price_signs = 0. * full_time

        # Implementation of equation (2). Trade sign in each second
        for t_idx, t_val in enumerate(full_time):

            condition = (time_t >= t_val) * (time_t < t_val + 1)
            # Empirical
            trades_same_t_exp = identified_trades[condition]
            sign_exp = int(np.sign(np.sum(trades_same_t_exp)))
            trade_signs[t_idx] = sign_exp
            try:
                price_signs[t_idx] = ask_t[condition][-1]
            except IndexError as e:
                full_time[t_idx] = 0

        # Saving data
        taq_data_tools_article_reproduction \
            .taq_save_data(function_name,
                           (full_time, price_signs, trade_signs),
                           ticker, ticker, year, month, day)

        return (full_time, price_signs, trade_signs)

    except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_self_response_day_data(ticker, date):
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

    function_name = taq_self_response_day_data.__name__
    taq_data_tools_article_reproduction \
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

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint price return and the self response function

        # Depending on the tau value
        for tau_idx in range(__tau__):

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


def taq_self_response_year_data(ticker, year):
    """Computes the self response of a year.

    Using the taq_self_response_day_data function computes the self-response
    function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_article_reproduction.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:
            data, avg_num = taq_self_response_day_data(ticker, date)
            self_ += data
            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    taq_data_tools_article_reproduction \
        .taq_save_data(function_name, self_ / num_s_t, ticker, ticker, year,
                       '', '')

    return (self_ / num_s_t, num_s_t)

# ----------------------------------------------------------------------------


def taq_cross_response_day_data(ticker_i, ticker_j, date):
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
            function_name = taq_cross_response_day_data.__name__
            taq_data_tools_article_reproduction \
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


def taq_cross_response_year_data(ticker_i, ticker_j, year):
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
        function_name = taq_cross_response_year_data.__name__
        taq_data_tools_article_reproduction \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_article_reproduction.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:
                data, avg_num = taq_cross_response_day_data(ticker_i, ticker_j,
                                                            date)

                cross += data
                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        # midpoint price returns
        taq_data_tools_article_reproduction \
            .taq_save_data(function_name, cross / num_c_t, ticker_i, ticker_j,
                           year, '', '')

        return (cross / num_c_t, num_c_t)

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_day_data(ticker, date):
    """Computes the trade sign self correlator of a year.

    Using the trade signs of a ticker computes the self-correlator during
    different time lags (:math:`\tau`) for a day.

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

    function_name = taq_trade_sign_self_correlator_day_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        _, _, trade_sign_i = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_time_data/taq_trade_signs_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))

        # Array of the average of each tau. 10^3 s used by Wang
        self_correlator = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the trade sign cross-correlator
        for tau_idx in range(__tau__):

            trade_sign_tau = trade_sign_i[:-tau_idx - 1]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            num[tau_idx] = trade_sign_no_0_len

            trade_sign_product = (trade_sign_i[tau_idx + 1:]
                                  * trade_sign_i[:-tau_idx - 1])

            self_correlator[tau_idx] = np.sum(trade_sign_product)

        return (self_correlator, num)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_year_data(ticker, year):
    """Computes the trade sign self correlator of a year.

    Using the taq_trade_sign_self_correlator_day_data function computes the
    self correlator function for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_trade_sign_self_correlator_year_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_article_reproduction.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:
            (data,
             avg_num) = taq_trade_sign_self_correlator_day_data(ticker, date)

            self_ += data
            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    taq_data_tools_article_reproduction \
        .taq_save_data(function_name, self_ / num_s_t, ticker, ticker, year,
                       '', '')

    return (self_ / num_s_t, num_s_t)

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_day_data(ticker_i, ticker_j, date):
    """Computes the trade sign cross correlator of a day.

    Using the trade signs of ticker i and trade signs of ticker j computes the
    cross-correlator during different time lags (:math:`\tau`).

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02).
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
            function_name = taq_trade_sign_cross_correlator_day_data.__name__
            taq_data_tools_article_reproduction \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            _, _, trade_sign_i = pickle.load(open("".join((
                    '../../taq_data/article_reproduction_data_2008/taq_trade_'
                    + 'signs_time_data/taq_trade_signs_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
            _, _, trade_sign_j = pickle.load(open("".join((
                    '../../taq_data/article_reproduction_data_2008/taq_trade_'
                    + 'signs_time_data/taq_trade_signs_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))

            # Array of the average of each tau. 10^3 s used by Wang
            cross_correlator = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the trade sign cross-correlator
            for tau_idx in range(__tau__):

                trade_sign_tau = 1 * trade_sign_j[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len

                trade_sign_product = (trade_sign_i[tau_idx + 1:]
                                      * trade_sign_j[:-tau_idx - 1])

                cross_correlator[tau_idx] = np.sum(trade_sign_product)

            return (cross_correlator, num)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_year_data(ticker_i, ticker_j, year):
    """Computes the trade sign cross correlator of a year.

    Using the taq_trade_sign_cross_correlator_day_data function computes the
    cross-correlator function for a year.

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
        function_name = taq_trade_sign_cross_correlator_year_data.__name__
        taq_data_tools_article_reproduction \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_article_reproduction.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:
                (data,
                 avg_num) = taq_trade_sign_cross_correlator_day_data(ticker_i,
                                                                     ticker_j,
                                                                     date)

                cross += data
                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        taq_data_tools_article_reproduction \
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
