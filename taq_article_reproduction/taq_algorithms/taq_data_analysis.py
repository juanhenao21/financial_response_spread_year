'''
TAQ data analysis

Module to compute the following data

- Midpoint price data: using the TAQ data obtain the best bid, best ask,
  quotes and midpoint price data.

- Trade signs data: using the TAQ data obtain the trade signs data.

- Self response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the self response of a stock.

- Cross response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the cross response between two
  stocks.

- Trade sign self correlator: using the trade signs of two stocks calculate
  the trade sign self correlator.

- Trade sign cross correlator: using the trade signs of two stocks calculate
  the trade sign cross correlator.

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


def taq_data_extract(ticker, date):
    """
    Extract the trades and quotes (TAQ) data for a day, from a CSV file with
    the full information of a year. The time range for each day is from 9:30
    to 16:00 (including both).
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_data_extract.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

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
        with open(quotes_filename) as f_quotes:
            for idx, line in enumerate(f_quotes):
                list_line = line.split()
                if (list_line[0] == date
                        and list_line[1] >= '34200'
                        and list_line[1] <= '57600'):
                    quotes_day_list.append(list_line[:6])

        assert len(quotes_day_list) != 0

        with open(trades_filename) as f_trades:
            for idx, line in enumerate(f_trades):
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


def taq_midpoint_all_transactions_data(ticker, year, month, day):
    """
    Obtain the midpoint price from the TAQ data for all the transactions.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50 in transactions.
    Return best bid, best ask, spread, midpoint price and time.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')sys
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_midpoint_all_transactions_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

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

    return time_q, bid_q, ask_q, midpoint, spread

# ----------------------------------------------------------------------------


def taq_midpoint_full_time_data(ticker, date):
    """
    Obtain the midpoint price from the TAQ data for a complete day. For further
    calculations we use the full time range from 9h40 to 15h50 in seconds
    (22200 seconds). To fill the time spaces when nothing happens we replicate
    the last value calculated until a change in the price happens. Save in a
    different pickle file the array of each of the following values: best bid,
    best ask, spread, midpoint price and time. Return midpoint price array.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_midpoint_full_time_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Calculate the values of the midpoint price for all the transactions
        (time_q, bid_q, ask_q,
         midpoint, spread) = taq_midpoint_all_transactions_data(ticker, year,
                                                                month, day)

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

    except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_signs_all_transactions_data(ticker, year, month, day):
    """
    Obtain the trade signs from the TAQ data. The trade signs are calculated
    using the equation (1) of https://arxiv.org/pdf/1603.01580.pdf.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices. For further calculations we use the whole
    time range from the opening of the market at 9h30 to the closing at 16h00
    in transactions.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """''

    function_name = taq_trade_signs_all_transactions_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

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

    for t_idx, t_val in enumerate(time_t):

        diff = ask_t[t_idx] - ask_t[t_idx - 1]

        if (diff):

            identified_trades[t_idx] = np.sign(diff)

        else:

            identified_trades[t_idx] = identified_trades[t_idx - 1]

    # All the identified trades must be different to zero
    assert not np.sum(identified_trades == 0)

    return (time_t, ask_t, identified_trades)

# ----------------------------------------------------------------------------


def taq_trade_signs_full_time_data(ticker, date):
    """
    Obtain the trade signs from the TAQ data. The trade signs are calculated
    using the equation (2) and the identified trades obtained with equation (1)
    of https://arxiv.org/pdf/1603.01580.pdf.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices. For further calculations we use the whole
    time range from the opening of the market at 9h40 to the closing at 15h50
    in seconds (22200 seconds). To fill the time spaces when nothing happens
    we just add zeros indicating that there were neither a buy nor a sell. Save
    in a pickle file the array of the trade signs.
    Return the full time trade signs.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param identified_trades: array of the trade signs from all the
         transactions (i.e. numpy.array())
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_trade_signs_full_time_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Calculate the values of the trade signs for all the transactions
        (time_t, ask_t,
         identified_trades) = taq_trade_signs_all_transactions_data(ticker,
                                                                    year,
                                                                    month,
                                                                    day)

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        full_time = np.array(range(34801, 57001))

        trade_signs = 0. * full_time
        price_signs = 0. * full_time

        # Implementation of equation (2). Trade sign in each second
        for t_idx, t_val in enumerate(full_time):

            condition = (time_t >= t_val) \
                        * (time_t < t_val + 1)
            # Experimental
            trades_same_t_exp = identified_trades[condition]
            sign_exp = int(np.sign(np.sum(trades_same_t_exp)))
            trade_signs[t_idx] = sign_exp
            try:
                price_signs[t_idx] = ask_t[condition][-1]
            except IndexError:
                full_time[t_idx] = 0

        # Saving data

        taq_data_tools.taq_save_data(function_name, trade_signs, ticker,
                                     ticker, year, month, day)

        return (full_time, price_signs, trade_signs)

    except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_self_response_data(ticker, date):
    """
    Obtain the self response function using the midpoint log returns
    and trade signs of the ticker during different time lags. Return an
    array with the self response.
        :param ticker: string of the abbreviation of the midpoint stock to
        be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month,
                                                  day)

    try:

        # Load data
        midpoint = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_full_time_data/taq_midpoint_full_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        trade_sign = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_full_time_data/taq_trade_signs_full_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)

        # Calculating the midpoint log return and the self response function

        # Depending on the tau value
        for tau_idx in range(__tau__):

            trade_sign_tau = trade_sign[:-tau_idx - 1]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            # Obtain the midpoint log return. Displace the numerator tau
            # values to the right and compute the return

            # midpoint price returns

            log_return_sec = (midpoint[tau_idx + 1:]
                              - midpoint[:-tau_idx - 1]) \
                / midpoint[:-tau_idx - 1]

            # Obtain the self response value
            if (trade_sign_no_0_len != 0):
                product = log_return_sec * trade_sign_tau
                self_response_tau[tau_idx] = (np.sum(product)
                                              / trade_sign_no_0_len)

        # Saving data
        # midpoint price log returns
        taq_data_tools.taq_save_data(function_name, self_response_tau, ticker,
                                     ticker, year, month, day)

        return self_response_tau

    except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_data(ticker_i, ticker_j, date):
    """
    Obtain the cross response function using the midpoint log returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each second. Return an array with the
    cross response function.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
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

            function_name = taq_cross_response_data.__name__
            taq_data_tools.taq_function_header_print_data(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq'
                    + '_midpoint_full_time_data/taq_midpoint_full_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
            trade_sign_j = pickle.load(open("".join((
                    '../../taq_data/article_reproduction_data_2008/taq_trade_'
                    + 'signs_full_time_data/taq_trade_signs_full_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function

            # Depending on the tau value
            for tau_idx in range(__tau__):

                trade_sign_tau = 1 * trade_sign_j[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                # Obtain the midpoint log return. Displace the numerator tau
                # values to the right and compute the return

                log_return_i_sec = (midpoint_i[tau_idx + 1:]
                                    - midpoint_i[:-tau_idx - 1]) \
                    / midpoint_i[:-tau_idx - 1]

                # Obtain the cross response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_i_sec * trade_sign_tau
                    cross_response_tau[tau_idx] = (np.sum(product)
                                                   / trade_sign_no_0_len)

            # Saving data

            taq_data_tools.taq_save_data(function_name, cross_response_tau,
                                         ticker_i, ticker_j, year, month, day)

            return cross_response_tau

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_data(ticker, year, month, day):
    """
    Obtain the trade sign self correlator using the trade signs of ticker i
    during different time lags.
        :param ticker: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_trade_sign_self_correlator_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data
    trade_sign_i = pickle.load(open("".join((
                '../taq_data_{1}/taq_trade_signs_full_time_data/taq_trade'
                + '_signs_full_time_data_{1}{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))

    # Array of the average of each tau. 10^3 s used by Wang
    self_correlator = np.zeros(__tau__)

    # Calculating the midpoint log return and the trade sign cross-correlator

    for tau_idx in range(__tau__):

        trade_sign_tau = trade_sign_i[:-tau_idx - 1]
        trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])

        trade_sign_product = (trade_sign_i[tau_idx + 1:]
                              * trade_sign_i[:-tau_idx - 1])

        self_correlator[tau_idx] = (np.sum(trade_sign_product)
                                    / trade_sign_no_0_len)

    # Saving data

    taq_data_tools.taq_save_data(function_name, self_correlator, ticker,
                                 ticker, year, month, day)

    return self_correlator

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_data(ticker_i, ticker_j, year, month, day):
    """
    Obtain the trade sign cross correlator using the trade signs of ticker i
    and trade signs of ticker j during different time lags.
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        function_name = taq_trade_sign_cross_correlator_data.__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, month,
                                                      day)

        # Load data
        trade_sign_i = pickle.load(open("".join((
                    '../taq_data_{1}/taq_trade_signs_full_time_data/taq_trade'
                    + '_signs_full_time_data_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
        trade_sign_j = pickle.load(open("".join((
                    '../taq_data_{1}/taq_trade_signs_full_time_data/taq_trade'
                    + '_signs_full_time_data_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))

        # Array of the average of each tau. 10^3 s used by Wang
        cross_correlator = np.zeros(__tau__)

        # Calculating the midpoint log return and the trade sign
        # cross-correlator

        for tau_idx in range(__tau__):

            try:

                trade_sign_product = np.append(trade_sign_i[tau_idx:]
                                               * trade_sign_j[:-tau_idx],
                                               np.zeros(tau_idx))

            except ValueError:

                trade_sign_product = trade_sign_i * trade_sign_j

            cross_correlator[tau_idx] = np.mean(
                trade_sign_product[trade_sign_j != 0])

        # Saving data

        taq_data_tools.taq_save_data(function_name, cross_correlator, ticker_i,
                                     ticker_j, year, month, day)

        return cross_correlator

# ----------------------------------------------------------------------------
