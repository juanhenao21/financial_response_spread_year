'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions and the trade sign self- and
cross-correlator functions. This module reproduces the sections 3.1 and 3.2 of
the `paper
<https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.


This script requires the following modules:
    * itertools.product
    * multiprocessing
    * numpy
    * os
    * pandas
    * pickle
    * taq_data_tools_responses_physical

The module contains the following functions:
    * taq_data_extract - extracts the data for every day in a year.
    * taq_midpoint_trade_data - computes the midpoint price of every trade.
    * taq_midpoint_physical_data - computes the midpoint price of every second.
    * taq_trade_signs_trade_data - computes the trade signs of every trade.
    * taq_trade_signs_physical_data - computes the trade signs of every second.
    * taq_self_response_day_responses_physical_data - computes the self
      response of a day.
    * taq_self_response_year_responses_physical_data - computes the self
      response of a year.
    * taq_cross_response_day_responses_physical_data - computes the cross
      response of a day.
    * taq_cross_response_year_responses_physical_data - computes the cross
      response of a year.
    * taq_trade_sign_self_correlator_day_responses_physical_data - computes the
      trade sign self correlator of a day.
    * taq_trade_sign_self_correlator_year_responses_physical_data - computes
      the trade sign self correlator of a year.
    * taq_trade_sign_cross_correlator_day_responses_physical_data - computes
      the trade sign cross correlator of a day.
    * taq_trade_sign_cross_correlator_year_responses_physical_data - computes
      the trade sign cross correlator of a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_responses_physical

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_data_extract(ticker, type, year):
    """Extracts the data for every day in a year.

    Extracts the trades and quotes (TAQ) data for a day from a CSV file with
    the information of a whole year. The time range for each day is from 9:30
    to 16:00, that means, the open market time.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param type: string with the type of the data to be extracted
     (i.e. 'trades' or 'quotes').
    :param year: string of the year to be analyzed (i.e. '2016').
    :return: None -- The function extracts the data and does not return a
     value.
    """

    function_name = taq_data_extract.__name__
    taq_data_tools_responses_physical \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    try:

        df = pd.DataFrame()
        chunksize = 10 ** 7

        date_list = taq_data_tools_responses_physical.taq_bussiness_days(year)

        # Load data
        csv_file = f'../../taq_data/csv_year_data_{year}/{ticker}_{year}' + \
            f'_NASDAQ_{type}.csv'

        df_type = {'quotes': {
                        'Date': 'str',
                        'Time': 'int',
                        'Bid': 'int',
                        'Ask': 'int',
                        'Vol_Bid': 'int',
                        'Vol_Ask': 'int',
                        'Mode': 'int',
                        'Cond': 'str',
                    },
                   'trades': {
                        'Date': 'str',
                        'Time': 'int',
                        'Ask': 'int',
                        'Vol_Ask': 'int',
                        'Mode': 'int',
                        'Corr': 'int',
                        'Cond': 'str',
                    }}

        col_names = {'quotes': ['Date', 'Time', 'Bid', 'Ask', 'Vol_Bid',
                                'Vol_Ask', 'Mode', 'Cond'],
                     'trades': ['Date', 'Time', 'Ask', 'Vol_Ask', 'Mode',
                                'Corr', 'Cond']}

        # Save data
        if (not os.path.isdir(f'../../taq_data/hdf5_daily_data_{year}/')):

            try:
                os.mkdir(f'../../taq_data/hdf5_daily_data_{year}/')
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        for chunk in pd.read_csv(csv_file, chunksize=chunksize, sep='\s+',
                                 names=col_names[type], dtype=df_type[type],
                                 na_filter=False, low_memory=False):

            chunk['Date'] = pd.to_datetime(chunk['Date'], format='%Y-%m-%d')
            chunk.set_index('Date', inplace=True)
            if (type == 'quotes'):
                chunk.drop(['Mode', 'Cond'], axis=1, inplace=True)
            else:
                chunk.drop(['Mode', 'Corr', 'Cond'], axis=1, inplace=True)

            for date in date_list:
                day = chunk.index.isin([date])
                df = chunk.loc[day & (chunk['Time'] >= 34200)
                               & (chunk['Time'] < 57600)]

                if not df.empty:
                    df.to_hdf(f'../../taq_data/hdf5_daily_data_{year}/taq_'
                              + f'{ticker}_{type}_{date}.h5', key=type,
                              format='table', append=True)

        print('Data Saved')
        print()

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_midpoint_trade_data(ticker, date):
    """Computes the midpoint price of every trade.

    Using the daily TAQ data computes the midpoint price of every trade in a
    day. For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:
        # Load data
        # The module is used in other folders, so it is necessary to use
        # absolute paths instead of relative paths
        # Obtain the absolut path of the current file and split it
        abs_path = os.path.abspath(__file__).split('/')
        # Take the path from the start to the project folder
        root_path = '/'.join(abs_path[:abs_path.index('project') + 1])
        data_quotes_trade = pd.read_hdf(root_path
                                        + f'/taq_data/hdf5_daily_data_{year}/'
                                        + f'taq_{ticker}_quotes_{date}.h5',
                                        key='/quotes')

        time_q = data_quotes_trade['Time'].to_numpy()
        bid_q = data_quotes_trade['Bid'].to_numpy()
        ask_q = data_quotes_trade['Ask'].to_numpy()

        # Some files are corrupted, so there are some zero values that does not
        # have sense
        condition = ask_q != 0
        time_q = time_q[condition]
        bid_q = bid_q[condition]
        ask_q = ask_q[condition]

        midpoint = (bid_q + ask_q) / 2

        return (time_q, midpoint)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_midpoint_physical_data(ticker, date):
    """Computes the midpoint price of every second.

    Using the taq_midpoint_trade_data function computes the midpoint price of
    every second. To fill the time spaces when nothing happens I replicate the
    last value calculated until a change in the price happens.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: numpy array.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_midpoint_physical_data.__name__
    taq_data_tools_responses_physical \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Calculate the values of the midpoint price for all the events
        time_q, midpoint_trade = taq_midpoint_trade_data(ticker, date)

        # 34800 s = 9h40 - 57000 s = 15h50
        # Reproducing the paper time values. In the results the time interval
        # for the midpoint is [34800, 56999]
        full_time = np.array(range(34800, 57000))
        midpoint = 0. * full_time

        # Select the last midpoint price of every second. If there is no
        # midpoint price in a second, takes the value of the previous second
        for t_idx, t_val in enumerate(full_time):

            condition = time_q == t_val
            if (np.sum(condition)):
                midpoint[t_idx] = midpoint_trade[condition][-1]

            else:
                midpoint[t_idx] = midpoint[t_idx - 1]

        # Prevent zero values in dates when the first seconds does not have a
        # midpoint price value
        t_pos = 34800
        while (not np.sum(time_q == t_pos)):
            t_pos -= 1
        m_pos = 0
        condition_2 = time_q == t_pos
        while (not midpoint[m_pos]):
            midpoint[m_pos] = midpoint_trade[condition_2][-1]
            m_pos += 1

        assert not np.sum(midpoint == 0)

        # Saving data
        if (not os.path.isdir(f'../../taq_data/responses_physical_data_{year}'
                              + f'/{function_name}/')):

            try:
                os.mkdir(f'../../taq_data/responses_physical_data_{year}/'
                         + f'{function_name}/')
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        pickle.dump(midpoint / 10000,
                    open(f'../../taq_data/responses_physical_data_{year}/'
                         + f'{function_name}/{function_name}_midpoint_'
                         + f'{year}{month}{day}_{ticker}.pickle', 'wb'))
        pickle.dump(full_time,
                    open(f'../../taq_data/responses_physical_data_{year}/'
                         + f'{function_name}/{function_name}_time.pickle',
                         'wb'))

        print('Data saved')
        print()

        return (full_time, midpoint)

    except TypeError as e:
        return None

# ----------------------------------------------------------------------------


def taq_trade_signs_trade_data(ticker, date):
    """Computes the trade signs of every trade.

    Using the daily TAQ data computes the trade signs of every trade in a day.
    The trade signs are computed using Eq. 1 of the
    `paper
    <https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.
    As the trades signs are not directly given by the TAQ data, they must be
    inferred by the trades prices.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.

    :param ticker: string of the abbreviation of the stock to be analyzed
        (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:
        # Load data
        # The module is used in other folders, so it is necessary to use
        # absolute paths instead of relative paths
        # Obtain the absolut path of the current file and split it
        abs_path = os.path.abspath(__file__).split('/')
        # Take the path from the start to the project folder
        root_path = '/'.join(abs_path[:abs_path.index('project') + 1])
        data_trades_trade = pd.read_hdf(root_path
                                        + f'/taq_data/hdf5_daily_data_{year}/'
                                        + f'taq_{ticker}_trades_{date}.h5',
                                        key='/trades')

        time_t = data_trades_trade['Time'].to_numpy()
        ask_t = data_trades_trade['Ask'].to_numpy()

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

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_trade_signs_physical_data(ticker, date):
    """Computes the trade signs of every second.

    Using the taq_trade_signs_trade_data function computes the trade signs of
    every second.
    The trade signs are computed using Eq. 2 of the
    `paper
    <https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.
    As the trades signs are not directly given by the TAQ data, they must be
    inferred by the trades prices.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.
    To fill the time spaces when nothing happens I added zeros indicating that
    there were neither a buy nor a sell.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_trade_signs_physical_data.__name__
    taq_data_tools_responses_physical \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Calculate the values of the trade signs for all the events
        (time_t, ask_t,
         identified_trades) = taq_trade_signs_trade_data(ticker, date)

        # Reproducing the paper time values. In her results the time interval
        # for the trade signs is [34801, 57000]
        full_time = np.array(range(34801, 57001))
        trade_signs = 0. * full_time
        price_signs = 0. * full_time

        # Implementation of Eq. 2. Trade sign in each second
        for t_idx, t_val in enumerate(full_time):

            condition = (time_t >= t_val) * (time_t < t_val + 1)
            trades_same_t_exp = identified_trades[condition]
            sign_exp = int(np.sign(np.sum(trades_same_t_exp)))
            trade_signs[t_idx] = sign_exp

            if (np.sum(condition)):
                price_signs[t_idx] = ask_t[condition][-1]

        # Saving data
        taq_data_tools_responses_physical \
            .taq_save_data(function_name,
                           (full_time, price_signs, trade_signs), ticker,
                           ticker, year, month, day)

        return (full_time, price_signs, trade_signs)

    except TypeError as e:
        return None

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_physical_data(ticker, date):
    """Computes the self-response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different time lags (:math:`\\tau`) for a day.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:
        # Load data
        midpoint = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_midpoint'
                + f'_physical_data/taq_midpoint_physical_data_midpoint'
                + f'_{year}{month}{day}_{ticker}.pickle', 'rb'))
        _, _, trade_sign = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_trade'
                + f'_signs_physical_data/taq_trade_signs_physical_data'
                + f'_{year}{month}{day}_{ticker}.pickle', 'rb'))

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s is used in the paper
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

            # Midpoint price returns
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
        zeros = np.zeros(__tau__)
        return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_physical_data(ticker, year):
    """Computes the self-response of a year.

    Using the taq_self_response_day_responses_physical_data function computes
    the self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_responses_physical_data.__name__
    taq_data_tools_responses_physical \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_physical.taq_bussiness_days(year)

    self_values = []
    args_prod = iprod([ticker], dates)

    # Parallel computation of the self-responses. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            taq_self_response_day_responses_physical_data, args_prod))

    # To obtain the total self-response, I sum over all the self-response
    # values and all the amount of trades (averaging values)
    self_v_final = np.sum(self_values[0], axis=0)

    self_response_val = self_v_final[0] / self_v_final[1]
    self_response_avg = self_v_final[1]

    # Saving data
    taq_data_tools_responses_physical \
        .taq_save_data(function_name, self_response_val, ticker, ticker, year,
                       '', '')

    return (self_response_val, self_response_avg)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_physical_data(ticker_i, ticker_j, date):
    """Computes the cross-response of a day.

    Using the midpoint price of ticker i and trade signs of ticker j computes
    the cross-response during different time lags (:math:`\\tau`) for a day.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
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
            # Load data
            midpoint_i = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq'
                    + f'_midpoint_physical_data/taq_midpoint_physical_data'
                    + f'_midpoint_{year}{month}{day}_{ticker_i}.pickle', 'rb'))
            _, _, trade_sign_j = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq_trade_'
                    + f'signs_physical_data/taq_trade_signs_physical_data'
                    + f'_{year}{month}{day}_{ticker_j}.pickle', 'rb'))

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s is used in the paper
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

                # Midpoint price returns
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
            zeros = np.zeros(__tau__)
            return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_physical_data(ticker_i, ticker_j, year):
    """Computes the cross-response of a year.

    Using the taq_cross_response_day_responses_physical_data function computes
    the cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = taq_cross_response_year_responses_physical_data \
            .__name__
        taq_data_tools_responses_physical \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_physical.taq_bussiness_days(year)

        cross_values = []
        args_prod = iprod([ticker_i], [ticker_j], dates)

        # Parallel computation of the cross-responses. Every result is appended
        # to a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            cross_values.append(pool.starmap(
                taq_cross_response_day_responses_physical_data, args_prod))

        # To obtain the total cross-response, I sum over all the cross-response
        # values and all the amount of trades (averaging values)
        cross_v_final = np.sum(cross_values[0], axis=0)

        cross_response_val = cross_v_final[0] / cross_v_final[1]
        cross_response_avg = cross_v_final[1]

        # Saving data
        taq_data_tools_responses_physical \
            .taq_save_data(function_name, cross_response_val, ticker_i,
                           ticker_j, year, '', '')

        return (cross_response_val, cross_response_avg)

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_day_responses_physical_data(ticker, date):
    """Computes the trade sign self-correlator of a year.

    Using the trade signs of a ticker computes the self-correlator during
    different time lags (:math:`\\tau`) for a day.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:
        # Load data
        _, _, trade_sign_i = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_trade'
                + f'_signs_physical_data/taq_trade_signs_physical_data'
                + f'_{year}{month}{day}_{ticker}.pickle', 'rb'))

        # Array of the average of each tau. 10^3 s is used in the paper.
        self_correlator = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the trade sign cross-correlator

        # Depending on the tau value
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
        zeros = np.zeros(__tau__)
        return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_year_responses_physical_data(ticker, year):
    """Computes the trade sign self-correlator of a year.

    Using the taq_trade_sign_self_correlator_day_responses_physical_data
    function computes the self-correlator function for a year.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = \
        taq_trade_sign_self_correlator_year_responses_physical_data.__name__
    taq_data_tools_responses_physical \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_physical.taq_bussiness_days(year)

    self_values = []
    args_prod = iprod([ticker], dates)

    # Parallel computation of the self-correlator. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            taq_trade_sign_self_correlator_day_responses_physical_data,
            args_prod))

    # To obtain the total self-correlator, I sum over all the self-correlator
    # values and all the amount of trades (averaging values)
    self_v_final = np.sum(self_values[0], axis=0)

    self_correlator_val = self_v_final[0] / self_v_final[1]
    self_correlator_avg = self_v_final[1]

    # Saving data
    taq_data_tools_responses_physical \
        .taq_save_data(function_name, self_correlator_val, ticker, ticker,
                       year, '', '')

    return (self_correlator_val, self_correlator_avg)

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_day_responses_physical_data(ticker_i,
                                                                ticker_j,
                                                                date):
    """Computes the trade sign cross-correlator of a day.

    Using the trade signs of ticker i and trade signs of ticker j computes the
    cross-correlator during different time lags (:math:`\\tau`) for a day.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
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
            # Load data
            _, _, trade_sign_i = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq_trade_'
                    + f'signs_physical_data/taq_trade_signs_physical_data'
                    + f'_{year}{month}{day}_{ticker_i}.pickle', 'rb'))
            _, _, trade_sign_j = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq_trade_'
                    + f'signs_physical_data/taq_trade_signs_physical_data'
                    + f'_{year}{month}{day}_{ticker_j}.pickle', 'rb'))

            # Array of the average of each tau. 10^3 s used by Wang
            cross_correlator = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the trade sign cross-correlator

            # Depending on the tau value
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
            zeros = np.zeros(__tau__)
            return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_year_responses_physical_data(ticker_i,
                                                                 ticker_j,
                                                                 year):
    """Computes the trade sign-cross correlator of a year.

    Using the taq_trade_sign_cross_correlator_day_responses_physical_data
    function computes the cross-correlator function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = \
            taq_trade_sign_cross_correlator_year_responses_physical_data \
            .__name__
        taq_data_tools_responses_physical \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_physical.taq_bussiness_days(year)

        cross_values = []
        args_prod = iprod([ticker_i], [ticker_j], dates)

        # Parallel computation of the cross-correlator. Every result is
        # appended to a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            cross_values.append(pool.starmap(
                taq_trade_sign_cross_correlator_day_responses_physical_data,
                args_prod))

        # To obtain the total cross-correlator, I sum over all the
        # cross-correlator values and all the amount of trades
        # (averaging values)
        cross_v_final = np.sum(cross_values[0], axis=0)

        cross_correlator_val = cross_v_final[0] / cross_v_final[1]
        cross_correlator_avg = cross_v_final[1]

        # Saving data
        taq_data_tools_responses_physical \
            .taq_save_data(function_name, cross_correlator_val, ticker_i,
                           ticker_j, year, '', '')

        return (cross_correlator_val, cross_correlator_avg)

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
