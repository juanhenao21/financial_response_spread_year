'''
ITCH data generator

Module to compute the following data

- Midpoint price data: using the TAQ data obtain the best bid, best ask,
  quotes and midpoint price data.

- Trade signs data: using the TAQ data obtain the trade signs data.

- Self response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the self response of a stock.

- Self response absolute function: using the midpoint price and the trade
  signs calculate the midpoint log returns and the self response with the
  absolute value of the midpoint log returns of a stock.

- Cross response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the cross response between two
  stocks.

- Average return and average trade sign: using the midpoint price and the
  trade signs calculate the midpoint log returns and the response between the
  product of the averaged midpoint log returns and the averaged trade signs of
  two stocks.

- Difference cross response and average return and average trade sign: using
  the cross response and the average product calculate its difference.

- Zero correlation model: using the midpoint price of a stock and a random
  trade signs array calculate the midpoint log returns and the response
  between the midpoint log returns and the random array.

- Trade sign cross correlator: using the trade signs of two stocks calculate
  the trade sign cross correlator.

- Trade sign self correlator: using the trade signs of two stocks calculate
  the trade sign self correlator.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

import numpy as np
import os

import pickle

import taq_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------------------------------------------------


def taq_midpoint_data(ticker, year, month, day):
    """
    Obtain the midpoint price from the TAQ data. For further calculations
    we use the full time range from 9h40 to 15h50 in seconds (22200 seconds).
    To fill the time spaces when nothing happens we replicate
    the last value calculated until a change in the price happens. Save in a
    different pickle file the array of each of the following values: best bid,
    best ask, spread, midpoint price and time.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_midpoint_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data

    time_q, bid_q, ask_q = pickle.load(open(
        '../../TAQ_2008/TAQ_py/TAQ_{}_quotes_{}{}{}.pickle'
        .format(ticker, year, month, day), 'rb'))

    time_q = time_q[ask_q != 0.]
    bid_q = bid_q[bid_q != 0.]
    ask_q = ask_q[ask_q != 0.]

    assert len(bid_q) == len(ask_q)

    midpoint = (bid_q + ask_q) / 2
    spread = ask_q - bid_q

    # 34800 s = 9h40 - 57000 s = 15h50
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

    count = 0

    for t_idx, t_val in enumerate(full_time):

        if (count < len(time_q) and t_val == time_q[count]):

            count += 1

            while (count < len(time_q) and
                   time_q[count - 1] == time_q[count]):

                count += 1

            midpoint_last_val[t_idx] = midpoint[count - 1]
            ask_last_val[t_idx] = ask_q[count - 1]
            bid_last_val[t_idx] = bid_q[count - 1]
            spread_last_val[t_idx] = spread[count - 1]

        else:

            midpoint_last_val[t_idx] = midpoint_last_val[t_idx - 1]
            ask_last_val[t_idx] = ask_last_val[t_idx - 1]
            bid_last_val[t_idx] = bid_last_val[t_idx - 1]
            spread_last_val[t_idx] = spread_last_val[t_idx - 1]

    # The should not be 0 values in the midpoint array
    assert not len(midpoint_last_val[midpoint_last_val == 0])

    # Saving data

    if (not os.path.isdir('../taq_data_{1}/{0}/'.format(function_name, year))):

        os.mkdir('../taq_data_{1}/{0}/'.format(function_name, year))
        print('Folder to save data created')

    pickle.dump(ask_last_val,
                open('../taq_data_{2}/{0}/{0}_ask_{2}{3}{4}_{1}.pickle'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(bid_last_val,
                open('../taq_data_{2}/{0}/{0}_bid_{2}{3}{4}_{1}.pickle'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(spread_last_val,
                open('../taq_data_{2}/{0}/{0}_spread_{2}{3}{4}_{1}.pickle'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(full_time, open('../taq_data_{1}/{0}/{0}_time.pickle'
                                .format(function_name, year), 'wb'))
    pickle.dump(midpoint_last_val,
                open('../taq_data_{2}/{0}/{0}_midpoint_{2}{3}{4}_{1}.pickle'
                     .format(function_name, ticker, year, month, day), 'wb'))

    print('Data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_trade_signs_data(ticker, year, month, day):
    """
    Obtain the trade signs from the TAQ data. The trade signs are calculated
    using the equation (1) and (2) of https://arxiv.org/pdf/1603.01580.pdf.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices. For further calculations we use the whole
    time range from the opening of the market at 9h30 to the closing at 16h
    in seconds and then convert the values to hours (22200 seconds). To fill
    the time spaces when nothing happens we just fill with zeros indicating
    that there were neither a buy nor a sell. Save in a pickle file the array
    of the trade signs.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """''

    function_name = taq_trade_signs_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data

    time_t, ask_t = pickle.load(open(
        '../../TAQ_2008/TAQ_py/TAQ_{}_trades_{}{}{}.pickle'
        .format(ticker, year, month, day), 'rb'))

    time_t_set = np.array(sorted(set(time_t)))
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

    assert not len(identified_trades[identified_trades == 0])

    trades_exp_s = np.zeros(len(time_t_set))

    # Implementation of equation (2). Trade sign in each second
    for t_idx, t_val in enumerate(time_t_set):

        # Experimental
        trades_same_t_exp = identified_trades[time_t == t_val]
        sign_exp = np.sign(np.sum(trades_same_t_exp))
        trades_exp_s[t_idx] = sign_exp

    # 34800 s = 9h40 - 57000 s = 15h50
    full_time = np.array(range(34800, 57000))
    trade_signs = 0. * full_time

    count_full = 0

    for t_idx, t_val in enumerate(full_time):

        if (count_full < len(time_t_set) and t_val == time_t_set[count_full]):

            trade_signs[t_idx] = trades_exp_s[count_full]
            count_full += 1

    assert (len(trades_exp_s[trades_exp_s != 0])
            == len(trade_signs[trade_signs != 0]))

    # Saving data

    taq_data_tools.taq_save_data(function_name, trade_signs, ticker, ticker,
                                 year, month, day)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_self_response_data(ticker, year, month, day):
    """
    Obtain the self response function using the midpoint log returns
    and trade signs of the ticker during different time lags.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_self_response_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month,
                                                  day)

    # Load data
    midpoint = pickle.load(open(''.join((
            '../taq_data_{1}/taq_midpoint_data/taq_midpoint_data'
            + '_midpoint_{1}{2}{3}_{0}.pickle').split())
            .format(ticker, year, month, day), 'rb'))
    trade_sign = pickle.load(open("".join((
            '../taq_data_{1}/taq_trade_signs_data/taq_trade_signs'
            + '_data_{1}{2}{3}_{0}.pickle').split())
            .format(ticker, year, month, day), 'rb'))

    assert len(midpoint) == len(trade_sign)

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(__tau__)

    # Calculating the midpoint log return and the cross response function

    # Depending on the tau value
    for tau_idx in range(__tau__):

        # Obtain the midpoint log return. Displace the numerator tau
        # values to the right and compute the return, and append the
        # remaining values of tau with zeros

        log_return_sec = np.append(np.log(
            midpoint[tau_idx + 1:]/midpoint[:-tau_idx - 1]),
            np.zeros(tau_idx + 1))

        self_response_tau[tau_idx] = np.mean(
            log_return_sec[trade_sign != 0] *
            trade_sign[trade_sign != 0])

    # Saving data

    taq_data_tools.taq_save_data(function_name, self_response_tau,
                                   ticker, ticker, year, month, day)

    return self_response_tau

# -----------------------------------------------------------------------------------------------------------------------


def taq_cross_response_data(ticker_i, ticker_j, year, month, day):
    """
    Obtain the cross response function using the midpoint log returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each second
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """
    if (ticker_i == ticker_j):

        return None

    else:

        function_name = taq_cross_response_data.__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, month,
                                                      day)

        # Load data
        midpoint_i = pickle.load(open(''.join((
                '../taq_data_{1}/taq_midpoint_data/taq_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                .format(ticker_i, year, month, day), 'rb'))
        trade_sign_j = pickle.load(open("".join((
                '../taq_data_{1}/taq_trade_signs_data/taq_trade_signs'
                + '_data_{1}{2}{3}_{0}.pickle').split())
                .format(ticker_j, year, month, day), 'rb'))

        assert len(midpoint_i) == len(trade_sign_j)

        # Array of the average of each tau. 10^3 s used by Wang
        cross_response_tau = np.zeros(__tau__)

        # Calculating the midpoint log return and the cross response function

        # Depending on the tau value
        for tau_idx in range(__tau__):

            # Obtain the midpoint log return. Displace the numerator tau
            # values to the right and compute the return, and append the
            # remaining values of tau with zeros

            log_return_i_sec = np.append(np.log(
                midpoint_i[tau_idx + 1:]/midpoint_i[:-tau_idx - 1]),
                np.zeros(tau_idx + 1))

            cross_response_tau[tau_idx] = np.mean(
                log_return_i_sec[trade_sign_j != 0] *
                trade_sign_j[trade_sign_j != 0])

        # Saving data

        taq_data_tools.taq_save_data(function_name, cross_response_tau,
                                       ticker_i, ticker_j, year, month, day)

        return cross_response_tau


# -----------------------------------------------------------------------------------------------------------------------
