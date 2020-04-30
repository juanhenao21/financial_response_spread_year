'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * itertools
    * multiprocessing
    * numpy
    * os
    * pandas
    * pickle
    * taq_data_tools_responses_trade

The module contains the following functions:
    * taq_midpoint_trade_data - obtains the midpoint price in trade time scale.
    * taq_trade_signs_trade_data - computes the trade signs of every trade.
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

from itertools import product as iprod
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pickle

import taq_data_tools_responses_trade

__tau__ = 1000

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

    function_name = taq_trade_signs_trade_data.__name__

    try:
        # Load data
        # The module is used in other folders, so it is necessary to use
        # absolute paths instead of relative paths
        # Obtain the absolute path of the current file and split it
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
        taq_data_tools_responses_trade \
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
                f'../../taq_data/responses_physical_data_{year}/taq'
                + f'_midpoint_physical_data/taq_midpoint_physical_data'
                + f'_midpoint_{year}{month}{day}_{ticker}.pickle', 'rb'))
        time_t, _, trade_sign = pickle.load(open(
            f'../../taq_data/responses_trade_data_{year}/taq_trade_signs_trade'
            + f'_data/taq_trade_signs_trade_data_{year}{month}{day}_{ticker}'
            + f'.pickle', 'rb'))

        # As the midpoint price values are loaded from the responses physical
        # module and their time is [34800, 56999] and the trade signs values
        # are loaded from the responses trade module and their time is
        # [34200, 57599], I set the time with reference to the midpoint price
        time_m = np.array(range(34800, 57000))
        cond_1 = (time_t >= 34801) * (time_t < 57001)
        time_t = time_t[cond_1]
        trade_sign = trade_sign[cond_1]

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

            # Filter the trade sign values according with the values that can
            # be taken by the midpoint price based on the time
            trade_sign_tau = trade_sign[time_t < time_m[-tau_idx - 1]]
            time_t_tau = time_t[time_t < time_m[-tau_idx - 1]]
            trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
            num[tau_idx] = trade_sign_no_0_len

            # Reduce the time to the corresponding length of returns
            time_m_short = time_m[:-tau_idx - 1]

            # The return of one second is multiplied with all the trade signs
            # of the next second and added to obtain the response
            for t_idx, t_val in enumerate(time_m_short):

                # Obtain the self response value
                # Multiply the return of tau with all the trade signs in one
                # second and add for all the seconds
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
    """Computes the self-response of a year.

    Using the taq_self_response_day_responses_trade_data function computes the
    self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_responses_trade_data.__name__
    taq_data_tools_responses_trade \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_trade.taq_bussiness_days(year)

    self_values = []
    args_prod = iprod([ticker], dates)

    # Parallel computation of the self-responses. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            taq_self_response_day_responses_trade_data, args_prod))

    # To obtain the total self-response, I sum over all the self-response
    # values and all the amount of trades (averaging values)
    self_v_final = np.sum(self_values[0], axis=0)

    self_response_val = self_v_final[0] / self_v_final[1]
    self_response_avg = self_v_final[1]

    # Saving data
    taq_data_tools_responses_trade \
        .taq_save_data(function_name, self_response_val, ticker, ticker, year,
                       '', '')

    return (self_response_val, self_response_avg)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_trade_data(ticker_i, ticker_j, date):
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
            time_t, _, trade_sign_j = pickle.load(open(
                    f'../../taq_data/responses_trade_data_{year}/taq_trade'
                    + f'_signs_trade_data/taq_trade_signs_trade_data'
                    + f'_{year}{month}{day}_{ticker_j}.pickle', 'rb'))

            # As the midpoint price values are loaded from the responses
            # physical # module and their time is [34800, 56999] and the trade
            # signs values # are loaded from the responses trade module and
            # their time is [34200, 57599], I set the time equal to the
            # midpoint price
            time_m = np.array(range(34800, 57000))
            cond_1 = (time_t >= 34801) * (time_t < 57001)
            time_t = time_t[cond_1]
            trade_sign_j = trade_sign_j[cond_1]

            # Array of the average of each tau. 10^3 s is used in the paper
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

                # Filter the trade sign values according with the values that
                # can be taken by the midpoint price based on the time
                trade_sign_tau = trade_sign_j[time_t < time_m[-tau_idx - 1]]
                time_t_tau = time_t[time_t < time_m[-tau_idx - 1]]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len

                # Reduce the time to the corresponding length of returns
                time_m_short = time_m[:-tau_idx - 1]

                # The return of one second is multiplied with all the trade
                # signs of the next second and added to obtain the response
                for t_idx, t_val in enumerate(time_m_short):

                    # Obtain the self response value
                    # Multiply the return of tau with all the trade signs in
                    # one second and add for all the seconds
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
    """Computes the cross-response of a year.

    Using the taq_cross_response_day_responses_trade_data function computes the
    cross-response function for a year.

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
        function_name = taq_cross_response_year_responses_trade_data.__name__
        taq_data_tools_responses_trade \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_trade.taq_bussiness_days(year)

        cross_values = []
        args_prod = iprod([ticker_i], [ticker_j], dates)

        # Parallel computation of the cross-responses. Every result is appended
        # to a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            cross_values.append(pool.starmap(
                taq_cross_response_day_responses_trade_data, args_prod))

        # To obtain the total cross-response, I sum over all the cross-response
        # values and all the amount of trades (averaging values)
        cross_v_final = np.sum(cross_values[0], axis=0)

        cross_response_val = cross_v_final[0] / cross_v_final[1]
        cross_response_avg = cross_v_final[1]

        # Saving data
        taq_data_tools_responses_trade \
            .taq_save_data(function_name, cross_response_val, ticker_i,
                           ticker_j, year, '', '')

        return (cross_response_val, cross_response_avg)

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
