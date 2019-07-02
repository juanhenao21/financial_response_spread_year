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


def taq_trade_signs_transactions_responses_data(ticker, date):
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

    function_name = taq_trade_signs_all_transactions_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Load data
        time_t, ask_t, _ = pickle.load(open(
            '../../taq_data/pickle_dayly_data_{1}/TAQ_{0}_trades_{1}{2}{3}.pickle'
            .format(ticker, year, month, day), 'rb'))

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        condition = (time_t >= 34801) * (time_t <= 57000)

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


def taq_self_response_day_transactions_responses_data(ticker, year, month, day,
                                        *, mod=__returns__, model=__case__):
    """
    Obtain the cross response function using the midpoint log returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each second. Return an array with the
    cross response function.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param mod='log': select the midpoint price return. 'ret' for midpoint
         price return and 'log' for midpoint price log return. Default 'log'
    """

    function_name = taq_self_response_transactions_data.__name__

    print('TAQ data')
    print(function_name)
    print('Processing data for the stock ' + ticker + ' the ' +
          year + '.' + month + '.' + day)

    midpoint_i = pickle.load(open(''.join((
                '../Cross_response_individual_stock/taq_data_{1}/taq_midpoint'
                + '_full_time_data/taq_midpoint_full_time_data_midpoint_{1}{2}'
                + '{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))

    if (model == 'juan'):
        time_m = np.array(range(34800, 57000))
    elif (model == 'wang'):
        time_m = np.array(range(34801, 57001))

    time_t, trade_sign_j = pickle.load(open("".join((
                '../Cross_response_individual_stock/taq_data_{1}/taq_trade_signs'
                + '_all_transactions_data_{4}/taq_trade_signs_all_transactions_data_{4}'
                + '_{1}{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day, model), 'rb'))

    assert not np.sum(trade_sign_j == 0)
    assert not np.sum(midpoint_i == 0)

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(__tau__)

    # Calculating the midpoint log return and the cross response function

    midpoint_t = 0. * trade_sign_j

    for t_idx, t_val in enumerate(time_m):
        condition = time_t == t_val
        len_c = np.sum(condition)
        midpoint_t[condition] = midpoint_i[t_idx] * np.ones(len_c)

    assert not np.sum(midpoint_t == 0)

    # Depending on the tau value
    for tau_idx in range(__tau__):

        trade_sign_tau = 1 * trade_sign_j[1:-tau_idx-1]
        trade_sign_no_0_len = len(trade_sign_tau)
        # Obtain the midpoint log return. Displace the numerator tau
        # values to the right and compute the return

        # midpoint price log returns
        if (mod == 'log'):
            log_return_i_sec = np.log(midpoint_t[tau_idx + 1: -1]
                                      / midpoint_t[:-tau_idx - 2])

        # midpoint price returns
        elif (mod == 'ret'):

            log_return_i_sec = (midpoint_t[tau_idx + 1: -1]
                                - midpoint_t[:-tau_idx - 2]) \
                / midpoint_t[:-tau_idx - 2]

        # Obtain the cross response value
        if (trade_sign_no_0_len != 0):
            product = log_return_i_sec * trade_sign_tau
            self_response_tau[tau_idx] = (np.sum(product)
                                           / trade_sign_no_0_len)

    if (not os.path.isdir('../Cross_response_individual_stock/taq_data_{1}/{0}/'
                          .format(function_name + '_' + mod + '_' + model, year))):

        try:

            os.mkdir('../Cross_response_individual_stock/taq_data_{1}/{0}/'.
                     format(function_name + '_' + mod + '_' + model, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    pickle.dump(self_response_tau, open(
        '../Cross_response_individual_stock/taq_data_{2}/{0}/{0}_{2}{3}{4}_{1}.pickle'
        .format(function_name + '_' + mod + '_' + model, ticker, year, month, day),
        'wb'))

    print('Data Saved')
    print()


    return self_response_tau

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_shift_data(ticker, date, shift, *,
                                               tau='off'):
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

    function_name = taq_self_response_day_responses_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

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

        # As the data is loaded from the original reproduction data from the
        # article, the data have a shift of 1 second. To correct this I made
        # both data to have the same time [34801, 56999]
        midpoint = midpoint[1:]
        trade_sign = trade_sign[:-1]

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint log return and the self response function

        # Depending on the tau value

        if (tau == 'off'):
            for tau_idx in range(__tau__):

                if (shift != 0):
                    midpoint_shift = midpoint[:-shift]
                    trade_sign_shift = trade_sign[shift:]
                else:
                    midpoint_shift = midpoint
                    trade_sign_shift = trade_sign

                trade_sign_tau = trade_sign_shift[:-tau_idx - 1]
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

        elif (tau == 'on'):
            for tau_idx in range(__tau__):

                midpoint_shift = midpoint[:-(tau_idx // 2) - 1]
                trade_sign_shift = trade_sign[tau_idx // 2 + 1:]

                assert len(midpoint_shift) == len(trade_sign_shift)

                trade_sign_tau = trade_sign_shift[:-tau_idx - 1]
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

    except FileNotFoundError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_shift_data(ticker, year, shift, *,
                                                tau='off'):
    """
    Obtain the year average self response function using the midpoint
    price returns and trade signs of the ticker during different time
    lags. Return an array with the year average self response.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    function_name = taq_self_response_year_responses_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '',
                                                  '')

    dates = taq_data_tools.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:

            (data,
             avg_num) = taq_self_response_day_responses_shift_data(ticker,
                                                                   date, shift,
                                                                   tau=tau)

            self_ += data

            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    if (tau == 'off'):
        taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                     shift), self_ / num_s_t, ticker, ticker,
                                     year, '', '')
    elif (tau == 'on'):
        taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                     'tau'), self_ / num_s_t, ticker, ticker,
                                     year, '', '')

    return self_ / num_s_t, num_s_t

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_shift_data(ticker_i, ticker_j, date,
                                                shift, *, tau='off'):
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

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        try:

            function_name = taq_cross_response_day_responses_shift_data. \
                            __name__
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

            # As the data is loaded from the original reproduction data from
            # the article, the data have a shift of 1 second. To correct this
            # I made both data to have the same time [34801, 56999]
            midpoint_i = midpoint_i[1:]
            trade_sign_j = trade_sign_j[:-1]

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function

            # Depending on the tau value

            if (tau == 'off'):
                for tau_idx in range(__tau__):

                    if (shift != 0):
                        midpoint_shift = midpoint_i[:-shift]
                        trade_sign_shift = trade_sign_j[shift:]
                    else:
                        midpoint_shift = midpoint_i
                        trade_sign_shift = trade_sign_j

                    trade_sign_tau = 1 * trade_sign_shift[:-tau_idx - 1]
                    trade_sign_no_0_len = len(
                                           trade_sign_tau[trade_sign_tau != 0])
                    num[tau_idx] = trade_sign_no_0_len
                    # Obtain the midpoint log return. Displace the numerator
                    # tau values to the right and compute the return

                    # Midpoint price returns
                    log_return_i_sec = (midpoint_shift[tau_idx + 1:]
                                        - midpoint_shift[:-tau_idx - 1]) \
                        / midpoint_shift[:-tau_idx - 1]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len != 0):
                        product = log_return_i_sec * trade_sign_tau
                        cross_response_tau[tau_idx] = np.sum(product)

            elif (tau == 'on'):
                for tau_idx in range(__tau__):

                    midpoint_shift = midpoint_i[:-(tau_idx // 2) - 1]
                    trade_sign_shift = trade_sign_j[tau_idx // 2 + 1:]

                    trade_sign_tau = 1 * trade_sign_shift[:-tau_idx - 1]
                    trade_sign_no_0_len = len(
                                          trade_sign_tau[trade_sign_tau != 0])
                    num[tau_idx] = trade_sign_no_0_len
                    # Obtain the midpoint log return. Displace the numerator
                    # tau values to the right and compute the return

                    # Midpoint price returns
                    log_return_i_sec = (midpoint_shift[tau_idx + 1:]
                                        - midpoint_shift[:-tau_idx - 1]) \
                        / midpoint_shift[:-tau_idx - 1]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len != 0):
                        product = log_return_i_sec * trade_sign_tau
                        cross_response_tau[tau_idx] = np.sum(product)

            return cross_response_tau, num

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_shift_data(ticker_i, ticker_j, year,
                                                 shift, *, tau='off'):
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

        function_name = taq_cross_response_year_responses_shift_data.__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, '',
                                                      '')

        dates = taq_data_tools.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:

                (data,
                 avg_num) = taq_cross_response_day_responses_shift_data(
                     ticker_i, ticker_j, date, shift, tau=tau)

                cross += data

                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        if (tau == 'off'):
            taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                         shift), cross / num_c_t, ticker_i,
                                         ticker_j, year, '', '')
        if (tau == 'on'):
            taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                         'tau'), cross / num_c_t, ticker_i,
                                         ticker_j, year, '', '')

        return cross / num_c_t, num_c_t

# ----------------------------------------------------------------------------
