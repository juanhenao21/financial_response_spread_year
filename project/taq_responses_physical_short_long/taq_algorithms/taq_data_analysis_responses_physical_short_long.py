''' TAQ data analysis module.

The functions in the module analyze the data from the NASDAQ stock market,
computing the self- and cross-response functions.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * numpy
    * pandas
    * pickle
    * taq_data_tools_responses_physical_short_long

The module contains the following functions:
    * taq_self_response_day_responses_physical_short_long_data - computes the
      self response of a day.
    * taq_self_response_year_responses_physical_short_long_data - computes the
      self response of a year.
    * taq_cross_response_day_responses_physical_short_long_data - computes the
      cross response of a day.
    * taq_cross_response_year_responses_physical_short_long_data - computes the
      cross response of a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import numpy as np
import pandas as pd
import pickle

import taq_data_tools_responses_physical_short_long

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_physical_short_long_data(ticker, date, tau,
                                                             tau_p):
    """Computes the self-response of a day.

    Using the midpoint price and trade signs of a ticker computes the self-
    response for a day. There is a constant :math:`\\tau` and :math:`\\tau'`
    that must be set in the parameters.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param tau: integer greater than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
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

        # As the data is loaded from the responses physical module results,
        # the data have a shift of 1 second.
        assert len(midpoint) == len(trade_sign)

        # Array for the average of each tau
        self_short = np.zeros(tau)
        self_long = np.zeros(tau)
        self_response = np.zeros(tau)
        self_shuffle = np.zeros(tau)
        num_short = np.zeros(tau)
        num_long = np.zeros(tau)
        num_response = np.zeros(tau)
        num_shuffle = np.zeros(tau)

        # Short response after tau_p
        # Calculating the midpoint price return and the self response function
        trade_sign_tau_short = trade_sign[:-tau_p - 1]
        trade_sign_no_0_len_short = len(trade_sign_tau_short
                                        [trade_sign_tau_short != 0])
        num_short[tau_p:] = trade_sign_no_0_len_short * np.ones(tau - tau_p)

        # Obtain the midpoint price return. Displace the numerator tau
        # values to the right and compute the return
        # Midpoint price returns
        log_return_sec_short = (midpoint[tau_p + 1:]
                                - midpoint[:-tau_p - 1]) \
            / midpoint[:-tau_p - 1]

        # Obtain the self response value
        if (trade_sign_no_0_len_short):
            product_short = log_return_sec_short * trade_sign_tau_short
            self_short[tau_p:] = np.sum(product_short) * np.ones(tau - tau_p)

        # Depending on the tau value
        for tau_idx in range(tau):

            if (tau_idx <= tau_p):
                # Short response
                trade_sign_tau_short = trade_sign[:-tau_idx - 1]
                trade_sign_tau_shuffle = 1 * trade_sign_tau_short
                trade_sign_no_0_len_short = len(trade_sign_tau_short
                                                [trade_sign_tau_short != 0])
                num_short[tau_idx] = trade_sign_no_0_len_short
                num_long[tau_idx] = trade_sign_no_0_len_short
                num_response[tau_idx] = trade_sign_no_0_len_short
                num_shuffle[tau_idx] = trade_sign_no_0_len_short

                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return
                # midpoint price returns
                log_return_sec_short = (midpoint[tau_idx + 1:]
                                        - midpoint[:-tau_idx - 1]) \
                    / midpoint[:-tau_idx - 1]

                # Obtain the self response value
                if (trade_sign_no_0_len_short):
                    product_short = log_return_sec_short * trade_sign_tau_short
                    np.random.shuffle(trade_sign_tau_shuffle)
                    product_shuffle = log_return_sec_short \
                        * trade_sign_tau_shuffle
                    self_short[tau_idx] = np.sum(product_short)
                    self_long[tau_idx] = np.sum(product_short)
                    self_response[tau_idx] = np.sum(product_short)
                    self_shuffle[tau_idx] = np.sum(product_shuffle)

            else:

                # Long response

                trade_sign_tau_long = trade_sign[:-(tau_idx + tau_p)]
                trade_sign_no_0_len_long = len(trade_sign_tau_long
                                               [trade_sign_tau_long != 0])
                num_long[tau_idx] = trade_sign_no_0_len_long

                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return
                # midpoint price returns
                log_return_sec_long = (midpoint[tau_idx:-tau_p]
                                       - midpoint[tau_p:-tau_idx]) \
                    / midpoint[tau_p:-tau_idx]

                # Obtain the self response value
                if (trade_sign_no_0_len_long != 0):
                    product_long = log_return_sec_long * trade_sign_tau_long
                    self_long[tau_idx] = np.sum(product_long)

                # Normal response

                trade_sign_tau_resp = trade_sign[:-tau_idx - 1]
                trade_sign_no_0_len_resp = len(trade_sign_tau_resp
                                               [trade_sign_tau_resp != 0])
                num_response[tau_idx] = trade_sign_no_0_len_resp

                # Obtain the midpoint price return. Displace the numerator tau
                # values to the right and compute the return
                # midpoint price returns
                log_return_sec_resp = (midpoint[tau_idx + 1:]
                                       - midpoint[:-tau_idx - 1]) \
                    / midpoint[:-tau_idx - 1]

                # Obtain the self response value
                if (trade_sign_no_0_len_resp != 0):
                    product = log_return_sec_resp * trade_sign_tau_resp
                    self_response[tau_idx] = np.sum(product)

                # Shuffle response
                trade_sign_tau_shuffle = 1 * trade_sign_tau_resp
                num_shuffle[tau_idx] = trade_sign_no_0_len_resp

                # Obtain the self response value
                if (trade_sign_no_0_len_resp != 0):
                    np.random.shuffle(trade_sign_tau_shuffle)
                    product_shuffle = log_return_sec_resp \
                        * trade_sign_tau_shuffle
                    self_shuffle[tau_idx] = np.sum(product_shuffle)

        return (self_short, num_short,
                self_long, num_long,
                self_response, num_response,
                self_shuffle, num_shuffle)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        zeros = np.zeros(tau)
        return (zeros, zeros, zeros, zeros, zeros, zeros, zeros, zeros)

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_physical_short_long_data(ticker, year,
                                                              tau, tau_p):
    """Computes the self-response of a year.

    Using the taq_self_response_day_responses_physical_short_long_data function
    computes the self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None – The function saves the data in a file and does not return
     a value.
    """

    function_name = taq_self_response_year_responses_physical_short_long_data \
        .__name__
    taq_data_tools_responses_physical_short_long \
        .taq_function_header_print_data(function_name, ticker, ticker, year,
                                        '', '')

    dates = taq_data_tools_responses_physical_short_long \
        .taq_bussiness_days(year)

    self_values = []
    args_prod = iprod([ticker], dates, [tau], [tau_p])

    # Parallel computation of the self-responses. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            taq_self_response_day_responses_physical_short_long_data,
            args_prod))

    # To obtain the total self-response, I sum over all the self-response
    # values and all the amount of trades (averaging values)
    self_v_final = np.sum(self_values[0], axis=0)

    self_response_short_val = self_v_final[0] / self_v_final[1]
    self_response_short_avg = self_v_final[1]
    self_response_long_val = self_v_final[2] / self_v_final[3]
    self_response_long_avg = self_v_final[3]
    self_response_resp_val = self_v_final[4] / self_v_final[5]
    self_response_resp_avg = self_v_final[5]
    self_response_shuffle_val = self_v_final[6] / self_v_final[7]
    self_response_shuffle_avg = self_v_final[7]

    # Saving data
    taq_data_tools_responses_physical_short_long \
        .taq_save_data(f'{function_name}_tau_{tau}_tau_p_{tau_p}',
                       (self_response_short_val,
                        self_response_long_val,
                        self_response_resp_val,
                        self_response_shuffle_val),
                       ticker, ticker, year, '', '')

    return (self_response_short_val,
            self_response_long_val,
            self_response_resp_val,
            self_response_shuffle_val)

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_physical_short_long_data(ticker_i,
                                                              ticker_j, date,
                                                              tau, tau_p):
    """Computes the cross-response of a day.

    Using the midpoint price of ticker i and trade signs of ticker j computes
    the cross-response for a day. There is a constant :math:`\\tau` and
    :math:`\\tau'` that must be set in the parameters.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param tau: integer great than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: tuple -- The function returns a tuple with positions.
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
                f'../../taq_data/responses_physical_data_{year}/taq_midpoint'
                + f'_physical_data/taq_midpoint_physical_data_midpoint'
                + f'_{year}{month}{day}_{ticker_i}.pickle', 'rb'))
            _, _, trade_sign_j = pickle.load(open(
                f'../../taq_data/responses_physical_data_{year}/taq_trade'
                + f'_signs_physical_data/taq_trade_signs_physical_data'
                + f'_{year}{month}{day}_{ticker_j}.pickle', 'rb'))

            # As the data is loaded from the article reproduction module
            # results, the data have a shift of 1 second.
            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_short = np.zeros(tau)
            cross_long = np.zeros(tau)
            cross_response = np.zeros(tau)
            cross_shuffle = np.zeros(tau)
            num_short = np.zeros(tau)
            num_long = np.zeros(tau)
            num_response = np.zeros(tau)
            num_shuffle = np.zeros(tau)

            # Short response after tau_p

            # Calculating the midpoint return and the cross response function
            trade_sign_tau_short = trade_sign_j[:-tau_p - 1]
            trade_sign_no_0_len_short = \
                len(trade_sign_tau_short[trade_sign_tau_short != 0])
            num_short[tau_p:] = trade_sign_no_0_len_short \
                * np.ones(tau - tau_p)
            # Obtain the midpoint price return. Displace the numerator
            # tau values to the right and compute the return
            log_return_i_sec_short = (midpoint_i[tau_p + 1:]
                                      - midpoint_i[:-tau_p - 1]) \
                / midpoint_i[:-tau_p - 1]

            # Obtain the cross response value
            if (trade_sign_no_0_len_short):
                product_short = log_return_i_sec_short \
                                * trade_sign_tau_short
                cross_short[tau_p:] = np.sum(product_short) \
                    * np.ones(tau - tau_p)

            # Depending on the tau value
            for tau_idx in range(tau):

                if (tau_idx <= tau_p):
                    # Short response
                    trade_sign_tau_short = trade_sign_j[:-tau_idx - 1]
                    trade_sign_tau_shuffle = 1 * trade_sign_tau_short
                    trade_sign_no_0_len_short = \
                        len(trade_sign_tau_short[trade_sign_tau_short != 0])
                    num_short[tau_idx] = trade_sign_no_0_len_short
                    num_long[tau_idx] = trade_sign_no_0_len_short
                    num_response[tau_idx] = trade_sign_no_0_len_short
                    num_shuffle[tau_idx] = trade_sign_no_0_len_short

                    # Obtain the midpoint price return. Displace the numerator
                    # tau values to the right and compute the return
                    # midpoint price returns

                    log_return_sec_short = (midpoint_i[tau_idx + 1:]
                                            - midpoint_i[:-tau_idx - 1]) \
                        / midpoint_i[:-tau_idx - 1]

                    # Obtain the self response value
                    if (trade_sign_no_0_len_short):
                        product_short = log_return_sec_short \
                            * trade_sign_tau_short
                        np.random.shuffle(trade_sign_tau_shuffle)
                        product_shuffle = log_return_sec_short \
                            * trade_sign_tau_shuffle
                        cross_short[tau_idx] = np.sum(product_short)
                        cross_long[tau_idx] = np.sum(product_short)
                        cross_response[tau_idx] = np.sum(product_short)
                        cross_shuffle[tau_idx] = np.sum(product_shuffle)

                else:
                    # Long response
                    trade_sign_tau_long = trade_sign_j[:-(tau_idx + tau_p)]
                    trade_sign_no_0_len_long = len(trade_sign_tau_long
                                                   [trade_sign_tau_long != 0])
                    num_long[tau_idx] = trade_sign_no_0_len_long
                    # Obtain the midpoint price return. Displace the numerator
                    # tau values to the right and compute the return
                    # midpoint price returns
                    log_return_sec_long = (midpoint_i[tau_idx:-tau_p]
                                           - midpoint_i[tau_p:-tau_idx]) \
                        / midpoint_i[tau_p:-tau_idx]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len_long != 0):
                        product_long = log_return_sec_long \
                            * trade_sign_tau_long
                        cross_long[tau_idx] = np.sum(product_long)

                    # Normal response
                    trade_sign_tau_resp = trade_sign_j[:-tau_idx - 1]
                    trade_sign_no_0_len_resp = len(trade_sign_tau_resp
                                                   [trade_sign_tau_resp != 0])
                    num_response[tau_idx] = trade_sign_no_0_len_resp

                    # Obtain the midpoint price return. Displace the numerator
                    # tau values to the right and compute the return
                    # midpoint price returns
                    log_return_sec_resp = (midpoint_i[tau_idx + 1:]
                                           - midpoint_i[:-tau_idx - 1]) \
                        / midpoint_i[:-tau_idx - 1]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len_resp != 0):
                        product = log_return_sec_resp * trade_sign_tau_resp
                        cross_response[tau_idx] = np.sum(product)

                    # Shuffle response
                    trade_sign_tau_shuffle = 1 * trade_sign_tau_resp
                    num_shuffle[tau_idx] = trade_sign_no_0_len_resp

                    # Obtain the cross response value
                    if (trade_sign_no_0_len_resp != 0):
                        np.random.shuffle(trade_sign_tau_shuffle)
                        product_shuffle = log_return_sec_resp \
                            * trade_sign_tau_shuffle
                        cross_shuffle[tau_idx] = np.sum(product_shuffle)

            return (cross_short, num_short,
                    cross_long, num_long,
                    cross_response, num_response,
                    cross_shuffle, num_shuffle)

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            zeros = np.zeros(tau)
            return (zeros, zeros, zeros, zeros, zeros, zeros, zeros, zeros)

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_physical_short_long_data(ticker_i,
                                                               ticker_j, year,
                                                               tau, tau_p):
    """Computes the cross-response of a year.

    Using the taq_cross_response_day_responses_physical_short_long_data
    function computes the cross-response function for a year.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param tau: integer great than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None – The function saves the data in a file and does not return a
     value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        function_name = \
             taq_cross_response_year_responses_physical_short_long_data \
             .__name__
        taq_data_tools_responses_physical_short_long \
            .taq_function_header_print_data(function_name, ticker_i, ticker_j,
                                            year, '', '')

        dates = taq_data_tools_responses_physical_short_long \
            .taq_bussiness_days(year)

        cross_values = []
        args_prod = iprod([ticker_i], [ticker_j], dates, [tau], [tau_p])

        # Parallel computation of the cross-responses. Every result is appended
        # to a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            cross_values.append(pool.starmap(
                taq_cross_response_day_responses_physical_short_long_data,
                args_prod))

        # To obtain the total cross-response, I sum over all the cross-response
        # values and all the amount of trades (averaging values)
        cross_v_final = np.sum(cross_values[0], axis=0)

        cross_response_short_val = cross_v_final[0] / cross_v_final[1]
        cross_response_short_avg = cross_v_final[1]
        cross_response_long_val = cross_v_final[2] / cross_v_final[3]
        cross_response_long_avg = cross_v_final[3]
        cross_response_resp_val = cross_v_final[4] / cross_v_final[5]
        cross_response_resp_avg = cross_v_final[5]
        cross_response_shuffle_val = cross_v_final[6] / cross_v_final[7]
        cross_response_shuffle_avg = cross_v_final[7]

        # Saving data
        taq_data_tools_responses_physical_short_long \
            .taq_save_data(f'{function_name}_tau_{tau}_tau_p_{tau_p}',
                           (cross_response_short_val,
                            cross_response_long_val,
                            cross_response_resp_val,
                            cross_response_shuffle_val),
                           ticker_i, ticker_j, year, '', '')

        return (cross_response_short_val,
                cross_response_long_val,
                cross_response_resp_val,
                cross_response_shuffle_val)
        # Saving data
        taq_data_tools_responses_physical_short_long \
            .taq_save_data('{}_tau_{}_tau_p_{}'
                           .format(function_name, tau, tau_p),
                           (cross_short / num_short_t,
                            cross_long / num_long_t,
                            cross_response / num_response_t,
                            cross_shuffle / num_shuffle_t),
                           ticker_i, ticker_j, year, '', '')

        return (cross_short / num_short_t,
                cross_long / num_long_t,
                cross_response / num_response_t,
                cross_shuffle / num_shuffle_t)

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
