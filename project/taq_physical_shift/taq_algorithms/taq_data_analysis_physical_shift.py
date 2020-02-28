'''TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * numpy
    * pandas
    * pickle
    * taq_data_tools_physical_shift

The module contains the following functions:
    * taq_self_response_day_physical_shift_data - computes the self response of
      a day.
    * taq_self_response_year_physical_shift_data - computes the self response
      of a year.
    * taq_cross_response_day_physical_shift_data - computes the cross response
      of a day.
    * taq_cross_response_year_physical_shift_data - computes the cross response
      of a year.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import numpy as np
import pandas as pd
import pickle

import taq_data_tools_physical_shift

# ----------------------------------------------------------------------------


def taq_self_response_day_physical_shift_data(ticker, date, tau):
    """Computes the self-response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response during different time shifts for a day. There is a constant
    :math:`\\tau` that most be set in the parameters.

    :param ticker: string of the abbreviation of the stock to be analyzed
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

    try:
        # Load data
        midpoint = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_midpoint'
                + f'_physical_data/taq_midpoint_physical_data_midpoint_{year}'
                + f'{month}{day}_{ticker}.pickle', 'rb'))
        _, _, trade_sign = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/'
                + f'taq_trade_signs_physical_data/taq_trade_signs_physical'
                + f'_data_{year}{month}{day}_{ticker}.pickle', 'rb'))

        # As the data is loaded from the responses physical module results,
        # the data have a shift of 1 second. To correct this I changed both
        # data to have the same time [34801, 56999]
        midpoint = midpoint[1:]
        trade_sign = trade_sign[:-1]

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s is used in the paper
        shift_val = range(- 10 * tau, 10 * tau, 1)
        self_response_shift = np.zeros(len(shift_val))
        num = np.zeros(len(shift_val))

        # Calculating the midpoint price return and the self response function
        # Depending on the time shift value
        for s_idx, s_val in enumerate(shift_val):

            if (s_val < 0):
                midpoint_shift = midpoint[np.abs(s_val):]
                trade_sign_shift = trade_sign[:-np.abs(s_val)]

            elif (s_val > 0):
                midpoint_shift = midpoint[:-s_val]
                trade_sign_shift = trade_sign[s_val:]

            else:
                midpoint_shift = midpoint
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
        shift_val = range(- 10 * tau, 10 * tau, 1)
        zeros = np.zeros(len(shift_val))
        return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_self_response_year_physical_shift_data(ticker, year, tau):
    """Computes the self-response of a year.

    Using the taq_self_response_day_physical_shift_data function computes the
    self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name = taq_self_response_year_physical_shift_data.__name__
    taq_data_tools_physical_shift \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_physical_shift.taq_bussiness_days(year)

    self_values = []
    args_prod = iprod([ticker], dates, [tau])

    # Parallel computation of the self-responses. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            taq_self_response_day_physical_shift_data, args_prod))

    # To obtain the total self-response, I sum over all the self-response
    # values and all the amount of trades (averaging values)
    self_v_final = np.sum(self_values[0], axis=0)

    self_response_val = self_v_final[0] / self_v_final[1]
    self_response_avg = self_v_final[1]

    # Saving data
    taq_data_tools_physical_shift \
        .taq_save_data(f'{function_name}_tau_{tau}', self_response_val, ticker,
                       ticker, year, '', '')

    return (self_response_val, self_response_avg)

# ----------------------------------------------------------------------------


def taq_cross_response_day_physical_shift_data(ticker_i, ticker_j, date, tau):
    """Computes the cross-response of a day.

    Using the midpoint price of ticker i and trade signs of ticker j computes
    the cross-response during different time shifts for a day. There is a
    constant :math:`\\tau` that most be set in the parameters.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
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
            function_name = taq_cross_response_day_physical_shift_data.__name__
            taq_data_tools_physical_shift \
                .taq_function_header_print_data(function_name, ticker_i,
                                                ticker_j, year, month, day)

            # Load data
            midpoint_i = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq'
                    + f'_midpoint_physical_data/taq_midpoint_physical_data'
                    + f'_midpoint_{year}{month}{day}_{ticker_i}.pickle', 'rb'))
            _, _, trade_sign_j = pickle.load(open(
                    f'../../taq_data/responses_physical_data_{year}/taq_trade'
                    + f'_signs_physical_data/taq_trade_signs_physical_data'
                    + f'_{year}{month}{day}_{ticker_j}.pickle', 'rb'))

            # As the data is loaded from the responses physical module
            # results, the data have a shift of 1 second. To correct this
            # I changed both data to have the same time [34801, 56999]
            midpoint_i = midpoint_i[1:]
            trade_sign_j = trade_sign_j[:-1]

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            shift_val = range(- 10 * tau, 10 * tau, 1)
            cross_response_shift = np.zeros(len(shift_val))
            num = np.zeros(len(shift_val))

            # Calculating the midpoint return and the cross response function

            # Depending on the time shift value
            for s_idx, s_val in enumerate(shift_val):

                if (s_val < 0):
                    midpoint_shift = midpoint_i[np.abs(s_val):]
                    trade_sign_shift = trade_sign_j[:-np.abs(s_val)]

                elif (s_val > 0):
                    midpoint_shift = midpoint_i[:-s_val]
                    trade_sign_shift = trade_sign_j[s_val:]

                else:
                    midpoint_shift = midpoint_i
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
            shift_val = range(- 10 * tau, 10 * tau, 1)
            zeros = np.zeros(len(shift_val))
            return (zeros, zeros)

# ----------------------------------------------------------------------------


def taq_cross_response_year_physical_shift_data(ticker_i, ticker_j, year, tau):
    """Computes the cross-response of a year.

    Using the taq_cross_response_day_physical_data function computes the
    cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = taq_cross_response_year_physical_shift_data.__name__
        taq_data_tools_physical_shift \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_physical_shift.taq_bussiness_days(year)

        cross_values = []
        args_prod = iprod([ticker_i], [ticker_j], dates, [tau])

        # Parallel computation of the cross-responses. Every result is appended
        # to a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            cross_values.append(pool.starmap(
                taq_cross_response_day_physical_shift_data, args_prod))

        # To obtain the total cross-response, I sum over all the cross-response
        # values and all the amount of trades (averaging values)
        cross_v_final = np.sum(cross_values[0], axis=0)

        cross_response_val = cross_v_final[0] / cross_v_final[1]
        cross_response_avg = cross_v_final[1]

        # Saving data
        taq_data_tools_physical_shift \
            .taq_save_data(f'{function_name}_tau_{tau}', cross_response_val,
                           ticker_i, ticker_j, year, '', '')

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
