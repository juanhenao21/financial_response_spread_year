'''
ITCH - TAQ trade sign classification

Module to make the trade sign classification in the TAQ data and test the
accuracy of the classification.

Two models will be validated. They can be seen in

https://arxiv.org/pdf/1603.01580.pdf

identified as equation (2) and (3)

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

import numpy as np
import os

import gzip

import itch_data_tools

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_load_test(ticker, year, month, day):
    """
    Obtain the reference trade signs, prices, volumes and time from an ITCH
    file. These data is used to test the trade sign classification models.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = itch_taq_trade_signs_load_test.__name__
    t_step = 'irrelevant '
    itch_data_tools.itch_function_header_print_data(function_name, ticker,
                                                    ticker, year, month, day,
                                                    t_step)

    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_{1}/{1}{2}{3}_{0}.csv.gz'
                         .format(ticker, year, month, day)),
                         dtype='str', skip_header=1, delimiter=',')

    # Lists of times, ids, types, volumes and prices
    # List of all the available information available in the data excluding
    # the last two columns

    # List of order types:
    # "B" = 1 - > Add buy order
    # "S" = 2 - > Add sell order
    # "E" = 3 - > Execute outstanding order in part
    # "C" = 4 - > Cancel outstanding order in part
    # "F" = 5 - > Execute outstanding order in full
    # "D" = 6 - > Delete outstanding order in full
    # "X" = 7 - > Bulk volume for the cross event
    # "T" = 8 - > Execute non-displayed order
    times_ = np.array([int(mytime) for mytime in data[:, 0]])
    ids_ = np.array([int(myid) for myid in data[:, 2]])
    types_ = np.array([1 * (mytype == 'B') +
                       2 * (mytype == 'S') +
                       3 * (mytype == 'E') +
                       4 * (mytype == 'C') +
                       5 * (mytype == 'F') +
                       6 * (mytype == 'D') +
                       7 * (mytype == 'X') +
                       8 * (mytype == 'T') for mytype in data[:, 3]])
    volumes_ = np.array([int(myvolume) for myvolume in data[:, 4]])
    prices_ = np.array([int(myprice) for myprice in data[:, 5]])

    ids = ids_[types_ < 7]
    times = times_[types_ < 7]
    types = types_[types_ < 7]
    volumes = volumes_[types_ < 7]
    prices = prices_[types_ < 7]

    # Reference lists
    # Reference lists using the original values or the length of the original
    # lists

    prices_ref = 1 * prices
    types_ref = 0 * types
    times_ref = 0 * times
    volumes_ref = 0 * types
    newids = {}
    hv = 0

    # Help lists with the data of the buy orders and sell orders

    hv_prices = prices[types < 3]
    hv_types = types[types < 3]
    hv_times = times[types < 3]
    hv_volumes = volumes[types < 3]

    trade_sign = 0 * types
    price_sign = 0 * types
    volume_sign = 0 * types
    time_sign = 0 * types

    # Fill the reference lists where the values of 'T' are 'E', 'C', 'F', 'D'

    # For the data in the length of the ids list (all data)
    for iii in range(len(ids)):

        # If the data is a sell or buy order
        if (types[iii] < 3):

            # Insert in the dictionary newids a key with the valor of the id
            # and the value of hv (a counter) that is the index in hv_types
            newids[ids[iii]] = hv

            # Increase the value of hv
            hv += 1

        # If the data is not a sell or buy order
        elif (types[iii] == 3 or
                types[iii] == 5):

            # Fill the values of prices_ref with no prices ('E', 'C', 'F', 'D')
            # with the price of the order
            prices_ref[iii] = hv_prices[newids[ids[iii]]]

            # Fill the values of types_ref with no  prices ('E', 'C', 'F', 'D')
            # with the type of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]

            # Fill the values of time_ref with no  prices ('E', 'C', 'F', 'D')
            # with the time of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]

            # Fill the values of volumes_ref with no  prices ('E','C','F', 'D')
            # with the volume of the order
            volumes_ref[iii] = hv_volumes[newids[ids[iii]]]

            if (hv_types[newids[ids[iii]]] == 2):

                trade_sign[iii] = 1.
                price_sign[iii] = prices_ref[iii]
                volume_sign[iii] = volumes_ref[iii]
                time_sign[iii] = times_ref[iii]

            elif (hv_types[newids[ids[iii]]] == 1):

                trade_sign[iii] = - 1.
                price_sign[iii] = prices_ref[iii]
                volume_sign[iii] = volumes_ref[iii]
                time_sign[iii] = times_ref[iii]

        else:

            # Fill the values of types_ref with no  prices ('E', 'C', 'F', 'D')
            # with the type of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]

            # Fill the values of time_ref with no  prices ('E', 'C', 'F', 'D')
            # with the time of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]

    # Ordering the data in the open market time

    # This line behaves as an or.the two arrays must achieve a condition, in
    # this case, be in the market trade hours (09:40 - 15:50)
    day_times_ind = (1. * time_sign / 3600 / 1000 > 9.666666) * \
                    (1. * time_sign / 3600 / 1000 < 15.833333) > 0

    price_signs = price_sign[day_times_ind]
    trade_signs = trade_sign[day_times_ind]
    volume_signs = volume_sign[day_times_ind]
    times_signs = time_sign[day_times_ind]

    # The length of the executed oustanding order in part and in full must
    # be the same as the length of the identified trade signs
    assert (len(types[types == 3]) + len(types[types == 5]
            == len(trade_signs[trade_signs != 0])))
    # The length of the price, volume and time must be equal to the length of
    # the identified trade signs
    assert (len(price_signs[price_signs != 0])
            == len(trade_signs[trade_signs != 0]))
    assert (len(volume_signs[volume_signs != 0])
            == len(trade_signs[trade_signs != 0]))
    assert (len(times_signs[times_signs != 0])
            == len(trade_signs[trade_signs != 0]))

    return (price_signs, trade_signs, volume_signs, times_signs)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_consecutive_trades_ms_test(ticker, price_signs,
                                                    trade_signs, times_signs,
                                                    year, month, day):
    """
    Obtain the experimental trade signs based on the change of prices. To
    compute the trades signs are used consecutive trades in the ITCH data.
    Implementatio of the equation (1)
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param price_signs: price of the trades
        :param trade_signs: theoric trade signs from ITCH data
        :param times_signs: time of the trades
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for consecutive trades in'
          ' ms for the stock ' + ticker + ' the ' + year + '.' + month + '.'
          + day)

    # trades with values different to zero to obtain the theoretical value
    price_no_0 = price_signs[trade_signs != 0]
    trades_no_0 = trade_signs[trade_signs != 0]
    time_no_0 = times_signs[trade_signs != 0]

    identified_trades = np.zeros(len(time_no_0))

    # Implementation of equation (1). Sign of the price change between
    # consecutive trades
    for t_idx, t_val in enumerate(time_no_0):

        diff = price_no_0[t_idx] - price_no_0[t_idx - 1]

        if (diff):

            identified_trades[t_idx] = np.sign(diff)

        else:

            identified_trades[t_idx] = identified_trades[t_idx - 1]

    assert not len(identified_trades[identified_trades == 0])
    assert len(identified_trades) == len(trades_no_0[trades_no_0 != 0])

    # Accuracy of the classification
    print('For consecutive trades in ms:')
    itch_data_tools.itch_taq_accuracy_msg(trades_no_0, identified_trades)

    return identified_trades

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_eq2_ms_test(ticker, trade_signs, times_signs,
                                     identified_trades, year, month, day):
    """
    Implementation of the eq. (2) to obtain the trade signs with a stamp of
    1 millisecond
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param trade_signs: theoric trade signs from ITCH data
        :param times_signs: time of the trades
        :param identified_trades: trades signs from eq. (1)
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for number imbalance of '
          ' trades in ms for the stock ' + ticker + ' the ' + year + '.'
          + month + '.' + day)

    trades_no_0 = trade_signs[trade_signs != 0]
    time_no_0 = times_signs[trade_signs != 0]
    time_no_0_set = np.array(sorted(set(time_no_0)))

    assert len(trades_no_0) == len(identified_trades)

    trades_exp_ms = np.zeros(len(time_no_0_set))
    trades_teo_ms = np.zeros(len(time_no_0_set))

    # Implementation of equation (2). Trade sign in each millisecond
    for t_idx, t_val in enumerate(time_no_0_set):

        # Experimental
        trades_same_t_exp = identified_trades[time_no_0 == t_val]
        sign_exp = np.sign(np.sum(trades_same_t_exp))
        trades_exp_ms[t_idx] = sign_exp

        # Theoric
        trades_same_t_teo = trades_no_0[time_no_0 == t_val]
        sign_teo = np.sign(np.sum(trades_same_t_teo))
        trades_teo_ms[t_idx] = sign_teo

    print(len(trades_teo_ms[trades_teo_ms != 0]))
    print(len(trades_exp_ms[trades_exp_ms != 0]))

    print('Reducing the trades to 1 per millisecond:')
    itch_data_tools.itch_taq_accuracy_msg(trades_teo_ms, trades_exp_ms)

    return (trades_teo_ms, trades_exp_ms)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_eq3_ms_test(ticker, trade_signs, volume_signs,
                                     times_signs, identified_trades, year,
                                     month, day):
    """
    Implementation of the eq. (3) to obtain the trade signs with a stamp of
    1 millisecond.
    Volume imbalance
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param trade_signs: theoric trade signs from ITCH data
        :param volume_signs: volume of the trades
        :param times_signs: time of the trades
        :param identified_trades: trades signs from eq. (1)
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for volume imbalance of '
          ' trades in ms for the stock ' + ticker + ' the ' + year + '.'
          + month + '.' + day)

    trades_no_0 = trade_signs[trade_signs != 0]
    volumes_no_0 = volume_signs[trade_signs != 0]
    time_no_0 = times_signs[trade_signs != 0]
    time_no_0_set = np.array(sorted(set(time_no_0)))

    assert len(trades_no_0) == len(identified_trades)

    trades_exp_ms = np.zeros(len(time_no_0_set))
    trades_teo_ms = np.zeros(len(time_no_0_set))

    # Implementation of equation (3). Trade sign in each millisecond
    for t_idx, t_val in enumerate(time_no_0_set):

        # Experimental
        trades_same_t_exp = identified_trades[time_no_0 == t_val]
        volumes_same_t = volumes_no_0[time_no_0 == t_val]
        sign_exp = np.sign(np.sum(trades_same_t_exp * volumes_same_t))
        trades_exp_ms[t_idx] = sign_exp

        # Theoric
        trades_same_t_teo = trades_no_0[time_no_0 == t_val]
        sign_teo = np.sign(np.sum(trades_same_t_teo))
        trades_teo_ms[t_idx] = sign_teo

    print('Reducing the trades to 1 per millisecond:')
    itch_data_tools.itch_taq_accuracy_msg(trades_teo_ms, trades_exp_ms)

    return (trades_teo_ms, trades_exp_ms)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_s_test(ticker, trades_teo_ms, trades_exp_ms,
                                trade_signs, times_signs, year, month, day):
    """
    Trades signs with a stamp of 1 second.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param trades_teo_ms: theoric trade signs in milliseconds (array)
        :param trades_exp_ms: experimental trade signs in milliseconds (array)
        :param times_signs: :param times_signs: time of the trades
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for trades in s for the'
          + ' stock  ' + ticker + ' the ' + year + '.' + month + '.' + day)

    time_no_0 = times_signs[trade_signs != 0]
    time_no_0_set = np.array(sorted(set(time_no_0)))

    full_time = np.array(range(34800, 57000))
    trades_teo_s_0 = 0. * full_time
    trades_exp_s_0 = 0. * full_time

    for t_idx, t_val in enumerate(full_time):

        trades_teo_s_0[t_idx] = np.sign(np.sum(
            trades_teo_ms[(time_no_0_set > t_val * 1000)
                          & (time_no_0_set < (t_val + 1) * 1000)]))
        trades_exp_s_0[t_idx] = np.sign(np.sum(
            trades_exp_ms[(time_no_0_set > t_val * 1000)
                          & (time_no_0_set < (t_val + 1) * 1000)]))

    trades_teo_s = trades_teo_s_0[trades_teo_s_0 != 0]
    trades_exp_s = trades_exp_s_0[trades_teo_s_0 != 0]

    print('Reducing the trades to 1 per second:')
    itch_data_tools.itch_taq_accuracy_msg(trades_teo_s, trades_exp_s)

    return (trades_teo_s, trades_exp_s)

# -----------------------------------------------------------------------------------------------------------------------


def main():

    ticker = ['AAPL', 'AAPL', 'GS', 'GS', 'XOM', 'XOM']
    year = '2008'
    month = ['01', '06', '10', '12', '02', '08']
    day = ['07', '02', '07', '10', '11', '04']

    file = open('../../Basic/stats.csv', 'a+')
    file.write('Date,No_Id_Trades,No_Matches,Accuracy,No_Id_Trades,'
               + 'Matches_eq_2,Acc_eq_2,Matches_eq_3,Acc_eq_3\n')

    for (t, m, d) in zip(ticker, month, day):

        (price_signs, trade_signs,
         volume_signs, times_signs) = itch_taq_trade_signs_load_test(t, year,
                                                                     m, d)

        identified_trades = \
            itch_taq_trade_signs_consecutive_trades_ms_test(t, price_signs,
                                                            trade_signs,
                                                            times_signs, year,
                                                            m, d)

        teo_eq2_ms, exp_eq2_ms = \
            itch_taq_trade_signs_eq2_ms_test(t, trade_signs, times_signs,
                                             identified_trades, year, m, d)

        teo_eq2_s, exp_eq2_s = \
            itch_taq_trade_signs_s_test(t, teo_eq2_ms, exp_eq2_ms, trade_signs,
                                        times_signs, year, m, d)

        teo_eq3_ms, exp_eq3_ms = \
            itch_taq_trade_signs_eq3_ms_test(t, trade_signs, volume_signs,
                                             times_signs, identified_trades,
                                             year, m, d)

        teo_eq3_s, exp_eq3_s = \
            itch_taq_trade_signs_s_test(t, teo_eq3_ms, exp_eq3_ms, trade_signs,
                                        times_signs, year, m, d)

        file.write('{}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n'
                   .format(t,
                           year + m + d,
                           len(trade_signs[trade_signs != 0]),
                           sum(trade_signs[trade_signs != 0]
                               == identified_trades),
                           round(sum(trade_signs[trade_signs != 0]
                                 == identified_trades)
                                 / len(trade_signs[trade_signs != 0]), 4),
                           len(teo_eq2_s),
                           sum(teo_eq2_s == exp_eq2_s),
                           round(sum(teo_eq2_s == exp_eq2_s)
                                 / len(teo_eq2_s), 4),
                           sum(teo_eq3_s == exp_eq3_s),
                           round(sum(teo_eq3_s == exp_eq3_s)
                                 / len(teo_eq3_s), 4)))

    file.close()

# -----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
