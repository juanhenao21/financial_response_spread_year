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
import pandas as pd

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

    # Load full data using cols with values time, order, type, shares and price
    data = pd.read_csv(gzip.open('../../ITCH_{1}/{1}{2}{3}_{0}.csv.gz'
                       .format(ticker, year, month, day), 'rt'),
                       usecols=(0, 2, 3, 4, 5))

    data['Price'] = data['Price'] / 10000

    # Select only trade orders
    trade_pos = np.array(data['T'] == 'E') + np.array(data['T'] == 'F')
    trade_data = data[trade_pos]
    # Converting the data in numpy arrays
    trade_data_time = trade_data['Time'].values
    trade_data_order = trade_data['Order'].values
    trade_data_types = 3 * np.array(trade_data['T'] == 'E') \
        + 4 * np.array(trade_data['T'] == 'F')
    trade_data_volume = trade_data['Shares'].values

    # Select only limit orders
    limit_pos = np.array(data['T'] == 'B') + np.array(data['T'] == 'S')
    limit_data = data[limit_pos]
    # Reduce the values to only the ones that have the same order number
    # as trade orders
    limit_data = limit_data[limit_data.Order.isin(trade_data['Order'])]
    # Converting the data in numpy arrays
    limit_data_order = limit_data['Order'].values
    limit_data_types = 1 * np.array(limit_data['T'] == 'S') \
        - 1 * np.array(limit_data['T'] == 'B')
    limit_data_volume = limit_data['Shares'].values
    limit_data_price = limit_data['Price'].values

    # Arrays to store the info of the identified trades
    length_trades = len(trade_data)
    trade_times = 1 * trade_data_time
    trade_signs = np.zeros(length_trades)
    trade_volumes = np.zeros(length_trades, dtype='uint16')
    trade_price = np.zeros(length_trades)

    for t_idx in range(len(trade_data)):
        # limit orders that have the same order as the trade order
        l_idx = np.where(limit_data_order == trade_data_order[t_idx])[0][0]

        # Save values that are independent of the type

        # Price of the trade (Limit data)
        trade_price[t_idx] = limit_data_price[l_idx]

        # Trade sign identification

        trade = limit_data_types[l_idx]

        if (trade == 1):
            trade_signs[t_idx] = 1.
        else:
            trade_signs[t_idx] = -1.

        # The volume depends on the trade type. If it is 4 the
        # value is taken from the limit data and the order number
        # is deleted from the data. If it is 3 the
        # value is taken from the trade data and then the
        # value of the volume in the limit data must be
        # reduced with the value of the trade data

        volume_type = trade_data_types[t_idx]

        if (volume_type == 4):

            trade_volumes[t_idx] = limit_data_volume[l_idx]
            limit_data_order[l_idx] = 0

        else:

            trade_volumes[t_idx] = trade_data_volume[t_idx]
            diff_volumes = limit_data_volume[l_idx] - trade_data_volume[t_idx]

            assert diff_volumes > 0

            limit_data_volume[l_idx] = diff_volumes

    assert not sum(trade_signs == 0)

    market_time = (trade_times / 3600 / 1000 >= 9.666666) & \
                  (trade_times / 3600 / 1000 < 15.833333)

    trade_times_market = trade_times[market_time]
    trade_signs_market = trade_signs[market_time]
    trade_volumes_market = trade_volumes[market_time]
    trade_price_market = trade_price[market_time]

    # The length of the executed oustanding order in part and in full must
    # be the same as the length of the identified trade signs
    assert (len(trade_data_types) == len(trade_signs[trade_signs != 0]))
    # The length of the price, volume and time must be equal to the length of
    # the identified trade signs
    assert (len(trade_price_market[trade_price_market != 0])
            == len(trade_signs_market[trade_signs_market != 0]))
    assert (len(trade_volumes_market[trade_volumes_market != 0])
            == len(trade_signs_market[trade_signs_market != 0]))
    assert (len(trade_times_market[trade_times_market != 0])
            == len(trade_signs_market[trade_signs_market != 0]))

    return (trade_times_market, trade_signs_market, trade_volumes_market,
            trade_price_market)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_eq1_ms_test(ticker, trade_signs, price_signs,
                                     year, month, day):
    """
    Obtain the experimental trade signs based on the change of prices. To
    compute the trades signs are used consecutive trades in the ITCH data.
    Implementatio of the equation (1)
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param trade_signs: theoric trade signs from ITCH data
        :param price_signs: price of the trades
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for consecutive trades in'
          ' ms for the stock ' + ticker + ' the ' + year + '.' + month + '.'
          + day)

    # trades with values different to zero to obtain the theoretical value
    assert not len(price_signs[price_signs == 0])
    assert not len(trade_signs[trade_signs == 0])

    identified_trades = np.zeros(len(trade_signs))

    # Implementation of equation (1). Sign of the price change between
    # consecutive trades
    for t_idx, t_val in enumerate(trade_signs):

        diff = price_signs[t_idx] - price_signs[t_idx - 1]

        if (diff):

            identified_trades[t_idx] = np.sign(diff)

        else:

            identified_trades[t_idx] = identified_trades[t_idx - 1]

    assert not len(identified_trades[identified_trades == 0])

    # Accuracy of the classification
    print('For consecutive trades in ms:')
    itch_data_tools.itch_taq_accuracy_msg(trade_signs, identified_trades)

    return identified_trades

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_eq2_ms_test(ticker, times_signs, trade_signs,
                                     identified_trades, year, month, day):
    """
    Implementation of the eq. (2) to obtain the trade signs with a stamp of
    1 millisecond
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param times_signs: time of the trades
        :param trade_signs: theoric trade signs from ITCH data
        :param identified_trades: trades signs from eq. (1)
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for number imbalance of '
          ' trades in ms for the stock ' + ticker + ' the ' + year + '.'
          + month + '.' + day)

    times_signs_set = np.array(sorted(set(times_signs)))

    assert not len(trade_signs[trade_signs == 0])
    assert not len(identified_trades[identified_trades == 0])

    trades_exp_ms = np.zeros(len(times_signs_set))
    trades_teo_ms = np.zeros(len(times_signs_set))

    # Implementation of equation (2). Trade sign in each millisecond
    for t_idx, t_val in enumerate(times_signs_set):

        # Experimental
        trades_same_t_exp = identified_trades[times_signs == t_val]
        sign_exp = np.sign(np.sum(trades_same_t_exp))
        trades_exp_ms[t_idx] = sign_exp

        # Theoric
        trades_same_t_teo = trade_signs[times_signs == t_val]
        sign_teo = np.sign(np.sum(trades_same_t_teo))
        trades_teo_ms[t_idx] = sign_teo

    print('Reducing the trades to 1 per millisecond:')
    itch_data_tools.itch_taq_accuracy_msg(trades_teo_ms, trades_exp_ms)

    return (trades_teo_ms, trades_exp_ms)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_eq3_ms_test(ticker, times_signs, trade_signs,
                                     volume_signs, identified_trades, year,
                                     month, day):
    """
    Implementation of the eq. (3) to obtain the trade signs with a stamp of
    1 millisecond.
    Volume imbalance
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param times_signs: time of the trades
        :param trade_signs: theoric trade signs from ITCH data
        :param volume_signs: volume of the trades
        :param identified_trades: trades signs from eq. (1)
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    print('Accuracy of the trade sign classification for volume imbalance of '
          ' trades in ms for the stock ' + ticker + ' the ' + year + '.'
          + month + '.' + day)

    times_signs_set = np.array(sorted(set(times_signs)))

    trades_exp_ms = np.zeros(len(times_signs_set))
    trades_teo_ms = np.zeros(len(times_signs_set))

    # Implementation of equation (3). Trade sign in each millisecond
    for t_idx, t_val in enumerate(times_signs_set):

        # Experimental
        trades_same_t_exp = identified_trades[times_signs == t_val]
        volumes_same_t = volume_signs[times_signs == t_val]
        sign_exp = np.sign(np.sum(trades_same_t_exp * volumes_same_t))
        trades_exp_ms[t_idx] = sign_exp

        # Theoric
        trades_same_t_teo = trade_signs[times_signs == t_val]
        sign_teo = np.sign(np.sum(trades_same_t_teo))
        trades_teo_ms[t_idx] = sign_teo

    print('Reducing the trades to 1 per millisecond:')
    itch_data_tools.itch_taq_accuracy_msg(trades_teo_ms, trades_exp_ms)

    return (trades_teo_ms, trades_exp_ms)

# -----------------------------------------------------------------------------------------------------------------------


def itch_taq_trade_signs_s_test(ticker, times_signs, trade_signs,
                                trades_teo_ms, trades_exp_ms, year, month,
                                day):
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

    times_signs_set = np.array(sorted(set(times_signs)))

    full_time = np.array(range(34800, 57000))
    trades_teo_s_0 = 0. * full_time
    trades_exp_s_0 = 0. * full_time

    for t_idx, t_val in enumerate(full_time):

        condition = (times_signs_set > t_val * 1000) \
                    * (times_signs_set < (t_val + 1) * 1000)
        trades_teo_s_0[t_idx] = np.sign(np.sum(
                                        trades_teo_ms[condition]))
        trades_exp_s_0[t_idx] = np.sign(np.sum(
                                        trades_exp_ms[condition]))

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

        (times_signs, trade_signs,
         volume_signs, price_signs) = itch_taq_trade_signs_load_test(t, year,
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
