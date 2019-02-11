'''
ITCH data generator

Module to compute the following data

- Midpoint price data: using the ITCH data obtain the best bid, best ask,
  quotes and midpoint price data.

- Trade signs data: using the ITCH data obtain the trade signs data.

- Self response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the self response of a stock.

- Self response absolute function: using the midpoint price and the trade
  signs calculate the midpoint log returns and the self response with the
  absolute value of the midpoint log returns of a stock.

- Cross response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the cross response between two
  stocks.

- Average return and average trade sign: using the midpoint price and the
  trade signs calculate the midpoint log returns and the response between the
  product of the averaged midpoint log returns and the averaged trade signs of
  two stocks.

- Difference cross response and average return and average trade sign: using
  the cross response and the average product calculate its difference.

- Zero correlation model: using the midpoint price of a stock and a random
  trade signs array calculate the midpoint log returns and the response
  between the midpoint log returns and the random array.

- Trade sign cross correlator: using the trade signs of two stocks calculate
  the trade sign cross correlator.

- Trade sign self correlator: using the trade signs of two stocks calculate
  the trade sign self correlator.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

import numpy as np
import os

import gzip
import pickle

import itch_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------------------------------------------------


def itch_midpoint_data(ticker, year, month, day, t_step):
    """
    Obtain the midpoint price from the ITCH 2016 data. For further calculations
    we use the full time range from the opening of the market at 9h30 to the
    closing at 16h in milliseconds and then convert the values to hours (23.4
    million data). To fill the time spaces when nothing happens we replicate
    the last value calculated until a change in the price happens. Save in a
    different pickle file the array of each of the following values: best bid,
    best ask, spread, midpoint price and time.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param t_step: time step in the data in ms
    """

    function_name = itch_midpoint_data.__name__
    itch_data_tools.itch_function_header_print_data(function_name, ticker,
                                                    ticker, year, month, day,
                                                    t_step)

    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_{1}/{1}{2}{3}_{0}.csv.gz'
                         .format(ticker, year, month, day)), dtype='str',
                         skip_header=1, delimiter=',')

    # Lists of times, ids, types, volumes and prices
    # List of all the available information available in the data excluding
    # the last two columns

    times_ = np.array([int(mytime) for mytime in data[:, 0]])
    ids_ = np.array([int(myid) for myid in data[:, 2]])

    # List of order types:
    # "B" = 1 - > Add buy order
    # "S" = 2 - > Add sell order
    # "E" = 3 - > Execute outstanding order in part
    # "C" = 4 - > Cancel outstanding order in part
    # "F" = 5 - > Execute outstanding order in full
    # "D" = 6 - > Delete outstanding order in full
    # "X" = 7 - > Bulk volume for the cross event
    # "T" = 8 - > Execute non-displayed order

    types_ = np.array([1 * (mytype == 'B') +
                       2 * (mytype == 'S') +
                       3 * (mytype == 'E') +
                       4 * (mytype == 'C') +
                       5 * (mytype == 'F') +
                       6 * (mytype == 'D') +
                       7 * (mytype == 'X') +
                       8 * (mytype == 'T') for mytype in data[:, 3]])
    prices_ = np.array([int(myprice) for myprice in data[:, 5]])

    ids = ids_[types_ < 7]
    times = times_[types_ < 7]
    types = types_[types_ < 7]
    prices = prices_[types_ < 7]

    # Reference lists
    # Reference lists using the original values or the length of the original
    # lists

    prices_ref = 1 * prices
    types_ref = 0 * types
    times_ref = 0 * times
    index_ref = 0 * types
    newids = {}
    insertnr = {}
    hv = 0

    # Help lists with the data of the buy orders and sell orders

    hv_prices = prices[types < 3]
    hv_types = types[types < 3]
    hv_times = times[types < 3]

    # Fill the reference lists where the values of 'T' are 'E', 'C', 'F', 'D'

    # For the data in the length of the ids list (all data)
    for iii in range(len(ids)):

        # If the data is a sell or buy order
        if (types[iii] < 3):

            # Insert in the dictionary newids a key with the valor of the id
            # and the value of hv (a counter)
            newids[ids[iii]] = hv

            # Insert in the dictionary insertnr a key with the valor of the id
            # and the value of the for counter
            insertnr[ids[iii]] = iii

            # Increase the value of hv
            hv += 1

        # If the data is not a sell or buy order
        else:

            # Fill the values of prices_ref with no prices ('E', 'C', 'F', 'D')
            # with the price of the order
            prices_ref[iii] = hv_prices[newids[ids[iii]]]
            # Fill the values of types_ref with no  prices ('E', 'C', 'F', 'D')
            # with the type of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]
            # Fill the values of time_ref with no  prices ('E', 'C', 'F', 'D')
            # with the time of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]
            # Fill the values of index_ref with no  prices ('E', 'C', 'F', 'D')
            # with the position of the sell or buy order
            index_ref[iii] = insertnr[ids[iii]]

    # Minimum and maximum trade price

    # The minimum price allowed is 0.9 times the price of
    # the minimum value of all full executed orders.
    minP = round(0.9 * (1. * prices_ref[types == 5] / 10000).min(), 2)
    # The maximum price allowed is 1.1 times the price of
    # the maximum value of all full executed orders.
    maxP = round(1.1 * (1. * prices_ref[types == 5] / 10000).max(), 2)
    # Values between maxP and minP with step of 0.01 cents
    valuesP = minP + 0.01 * np.arange(int((maxP - minP) / 0.01))
    maxP = valuesP.max()

    # Construct quotes and spread

    nAsk = 0 * valuesP      # Sell values started at 0
    nAsk[-1] = 1            # Last value of nAsk set to 1
    nBid = 0 * valuesP      # Buy values starte at 0
    nBid[0] = 1             # First value of nBid set to 1
    bestAsk = 10000000.     # Set bestAsk and bestAskOld a high value
    bestAskOld = 10000000.
    bestBid = 0.            # Set bestBid and bestBidOld a low value
    bestBidOld = 0.
    bestAsks = []           # Create lists for best asks, bids and times
    bestBids = []
    bestTimes = []

    # Finding the best asks and best bids

    # For the data in the length of the ids list (all data)
    for iii in range(len(ids)):

        # Incoming limit orders

        myPriceIndex = int(round(1. * (1. * prices_ref[iii] / 10000 - minP)
                           / 0.01))

        # Initializing bestAksOld and bestBidOld
        bestAskOld = 1 * bestAsk
        bestBidOld = 1 * bestBid

        # The price is greater than the minP
        if (myPriceIndex >= 0 and
                myPriceIndex < len(valuesP)):

            # If the order is a sell
            if (types[iii] == 2):

                if (nAsk[myPriceIndex] == 0):

                    # The bestAsk is the minimum value between the previous
                    # bestAsk and the value in valuesP with id myPriceIndex
                    bestAsk = min(bestAsk, valuesP[myPriceIndex])

                # Increase the value of nAsk to 1 (value arrived the book)
                nAsk[myPriceIndex] += 1

            # If the order is a buy
            if (types[iii] == 1):

                if (nBid[myPriceIndex] == 0):

                    # The bestBid is the maximum value between the previous
                    # bestBid and the value in valuesP with id myPriceIndex
                    bestBid = max(bestBid, valuesP[myPriceIndex])

                # Increase the value of nBid to 1 (value arrived the book)
                nBid[myPriceIndex] += 1

            # limit orders completely leaving

            # If the order is a full executed order or if the order is a full
            # delete order
            if (types[iii] == 5 or
                    types[iii] == 6):

                # If the order is a sell
                if (types_ref[iii] == 2):

                    # Reduce the value in nAsk to 0 (value left the book)
                    nAsk[myPriceIndex] -= 1

                    # If the value is not in the book and if the value is the
                    # best ask
                    if (nAsk[myPriceIndex] == 0 and
                            valuesP[myPriceIndex] == bestAsk):

                        # The best ask is the minimum value of the prices that
                        # are currently in the order book
                        bestAsk = valuesP[nAsk > 0].min()

                else:

                    # Reduce the value in nBid to 0 (value left the book)
                    nBid[myPriceIndex] -= 1

                    # If the value is not in the book and if the value is the
                    # best bid
                    if (nBid[myPriceIndex] == 0 and
                            valuesP[myPriceIndex] == bestBid):

                        # The best bid is the maximum value of the prices that
                        # are currently in the order book
                        bestBid = valuesP[nBid > 0].max()

        # If the bestAsk changes or and if the bestBid changes
        if (bestAsk != bestAskOld or
                bestBid != bestBidOld):

            # Append the values of bestTimes, bestAsks and bestBids
            bestTimes.append(times[iii])
            bestAsks.append(bestAsk)
            bestBids.append(bestBid)
            bestAskOld = bestAsk
            bestBidOld = bestBid

    # Calculating the spread, midpoint and time

    # Calculating the spread
    spread_ = np.array(bestAsks) - np.array(bestBids)
    # Transforming bestTimes in an array
    timesS = np.array(bestTimes)
    midpoint_ = 1. * (np.array(bestAsks) + np.array(bestBids)) / 2

    # Setting the values in the open market time

    # This line behaves as an or the two arrays must achieve a condition, in
    # this case, be in the market trade hours
    day_times_ind = (1. * timesS / 3600 / 1000 > 9.5) * \
                    (1. * timesS / 3600 / 1000 < 16) > 0

    # Midpoint in the market trade hours
    midpoint = 1. * midpoint_[day_times_ind]
    # Time converted to hours in the market trade hours
    times_spread = 1. * timesS[day_times_ind]
    bestAsks = np.array(bestAsks)[day_times_ind]
    bestBids = np.array(bestBids)[day_times_ind]
    # Spread in the market trade hours
    spread = spread_[day_times_ind]

    # Completing the full time entrances

    # 34 200 000 ms = 9h30 - 57 600 000 ms = 16h
    full_time = np.array(range(34200000, 57600000))

    # As there can be several values for the same millisecond, we use the
    # first value of each millisecond in the full time array as is the
    # easier way to obtain the value and it behaves quiet equal as the
    # original input

    midpoint_last_val = 0. * full_time
    midpoint_last_val[-1] = midpoint[0]

    bestAsks_last_val = 0. * full_time
    bestAsks_last_val[-1] = midpoint[0]

    bestBids_last_val = 0. * full_time
    bestBids_last_val[-1] = midpoint[0]

    spread_last_val = 0. * full_time
    spread_last_val[-1] = midpoint[0]

    count = 0

    for t_idx, t_val in enumerate(full_time):

        if (count < len(times_spread) and t_val == times_spread[count]):

            count += 1

            while (count < len(times_spread) and
                   times_spread[count - 1] == times_spread[count]):

                count += 1

            midpoint_last_val[t_idx] = midpoint[count - 1]
            bestAsks_last_val[t_idx] = bestAsks[count - 1]
            bestBids_last_val[t_idx] = bestBids[count - 1]
            spread_last_val[t_idx] = spread[count - 1]

        else:

            midpoint_last_val[t_idx] = midpoint_last_val[t_idx - 1]
            bestAsks_last_val[t_idx] = bestAsks_last_val[t_idx - 1]
            bestBids_last_val[t_idx] = bestBids_last_val[t_idx - 1]
            spread_last_val[t_idx] = spread_last_val[t_idx - 1]

    # Saving data

    if (not os.path.isdir('../itch_data_{2}/{0}_{5}ms/'
                          .format(function_name, ticker, year, month, day,
                                  t_step))):

        os.mkdir('../itch_data_{2}/{0}_{5}ms/'
                 .format(function_name, ticker, year, month, day, t_step))
        print('Folder to save data created')

    pickle.dump(bestAsks_last_val,
                open(''.join(('../itch_data_{2}/{0}_{5}ms/{0}_ask_{2}{3}{4}'
                     + '_{1}_{5}ms.pickle').split())
                     .format(function_name, ticker, year, month, day, t_step),
                     'wb'))
    pickle.dump(bestBids_last_val,
                open(''.join(('../itch_data_{2}/{0}_{5}ms/{0}_bid_{2}{3}{4}'
                     + '_{1}_{5}ms.pickle').split())
                     .format(function_name, ticker, year, month, day, t_step),
                     'wb'))
    pickle.dump(spread_last_val,
                open(''.join(('../itch_data_{2}/{0}_{5}ms/{0}_spread_{2}{3}{4}'
                     + '_{1}_{5}ms.pickle').split())
                     .format(function_name, ticker, year, month, day, t_step),
                     'wb'))
    pickle.dump(full_time,
                open('../itch_data_{1}/{0}_{2}ms/{0}_time_{2}ms.pickle'
                     .format(function_name, year, t_step), 'wb'))
    pickle.dump(midpoint_last_val,
                open(''.join(('../itch_data_{2}/{0}_{5}ms/{0}_midpoint'
                     + '_{2}{3}{4}_{1}_{5}ms.pickle').split())
                     .format(function_name, ticker, year, month, day, t_step),
                     'wb'))

    print('Data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_trade_signs_data(ticker, year, month, day, t_step):
    """
    Obtain the trade signs from the ITCH data. For further calculations
    we use the whole time range from the opening of the market at 9h30 to the
    closing at 16h in milliseconds and then convert the values to hours (23.4
    million data). To fill the time spaces when nothing happens we just fill
    with zeros indicating that there were neither a buy nor a sell. Save in a
    pickle file the array of the trade signs
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param t_step: time step in the data in ms
    """''

    function_name = itch_trade_signs_data.__name__
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

    ids = ids_[types_ < 7]
    times = times_[types_ < 7]
    types = types_[types_ < 7]

    # Reference lists
    # Reference lists using the original values or the length of the original
    # lists

    types_ref = 0 * types
    times_ref = 0 * times
    newids = {}
    hv = 0

    # Help lists with the data of the buy orders and sell orders

    hv_types = types[types < 3]
    hv_times = times[types < 3]

    trade_sign = 0 * types

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

            trade_sign[iii] = 0

        # If the data is not a sell or buy order
        elif (types[iii] == 3 or
                types[iii] == 5):

            # Fill the values of types_ref with no  prices ('E', 'C', 'F', 'D')
            # with the type of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]

            # Fill the values of time_ref with no  prices ('E', 'C', 'F', 'D')
            # with the time of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]

            if (hv_types[newids[ids[iii]]] == 2):

                trade_sign[iii] = 1.

            elif (hv_types[newids[ids[iii]]] == 1):

                trade_sign[iii] = - 1.

        else:

            # Fill the values of types_ref with no  prices ('E', 'C', 'F', 'D')
            # with the type of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]

            # Fill the values of time_ref with no  prices ('E', 'C', 'F', 'D')
            # with the time of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]

            trade_sign[iii] = 0

    # Ordering the data in the open market time

    # This line behaves as an or.the two arrays must achieve a condition, in
    # this case, be in the market trade hours
    day_times_ind = (1. * times / 3600 / 1000 > 9.5) * \
                    (1. * times / 3600 / 1000 < 16) > 0

    trade_signs = trade_sign[day_times_ind]
    times_signs = times[day_times_ind]

    # Completing the full time entrances

    # 34 200 000 ms = 9h30 - 57 600 000 ms = 16h
    full_time = np.array(range(34200000, 57600000))

    # As there can be several values for the same millisecond, we use the most
    # used trade value of each millisecond in the full time array as it
    # behaves quiet similar as the original input

    count = 0
    trade_signs_complete_most = 0. * full_time

    for t_idx, t_val in enumerate(full_time):

        most = 0

        if (count < len(times_signs) and t_val == times_signs[count]):

            most += trade_signs[count]

            count += 1

            while (count < len(times_signs) and
                    times_signs[count - 1] == times_signs[count]):

                most += trade_signs[count]
                count += 1

            if (most > 0):

                trade_signs_complete_most[t_idx] = 1.

            elif (most < 0):

                trade_signs_complete_most[t_idx] = -1.

    # Saving data

    itch_data_tools.itch_save_data(function_name, trade_signs_complete_most,
                                   ticker, ticker, year, month, day, t_step)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_self_response_data(ticker, year, month, day, tau_val, t_step):
    """
    Obtain the self response function using the midpoint log returns
    and trade signs of ticker i during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    function_name = itch_self_response_data.__name__
    itch_data_tools.itch_function_header_print_data(function_name, ticker,
                                                    ticker, year, month, day,
                                                    str(t_step))

    # Load data
    midpoint_i = pickle.load(open(''.join((
                '../itch_data_{1}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker, year, month, day), 'rb'))
    trade_sign_i = pickle.load(open("".join((
                '../itch_data_{1}/itch_trade_signs_data_1ms/itch_trade_signs'
                + '_data_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker, year, month, day), 'rb'))
    time = pickle.load(open(''.join((
                '../itch_data_{}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_time_1ms.pickle').split())
                .format(year), 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(__tau__)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # reshape and average data of trade signs
    (trade_sign_i_sec_avg,
     trade_sign_i_sec_nr) = itch_data_tools.itch_trade_sign_reshape(
                                                 trade_sign_i, time_t_step)

    # Calculating the midpoint log return and the cross response function

    for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                    int(tau_val * 1E-3))):

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau_v:]/midpoint_i_sec[:-tau_v]), np.zeros(tau_v))

        self_response_tau[tau_idx] = np.mean(
            log_return_i_sec[trade_sign_i_sec_nr != 0] *
            trade_sign_i_sec_avg[trade_sign_i_sec_nr != 0])

    # Saving data

    itch_data_tools.itch_save_data(function_name, self_response_tau, ticker,
                                   ticker, year, month, day, str(t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_self_response_abs_data(ticker, year, month, day, tau_val, t_step):
    """
    Obtain the self response using the average of the absolute value of the
    midpoint log return of ticker i during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2017')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    function_name = itch_self_response_abs_data.__name__
    itch_data_tools.itch_function_header_print_data(function_name, ticker,
                                                    ticker, year, month, day,
                                                    str(t_step))

    # Load data
    midpoint_i = pickle.load(open(''.join((
                '../itch_data_{1}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker, year, month, day), 'rb'))
    time = pickle.load(open(''.join((
                '../itch_data_{}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_time_1ms.pickle').split())
                .format(year), 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(__tau__)

    # Using values t_step millisecond
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # Calculating the midpoint log return and the cross response functions

    for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                    int(tau_val * 1E-3))):

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau_v:]/midpoint_i_sec[:-tau_v]), np.zeros(tau_v))

        self_response_tau[tau_idx] = np.mean(np.abs(log_return_i_sec))

    # Saving data

    itch_data_tools.itch_save_data(function_name, self_response_tau, ticker,
                                   ticker, year, month, day, str(t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_zero_correlation_model_data(ticker, year, month, day, tau_val,
                                     t_step):
    """
    Obtain the cross response function using the midpoint log return of
    ticker i and random trade signs during different time lags. The data is
    adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    function_name = itch_zero_correlation_model_data.__name__
    itch_data_tools.itch_function_header_print_data(function_name, ticker,
                                                    ticker, year, month, day,
                                                    str(t_step))

    # Load data
    midpoint_i = pickle.load(open(''.join((
                '../itch_data_{1}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker, year, month, day), 'rb'))
    time = pickle.load(open(''.join((
                '../itch_data_{}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_time_1ms.pickle').split())
                .format(year), 'rb'))

    # Setting variables to work with 1s accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    cross_response_tau = np.zeros(__tau__)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from ms to s
    time_t_step = time[::t_step]

    # Calculating the midpoint log return and the cross response functions

    for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                    int(tau_val * 1E-3))):

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau_v:] / midpoint_i_sec[:-tau_v]), np.zeros(tau_v))

        trade_sign_rand = np.random.rand(len(time_t_step))
        trade_sign_rand_j = (1 * (trade_sign_rand > 0.5)
                             - 1 * (trade_sign_rand <= 0.5))

        cross_response_tau[tau_idx] = np.mean(
            log_return_i_sec * trade_sign_rand_j)

    # Saving data

    itch_data_tools.itch_save_data(function_name, cross_response_tau, ticker,
                                   ticker, year, month, day, t_step)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_cross_response_data(ticker_i, ticker_j, year, month, day, tau_val,
                             t_step):
    """
    Obtain the cross response function using the midpoint log returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """
    if (ticker_i == ticker_j):

        return None

    else:

        function_name = itch_cross_response_data.__name__
        itch_data_tools.itch_function_header_print_data(function_name,
                                                        ticker_i, ticker_j,
                                                        year, month, day,
                                                        str(t_step))

        # Load data
        midpoint_i = pickle.load(open(''.join((
                '../itch_data_{1}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker_i, year, month, day), 'rb'))
        trade_sign_j = pickle.load(open("".join((
                '../itch_data_{1}/itch_trade_signs_data_1ms/itch_trade_signs'
                + '_data_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker_j, year, month, day), 'rb'))
        time = pickle.load(open(''.join((
                '../itch_data_{}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_time_1ms.pickle').split())
                .format(year), 'rb'))

        # Setting variables to work with t_step ms accuracy

        # Array of the average of each tau. 10^3 s used by Wang
        cross_response_tau = np.zeros(__tau__)

        # Using values each second
        midpoint_i_sec = midpoint_i[::t_step]
        # Changing time from 1 ms to t_step ms
        time_t_step = time[::t_step]

        # reshape and average data of trade signs
        (trade_sign_j_sec_avg,
         trade_sign_j_sec_nr) = itch_data_tools.itch_trade_sign_reshape(
                                                    trade_sign_j, time_t_step)

        # Calculating the midpoint log return and the cross response function

        # Depending on the ta
        for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                        int(tau_val * 1E-3))):

            # Obtain the midpoint log return. Displace the numerator tau
            # values to the right and compute the return, and append the
            # remaining values of tau with zeros
            log_return_i_sec = np.append(np.log(
                midpoint_i_sec[tau_v:]/midpoint_i_sec[:-tau_v]),
                np.zeros(tau_v))

            cross_response_tau[tau_idx] = np.mean(
                log_return_i_sec[trade_sign_j_sec_nr != 0] *
                trade_sign_j_sec_avg[trade_sign_j_sec_nr != 0])

        # Saving data

        itch_data_tools.itch_save_data(function_name, cross_response_tau,
                                       ticker_i, ticker_j, year, month, day,
                                       str(t_step))

        return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_avg_return_avg_trade_prod_data(ticker_i, ticker_j, year, month, day,
                                        tau_val, t_step):
    """
    Obtain the result of the product between the averaged midpoint log return
    of ticker i and the averaged trade signs of ticker j during different time
    lags. The data is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock
         to be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    if (ticker_i == ticker_j):

        return None

    else:

        function_name = itch_avg_return_avg_trade_prod_data.__name__
        itch_data_tools.itch_function_header_print_data(function_name,
                                                        ticker_i, ticker_j,
                                                        year, month, day,
                                                        str(t_step))

        # Load data
        midpoint_i = pickle.load(open(''.join((
                '../itch_data_{1}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_midpoint_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker_i, year, month, day), 'rb'))
        trade_sign_j = pickle.load(open("".join((
                '../itch_data_{1}/itch_trade_signs_data_1ms/itch_trade_signs'
                + '_data_{1}{2}{3}_{0}_1ms.pickle').split())
                .format(ticker_j, year, month, day), 'rb'))
        time = pickle.load(open(''.join((
                '../itch_data_{}/itch_midpoint_data_1ms/itch_midpoint_data'
                + '_time_1ms.pickle').split())
                .format(year), 'rb'))

        # Setting variables to work with t_step ms accuracy

        # Array of the average of each tau. 10^3 s used by Wang
        avg_return_sign = np.zeros(__tau__)

        # Using values each second
        midpoint_i_sec = midpoint_i[::t_step]
        # Changing time from 1 ms to t_step ms
        time_t_step = time[::t_step]

        # reshape and average data of trade signs
        (trade_sign_j_sec_avg,
         trade_sign_j_sec_nr) = itch_data_tools.itch_trade_sign_reshape(
                                                    trade_sign_j, time_t_step)

        # Calculating the midpoint log return and the cross response functions

        for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                        int(tau_val * 1E-3))):

            # Obtain the midpoint log return. Displace the numerator tau values
            # to the right and compute the return, and append the remaining
            # values of tau with zeros
            log_return_i_sec = np.append(np.log(
                        midpoint_i_sec[tau_v:]/midpoint_i_sec[:-tau_v]),
                        np.zeros(tau_v))

            avg_return_sign[tau_idx] = (
                np.mean(log_return_i_sec[trade_sign_j_sec_nr != 0]) *
                np.mean(trade_sign_j_sec_avg[trade_sign_j_sec_nr != 0]))

        # Saving data

        itch_data_tools.itch_save_data(function_name, avg_return_sign,
                                       ticker_i, ticker_j, year, month, day,
                                       str(t_step))

        return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_difference_cross_response_avg_prod_data(ticker_i, ticker_j, year,
                                                 month, day, t_step):

    if (ticker_i == ticker_j):

        return None

    else:

        function_name = itch_difference_cross_response_avg_prod_data.__name__
        itch_data_tools.itch_function_header_print_data(function_name,
                                                        ticker_i, ticker_j,
                                                        year, month, day,
                                                        str(t_step))

        # Load data
        cross_response = pickle.load(open(''.join((
            '../itch_data_{2}/itch_cross_response_data_{5}ms/itch_cross'
            + '_response_data_{2}{3}{4}_{0}i_{1}j_{5}ms.pickle').split())
            .format(ticker_i, ticker_j, year, month, day, t_step), 'rb'))
        avg_return_avg_trade = pickle.load(open(''.join((
            '../itch_data_{2}/itch_avg_return_avg_trade_prod_data_{5}ms/itch'
            + '_avg_return_avg_trade_prod_data_{2}{3}{4}_{0}i_{1}j_{5}ms.'
            + 'pickle').split())
            .format(ticker_i, ticker_j, year, month, day, t_step), 'rb'))

        difference = cross_response - avg_return_avg_trade

        # Saving data

        itch_data_tools.itch_save_data(function_name, difference, ticker_i,
                                       ticker_j, year, month, day, str(t_step))

        return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_trade_sign_self_correlator_data(ticker_i, day, tau_val, t_step):
    """
    Obtain the trade sign self correlator using the trade signs of ticker i
    during different time lags. The data is adjusted to use only the values
    each t_step ms
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """
    print('trade sign cross correlator data')
    print('Processing data for the stock i ' + ticker_i + ' the day ' + day
          + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    trade_sign_i = pickle.load(open(''.join((
                '../Data/trade_signs_data_1ms/trade_signs_data_201603{}'
                + '_{}i_1ms.pickl').split())
                .format(day, ticker_i), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    self_correlator = np.zeros(__tau__)

    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # reshape and average data of trade signs
    (trade_sign_i_sec_avg,
     trade_sign_i_sec_nr) = itch_data_tools.trade_sign_reshape(
        trade_sign_i, time_t_step)

    # Calculating the midpoint log return and the cross response function

    for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                    int(tau_val * 1E-3))):

        trade_sign_product = np.append(trade_sign_i_sec_avg[tau_v:]
                                       * trade_sign_i_sec_avg[:-tau_v],
                                       np.zeros(tau_v))

        self_correlator[tau_idx] = np.mean(
            trade_sign_product[trade_sign_i_sec_nr != 0])

    # Saving data

    function_name = trade_sign_self_correlator_data.__name__
    itch_data_tools.save_data(function_name, self_correlator, ticker_i,
                              ticker_i, day, t_step)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_trade_sign_autocorrelation_data(ticker_i, day, tau_val, t_step):
    """
    Obtain the trade sign autocorrelation using the trade signs of ticker i
    during different time lags. The data is adjusted to use only the values
    each t_step ms
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """
    print('Trade sign autocorrelation data')
    print('Processing data for the stock i ' + ticker_i + ' the day ' + day
          + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    trade_sign_i = pickle.load(open(''.join((
                '../Data/trade_signs_data_1ms/trade_signs_data_201603{}'
                + '_{}i_1ms.pickl').split())
                .format(day, ticker_i), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    trade_sign_autocorrelation = np.zeros(__tau__)

    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # reshape and average data of trade signs
    (trade_sign_i_sec_avg,
     trade_sign_i_sec_nr) = itch_data_tools.trade_sign_reshape(
        trade_sign_i, time_t_step)

    # Calculating the midpoint log return and the cross response function

    trade_mean_square = (np.mean(
                            trade_sign_i_sec_avg[trade_sign_i_sec_nr != 0])
                         * np.mean(
                            trade_sign_i_sec_avg[trade_sign_i_sec_nr != 0]))

    trade_square_mean = np.mean(
                            trade_sign_i_sec_avg[trade_sign_i_sec_nr != 0]
                            * trade_sign_i_sec_avg[trade_sign_i_sec_nr != 0])

    for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                    int(tau_val * 1E-3))):

        trade_sign_product = np.append(trade_sign_i_sec_avg[tau_v:]
                                       * trade_sign_i_sec_avg[:-tau_v],
                                       np.zeros(tau_v))

        trade_sign_product_mean = np.mean(
            trade_sign_product[trade_sign_i_sec_nr != 0])

        trade_sign_autocorrelation[tau_idx] = (
            (trade_sign_product_mean - trade_mean_square)
            / (trade_square_mean - trade_mean_square))

    # Saving data

    function_name = trade_sign_autocorrelation_data.__name__
    itch_data_tools.save_data(function_name, trade_sign_autocorrelation,
                              ticker_i, ticker_i, day, t_step)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def itch_trade_sign_cross_correlator_data(ticker_i, ticker_j, day, tau_val, t_step):
    """
    Obtain the trade sign cross correlator using the trade signs of ticker i
    and j during different time lags. The data is adjusted to use only the
    values each t_step ms
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """
    if (ticker_i == ticker_j):

        return None

    else:

        print('trade sign cross correlator data')
        print('Processing data for the stock i ' + ticker_i + ' and stock j '
              + ticker_j + ' the day ' + day + ' March, 2016')
        print('Time step: ', t_step, 'ms')

        # Load data
        trade_sign_i = pickle.load(open(''.join((
                    '../Data/trade_signs_data_1ms/trade_signs_data_201603{}'
                    + '_{}i_1ms.pickl').split())
                    .format(day, ticker_i), 'rb'))
        trade_sign_j = pickle.load(open(''.join((
                    '../Data/trade_signs_data_1ms/trade_signs_data_201603{}'
                    + '_{}i_1ms.pickl').split())
                    .format(day, ticker_j), 'rb'))
        time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

        # Setting variables to work with t_step ms accuracy

        # Array of the average of each tau. 10^3 s used by Wang
        cross_correlator = np.zeros(__tau__)

        # Changing time from 1 ms to t_step ms
        time_t_step = time[::t_step]

        # reshape and average data of trade signs
        trade_sign_i_sec_avg, _ = itch_data_tools.trade_sign_reshape(
            trade_sign_i, time_t_step)
        (trade_sign_j_sec_avg,
         trade_sign_j_sec_nr) = itch_data_tools.trade_sign_reshape(
            trade_sign_j, time_t_step)

        # Calculating the midpoint log return and the cross response function

        for tau_idx, tau_v in enumerate(range(1, tau_val + 1,
                                        int(tau_val * 1E-3))):

            trade_sign_product = np.append(trade_sign_i_sec_avg[tau_v:]
                                           * trade_sign_j_sec_avg[:-tau_v],
                                           np.zeros(tau_v))

            cross_correlator[tau_idx] = np.mean(
                trade_sign_product[trade_sign_j_sec_nr != 0])

        # Saving data

        function_name = trade_sign_cross_correlator_data.__name__
        itch_data_tools.save_data(function_name, cross_correlator, ticker_i,
                                  ticker_j, day, t_step)

        return None

# -----------------------------------------------------------------------------------------------------------------------

def main():

    return None


if __name__ == '__main__':
    main()
