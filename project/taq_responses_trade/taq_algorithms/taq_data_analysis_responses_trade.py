'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * numpy
    * os
    * pandas
    * pickle
    * taq_data_tools_responses_trade

The module contains the following functions:
    * taq_self_response_day_responses_trade_data - computes the self response
      of a day.
    * taq_self_response_year_responses_trade_data - computes the self response
      of a year.
    * taq_cross_response_day_responses_trade_data - computes the cross
      response of a day.
    * taq_cross_response_year_responses_trade_data - computes the cross
      response of a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from itertools import product as ipod
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_responses_trade

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_midpoint_day_responses_trade_data(ticker, date):
    """Obtain the midpoint in trade time scale.

    Using the midpoint price in physical time scale, associate the value of
    each second to the value of each trade in trade time scale for a day.

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

    function_name = taq_midpoint_day_responses_trade_data.__name__
    taq_data_tools_responses_trade \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        month, day)

    try:
        # Load data
        midpoint = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_midpoint'
                + f'_time_data/taq_midpoint_time_data_midpoint_{year}{month}'
                + f'{day}_{ticker}.pickle', 'rb'))
        time_t, _, _ = pickle.load(open(
                f'../../taq_data/responses_trade_shift_data_{year}/taq_trade'
                + f'_signs_responses_trade_shift_data/taq_trade_signs'
                + f'_responses_trade_shift_data_{year}{month}{day}_{ticker}'
                + f'.pickle', 'rb'))

        assert not np.sum(midpoint == 0)
        assert not np.sum(time_t == 0)

        # Midpoint array with the length of the trade signs
        midpoint_t = 0. * time_t
        midpoint = midpoint[1:]
        time_scale = range(34801, 57000)

        # It is needed to associate each trade sign with a midpoint price
        for t_idx, t_val in enumerate(time_scale):
            condition = time_t == t_val
            len_c = np.sum(condition)
            midpoint_t[condition] = midpoint[t_idx] * np.ones(len_c)

        assert not np.sum(midpoint_t == 0)

        # Saving data
        taq_data_tools_responses_trade.taq_save_data(function_name, midpoint_t,
                                                     ticker, ticker, year,
                                                     month, day)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_trade_signs_trade_data(ticker, date):
    """Computes the trade signs of every trade.

    Using the dayly TAQ data computes the trade signs of every trade in a day.
    The trade signs are computed using Eq. 1 of the
    `paper
    <https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.
    As the trades signs are not directly given by the TAQ data, they must be
    infered by the trades prices.
    For further calculations, the function returns the values for the time
    range from 9h40 to 15h50.

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

    try:
        # Load data
        # The module is used in other folders, so it is necessary to use
        # absolute paths instead of relative paths
        # Obtain the absolut path of the current file and split it
        abs_path = os.path.abspath(__file__).split('/')
        # Take the path from the start to the project folder
        root_path = '/'.join(abs_path[:abs_path.index('project') + 1])
        data_trades_trade = pd.read_hdf(root_path
                                        + f'/taq_data/hdf5_dayly_data_{year}/'
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

        # Saving data
        taq_data_tools_responses_event_shift \
            .taq_save_data(function_name, (time_t, ask_t, identified_trades),
                           ticker, ticker, year, month, day)

        return (time_t, ask_t, identified_trades)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_trade_data(ticker, date):
    """Computes the self-response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different time lags (:math:`\\tau`) for a day.

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

    try:
        # Load data
        midpoint = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq'
                + f'_midpoint_time_data/taq_midpoint_time_data_midpoint'
                + f'_{year}{month}{day}_{ticker}.pickle', 'rb'))
        time_t, _, trade_sign = pickle.load(open(
            f'../../taq_data/responses_trade_data_{year}/taq_trade_signs_trade'
            + f'_data/taq_trade_signs_trade_data_{year}{month}{day}_{ticker}'
            + f'.pickle', 'rb'))

        # As the trade signs data only reach the second 56999, the midpoint
        # data must be cut to 56998 seconds
        time_m = np.array(range(34800, 56999))
        midpoint = midpoint[:-1]

        # Array of the average of each tau. 10^3 s is used in the paper
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint price return and the self response function

        # Depending on the tau value
        for tau_idx in range(__tau__):

            # midpoint price returns
            # Obtain the midpoint price return. Displace the numerator tau
            # values to the right and compute the return

            log_return_sec = (midpoint[tau_idx + 1:]
                              - midpoint[:-tau_idx - 1]) \
                / midpoint[:-tau_idx - 1]

            trade_sign_tau = trade_sign[time_t < time_m[-tau_idx - 1]]
            time_t_tau = time_t[time_t < time_m[-tau_idx - 1]]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            num[tau_idx] = trade_sign_no_0_len

            # Reduce the time to the corresponding length of returns
            time_m_short = time_m[:-tau_idx - 1]

            for t_idx, t_val in enumerate(time_m_short):

                # Obtain the self response value
                product = log_return_sec[t_idx] \
                    * trade_sign_tau[time_t_tau == t_val]
                self_response_tau[tau_idx] += np.sum(product)

        return (self_response_tau, num)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        zeros = np.zeros(__tau__)
        return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_trade_data(ticker, year):
    """Computes the self response of a year.

    Using the taq_self_response_day_responses_trade_data function computes the
    self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_responses_trade_data.__name__
    taq_data_tools_responses_trade \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_trade.taq_bussiness_days(year)

    data = []
    args_prod = product([ticker], dates)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        data.append(pool.starmap(taq_self_response_day_responses_trade_data,
                                 args_prod))

    total = np.sum(data[0], axis=0)

    # Saving data
    taq_data_tools_responses_trade \
        .taq_save_data(function_name, total[0] / total[1], ticker, ticker,
                       year, '', '')

    return (total[0] / total[1], total[1])

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_trade_data(ticker_i, ticker_j, date):
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
            function_name = taq_cross_response_day_responses_trade_data \
                .__name__
            taq_data_tools_responses_trade \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    f'../../taq_data/responses_physical_data_{year}/taq'
                    + f'_midpoint_time_data/taq_midpoint_time_data_midpoint'
                    + f'_{year}{month}{day}_{ticker_i}.pickle').split()),
                    'rb'))
            time_t, _, trade_sign_j = pickle.load(open("".join((
                    f'../../taq_data/responses_trade_shift_data_{year}/taq'
                    + f'_trade_signs_responses_trade_shift_data/taq_trade'
                    + f'_signs_responses_trade_shift_data_{year}{month}{day}'
                    + f'_{ticker_j}.pickle').split()), 'rb'))

            # As the trade signs data only reach the second 56999, the midpoint
            # data must be cut to 56998 seconds
            time_m = np.array(range(34800, 56999))
            midpoint_i = midpoint_i[:-1]

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function
            # Depending on the tau value
            for tau_idx in range(__tau__):

                # midpoint price returns
                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return

                log_return_i_sec = (midpoint_i[tau_idx + 1:]
                                    - midpoint_i[:-tau_idx - 1]) \
                    / midpoint_i[:-tau_idx - 1]

                trade_sign_tau = trade_sign_j[time_t < time_m[-tau_idx - 1]]
                time_t_tau = time_t[time_t < time_m[-tau_idx - 1]]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len

                # Reduce the time to the corresponding length of returns
                time_m_short = time_m[:-tau_idx - 1]

                for t_idx, t_val in enumerate(time_m_short):

                    # Obtain the self response value
                    product = log_return_i_sec[t_idx] \
                        * trade_sign_tau[time_t_tau == t_val]
                    cross_response_tau[tau_idx] += np.sum(product)

            return (cross_response_tau, num)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            zeros = np.zeros(__tau__)
            return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_trade_data(ticker_i, ticker_j, year):
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
        function_name = taq_cross_response_year_responses_trade_data.__name__
        taq_data_tools_responses_trade \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_trade.taq_bussiness_days(year)

        data = []
        args_prod = product([ticker_i], [ticker_j], dates)

        with mp.Pool(processes=mp.cpu_count()) as pool:
            data.append(pool.starmap(
                taq_cross_response_day_responses_trade_data, args_prod))

        total = np.sum(data[0], axis=0)

        # Saving data
        taq_data_tools_responses_trade \
            .taq_save_data(function_name, total[0] / total[1], ticker_i,
                           ticker_j, year, '', '')

        return (total[0] / total[1], total[1])

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
