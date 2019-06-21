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

import taq_data_tools_comp

__tau__ = 1000
__n_path__ = '../'

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
    taq_data_tools_comp.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data
    # TAQ data gives directly the quotes data in every second that there is
    # a change in the quotes
    time_q_, bid_q_, ask_q_, _, _ = pickle.load(open(
        '{4}../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_quotes_{1}{2}{3}.pickle'
        .format(ticker, year, month, day, __n_path__), 'rb'))

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
    taq_data_tools_comp.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data

    time_t, ask_t, _ = pickle.load(open(
        '{4}../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_trades_{1}{2}{3}.pickle'
        .format(ticker, year, month, day, __n_path__), 'rb'))

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
    taq_data_tools_comp.taq_function_header_print_data(function_name, ticker,
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
        taq_data_tools_comp.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, month,
                                                      day)

        # Load data
        trade_sign_i = pickle.load(open("".join((
                    '{4}../../taq_data_{1}/taq_trade_signs_full_time_data/taq_trade'
                    + '_signs_full_time_data_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
        trade_sign_j = pickle.load(open("".join((
                    '{4}../../taq_data_{1}/taq_trade_signs_full_time_data/taq_trade'
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

        return cross_correlator

# ----------------------------------------------------------------------------
