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


def taq_data_extract(ticker, type, year):
    """Extracts the data for every day in a year.

    Extracts the trades and quotes (TAQ) data for a day from a CSV file with
    the information of a whole year. The time range for each day is from 9:30
    to 16:00, that means, the open market time.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param type: string with the type of the data to be extracted
     (i.e. 'trades' or 'quotes').
    :param year: string of the year to be analyzed (i.e. '2016').
    :return: None -- The function extracts the data and does not return a
     value.
    """

    function_name = taq_data_extract.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    try:

        df = pd.DataFrame()
        chunksize = 10 ** 7

        date_list = taq_data_tools_article_reproduction \
            .taq_bussiness_days(year)

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
        if (not os.path.isdir(f'../../taq_data/hdf5_dayly_data_{year}/')):

            try:
                os.mkdir(f'../../taq_data/hdf5_dayly_data_{year}/')
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
                    df.to_hdf(f''.join(('../../taq_data/hdf5_dayly_data_'
                              + f'{year}/taq_{ticker}_{type}_{date}.h5')
                              .split()), key=type,
                              format='table', append=True)

        print('Data Saved')
        print()

        return None

    except AssertionError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_midpoint_event_data(ticker, date):
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

    date_sep = date.split('-')
    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_midpoint_event_data.__name__
    taq_data_tools_article_reproduction \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    # Load data
    # TAQ data gives directly the quotes data in every second that there is
    # a change in the quotes
    data_quotes_event = pd.read_hdf(
        f'../../taq_data/hdf5_dayly_data_{year}/taq_{ticker}_quotes_'
        + f'{date}.h5')

    # Some files are corrupted, so there are some zero values that
    # does not have sense
    data_quotes_event = data_quotes_event[data_quotes_event['Ask'] != 0]

    data_quotes_event['Midpoint'] = (data_quotes_event['Bid']
                                     + data_quotes_event['Ask']) / 2
    data_quotes_event['Spread'] = data_quotes_event['Ask'] \
        - data_quotes_event['Bid']

    return data_quotes_event

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
        data_quotes_event = taq_midpoint_event_data(ticker, date)

        # 34800 s = 9h40 - 57000 s = 15h50
        # Reproducing S. Wang values. In her results the time interval for the
        # midpoint is [34800, 56999]
        full_time = np.array(range(34800, 57000))

        # As there can be several values for the same second, we use the
        # last value of each second in the full time array as it behaves
        # quiet equal as the original input
        set_data_time = np.array(list(set(data_quotes_event['Time'])))
        list_data_time = [0] * len(full_time)

        for t_idx, t_val in enumerate(full_time):
            if (np.sum(t_val == set_data_time)):

                condition = data_quotes_event['Time'] == t_val
                data_dict = {'Time': data_quotes_event[condition].ix[-1]['Time'],
                             'Midpoint': data_quotes_event[condition].ix[-1]['Midpoint']}

                list_data_time[t_idx] = data_dict

            else:

                data_dict = {'Time': list_data_time[t_idx - 1]['Time'],
                             'Midpoint': list_data_time[t_idx - 1]['Midpoint']}

                list_data_time[t_idx] = data_dict

        data_quotes_time = pd.DataFrame(list_data_time, columns=['Time', 'Midpoint'])

        # The lengths of the time and the dataframe have to be the same
        assert len(full_time) == len(data_quotes_time['Time'])

        data_quotes_time['Time'] = full_time

        # Saving data

        if (not os.path.isdir(''.join((f'../../taq_data/article_reproduction'
                              + f'_data_{function_name}/{year}/').split()))):

            try:
                os.mkdir(''.join((f'../../taq_data/article_reproduction_data'
                        + f'_{year}/{function_name}/').split()))
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        data_quotes_time.astype(str).to_hdf(''.join((f'../../taq_data/article'
                                + f'_reproduction_data_{year}/{function_name}/'
                                + f'{function_name}_quotes_{year}{month}{day}'
                                + f'_{ticker}.h5').split()),
                                key='data_quotes_time', mode='w', format='table')

        print('Data saved')
        print()

        return data_quotes_time

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

    import time
    import multiprocessing as mp
    from itertools import product
    t = 0
    tickers = ['AAPL', 'MSFT']
    for _ in range(1):
        t0 = time.time()
        data_time = taq_midpoint_time_data('MSFT', '2008-01-02')
        data_event = taq_midpoint_event_data('MSFT', '2008-01-02')
        t1 = time.time()
        t += t1 - t0

    print(t)


    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
