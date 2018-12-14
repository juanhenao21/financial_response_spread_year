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

- Zero correlation model: using the midpoint price of a stock and a random
  trade signs array calculate the midpoint log returns and the response
  between the midpoint log retuns and the random array.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

import numpy as np
import os

import gzip
import pickle

# -----------------------------------------------------------------------------------------------------------------------


def midpoint_data(ticker, day):
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
        :param day: string of the day to be analized (i.e '07')
    """

    print('Midpoint price data')
    print('Processing data for the stock', ticker, 'the day', day +
          ' March, 2016')

    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_2016/201603{}_{}.csv.gz'
                         .format(day, ticker)), dtype='str', skip_header=1,
                         delimiter=',')

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

    midpoint_first_val = 0. * full_time
    midpoint_first_val[-1] = midpoint[0]

    bestAsks_first_val = 0. * full_time
    bestAsks_first_val[-1] = midpoint[0]

    bestBids_first_val = 0. * full_time
    bestBids_first_val[-1] = midpoint[0]

    spread_first_val = 0. * full_time
    spread_first_val[-1] = midpoint[0]

    count = 0

    for t_idx, t_val in enumerate(full_time):

        if (count < len(times_spread) and t_val == times_spread[count]):

            midpoint_first_val[t_idx] = midpoint[count]
            bestAsks_first_val[t_idx] = bestAsks[count]
            bestBids_first_val[t_idx] = bestBids[count]
            spread_first_val[t_idx] = spread[count]

            count += 1

            while (count < len(times_spread) and
                   times_spread[count - 1] == times_spread[count]):

                count += 1

        else:

            midpoint_first_val[t_idx] = midpoint_first_val[t_idx - 1]
            bestAsks_first_val[t_idx] = bestAsks_first_val[t_idx - 1]
            bestBids_first_val[t_idx] = bestBids_first_val[t_idx - 1]
            spread_first_val[t_idx] = spread_first_val[t_idx - 1]

    # Saving data

    if (not os.path.isdir('../Data/midpoint_data/')):

        os.mkdir('../Data/midpoint_data/')
        print('Folder to save data created')

    pickle.dump(bestAsks_first_val,
                open('../Data/midpoint_data/bestAsks_201603{}_{}.pickl'
                     .format(day, ticker), 'wb'))
    pickle.dump(bestBids_first_val,
                open('../Data/midpoint_data/bestBids_201603{}_{}.pickl'
                     .format(day, ticker), 'wb'))
    pickle.dump(spread_first_val,
                open('../Data/midpoint_data/spread_201603{}_{}.pickl'
                     .format(day, ticker), 'wb'))
    pickle.dump(full_time, open('../Data/midpoint_data/time.pickl', 'wb'))
    pickle.dump(midpoint_first_val,
                open('../Data/midpoint_data/midpoint_201603{}_{}.pickl'
                     .format(day, ticker), 'wb'))

    print('Midpoint price data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def trade_signs_data(ticker, day):
    """
    Obtain the trade signs from the ITCH 2016 data. For further calculations
    we use the whole time range from the opening of the market at 9h30 to the
    closing at 16h in milliseconds and then convert the values to hours (23.4
    million data). To fill the time spaces when nothing happens we just fill
    with zeros indicating that there were neither a buy nor a sell. Save in a
    pickle file the array of the trade signs
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
    """''

    print('Trade signs data')
    print('Processing data for the stock', ticker, 'the day', day +
          ' March, 2016')

    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_2016/201603{}_{}.csv.gz'
                         .format(day, ticker)),
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

    if (not os.path.isdir('../Data/trade_signs_data/')):

        os.mkdir('../Data/trade_signs_data/')
        print('Folder to save data created')

    pickle.dump(trade_signs_complete_most, open(
            '../Data/trade_signs_data/trade_signs_most_201603{}_{}.pickl'
            .format(day, ticker), 'wb'))

    print('Trade signs data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def self_response_data(ticker_i, day, tau_val, t_step):
    """
    Obtain the self response function using the midpoint log returns
    and trade signs of ticker i during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    print('Self response function data')
    print('Processing data for the stock i ' + ticker_i + ' the day ' + day
          + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    midpoint_i = pickle.load(open(
                '../Data/midpoint_data/midpoint_201603{}_{}.pickl'
                .format(day, ticker_i), 'rb'))
    trade_sign_j = pickle.load(open(
                '../Data/trade_signs_data/trade_signs_most_201603{}_{}.pickl'
                .format(day, ticker_i), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(tau_val)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # Reshape the array in group of values of t_step ms and infer the number
    # of rows, then sum all rows.
    trade_sign_j_sec_sum = np.sum(np.reshape(trade_sign_j, (t_step, -1)),
                                  axis=0)

    # Reasign the trade sign, if the value of the array is greater than 0
    # gives a 1 and -1 for the contrary.
    trade_sign_j_sec_avg = 1 * (trade_sign_j_sec_sum > 0) \
        - 1 * (trade_sign_j_sec_sum < 0)
    # Reshape the array in group of values of t_step ms and infer the number
    # rows, then sum the absolute value of all rows. This is used to know
    # where a trade sign is cero.
    trade_sign_j_sec_nr = np.sum(np.reshape(np.absolute(trade_sign_j),
                                 (t_step, -1)), axis=0)

    # Calculating the midpoint log return and the cross response function

    for tau in range(1, tau_val):

        # Every second have a log-return
        log_return_i_sec = 0. * time_t_step

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau:]/midpoint_i_sec[:-tau]), np.zeros(tau))

        self_response_tau[tau] = np.mean(
            log_return_i_sec[trade_sign_j_sec_nr != 0] *
            trade_sign_j_sec_avg[trade_sign_j_sec_nr != 0])

    # Saving data

    if (not os.path.isdir('../Data/self_response_data_{}ms/'.format(t_step))):

        os.mkdir('../Data/self_response_data_{}ms/'.format(t_step))
        print('Folder to save data created')

    pickle.dump(self_response_tau, open(
        '../Data/self_response_data_{}ms/self_201603{}_{}i_{}ms.pickl'
        .format(t_step, day, ticker_i, t_step), 'wb'))

    print('Self response function data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def self_response_abs_data(ticker_i, day, tau_val, t_step):
    """
    Obtain the self response using the average of the absolute value of the
    midpoint log return of ticker i during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    print('Self response absolute value data')
    print('Processing data for the stock i ' + ticker_i + ' the day '
          + day + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    midpoint_i = pickle.load(open(
                '../Data/midpoint_data/midpoint_201603{}_{}.pickl'.format
                (day, ticker_i), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    self_response_tau = np.zeros(tau_val)

    # Using values t_step millisecond
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # Calculating the midpoint log return and the cross response functions

    for tau in range(1, tau_val):

        # Every second have a log-return
        log_return_i_sec = 0. * time_t_step

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau:]/midpoint_i_sec[:-tau]), np.zeros(tau))

        self_response_tau[tau] = np.mean(np.abs(log_return_i_sec))

    # Saving data

    if (not os.path.isdir('../Data/self_response_abs_data_{}ms/'
                          .format(t_step))):

        os.mkdir('../Data/self_response_abs_data_{}ms/'.format(t_step))
        print('Folder to save data created')

    pickle.dump(self_response_tau, open(
        '../Data/self_response_abs_data_{}ms/self_abs_201603{}_{}i_{}ms.pickl'
        .format(t_step, day, ticker_i, t_step), 'wb'))

    print('Self response absolute functions data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def cross_response_data(ticker_i, ticker_j, day, tau_val, t_step):
    """
    Obtain the cross response function using the midpoint log returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    print('Cross response function data')
    print('Processing data for the stock i ' + ticker_i + ' and stock j ' +
          ticker_j + ' the day ' + day + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    midpoint_i = pickle.load(open(
                '../Data/midpoint_data/midpoint_201603{}_{}.pickl'
                .format(day, ticker_i), 'rb'))
    trade_sign_j = pickle.load(open(
                '../Data/trade_signs_data/trade_signs_most_201603{}_{}.pickl'
                .format(day, ticker_j), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    cross_response_tau = np.zeros(tau_val)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # Reshape the array in group of values of t_step ms and infer the number
    # of rows, then sum all rows.
    trade_sign_j_sec_sum = np.sum(np.reshape(trade_sign_j, (t_step, -1)),
                                  axis=0)

    # Reasign the trade sign, if the value of the array is greater than 0
    # gives a 1 and -1 for the contrary.
    trade_sign_j_sec_avg = 1 * (trade_sign_j_sec_sum > 0) \
        - 1 * (trade_sign_j_sec_sum < 0)
    # Reshape the array in group of values of t_step ms and infer the number
    # rows, then sum the absolute value of all rows. This is used to know
    # where a trade sign is cero.
    trade_sign_j_sec_nr = np.sum(np.reshape(np.absolute(trade_sign_j),
                                 (t_step, -1)), axis=0)

    # Calculating the midpoint log return and the cross response function

    for tau in range(1, tau_val):

        # Every second have a log-return
        log_return_i_sec = 0. * time_t_step

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau:]/midpoint_i_sec[:-tau]), np.zeros(tau))

        cross_response_tau[tau] = np.mean(
            log_return_i_sec[trade_sign_j_sec_nr != 0] *
            trade_sign_j_sec_avg[trade_sign_j_sec_nr != 0])

    # Saving data

    if (not os.path.isdir('../Data/cross_response_data_{}ms/'.format(t_step))):

        os.mkdir('../Data/cross_response_data_{}ms/'.format(t_step))
        print('Folder to save data created')

    pickle.dump(cross_response_tau, open(
        '../Data/cross_response_data_{}ms/cross_201603{}_{}i_{}j_{}ms.pickl'
        .format(t_step, day, ticker_i, ticker_j, t_step), 'wb'))

    print('Cross response function data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def avg_return_avg_trade_prod_data(ticker_i, ticker_j, day, tau_val, t_step):
    """
    Obtain the result of the product between the averaged midpoint log return
    of ticker i and the averaged trade signs of ticker j during different time
    lags. The data is adjusted to use only the values each t_step ms
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock
         to be analized (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param tau_val: maximum time lag to be analyzed
        :param t_step: time step in the data in ms
    """

    print('Product between the averaged midpoint log return of ticker i and '
          + 'the averaged trade signs of ticker j data')
    print('Processing data for the stock i ' + ticker_i + ' and stock j '
          + ticker_j + ' the day ' + day + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    midpoint_i = pickle.load(open(
        '../Data/midpoint_data/midpoint_201603{}_{}.pickl'
        .format(day, ticker_i), 'rb'))
    trade_sign_j = pickle.load(open(
        '../Data/trade_signs_data/trade_signs_most_201603{}_{}.pickl'
        .format(day, ticker_j), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with t_step ms accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    avg_return_sign = np.zeros(tau_val)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from 1 ms to t_step ms
    time_t_step = time[::t_step]

    # Reshape the array in group of values of t_step ms and infer the number
    # of rows, then sum all rows.
    trade_sign_j_sec_sum = np.sum(np.reshape(trade_sign_j, (t_step, -1)),
                                  axis=0)

    # Reasign the trade sign, if the value of the array is greater than 0
    # gives a 1 and -1 for the contrary.
    trade_sign_j_sec_avg = 1 * (trade_sign_j_sec_sum > 0) \
        - 1 * (trade_sign_j_sec_sum < 0)

    # Reshape the array in group of values of t_step ms and infer the number
    # rows, then sum the absolute value of all rows. This is used to know
    # where a trade sign is cero.
    trade_sign_j_sec_nr = np.sum(np.reshape(np.absolute(trade_sign_j),
                                 (t_step, -1)), axis=0)

    # Calculating the midpoint log return and the cross response functions

    for tau in range(1, tau_val):

        # Every second have a log-return
        log_return_i_sec = 0. * time_t_step

        # Obtain the midpoint log return. Displace the numerator tau values
        # to the right and compute the return, and append the remaining values
        # of tau with zeros
        log_return_i_sec = np.append(np.log(
                    midpoint_i_sec[tau:]/midpoint_i_sec[:-tau]), np.zeros(tau))

        avg_return_sign[tau] = (np.mean(
                                log_return_i_sec[trade_sign_j_sec_nr != 0]) *
                                np.mean(
                                trade_sign_j_sec_avg[trade_sign_j_sec_nr != 0]
                                ))

    # Saving data

    if (not os.path.isdir('../Data/avg_return_sign_data_{}ms/'
                          .format(t_step))):

        os.mkdir('../Data/avg_return_sign_data_{}ms/'.format(t_step))
        print('Folder to save data created')

    pickle.dump(avg_return_sign, open(
        '../Data/avg_return_sign_data_{}ms/avg_201603{}_{}i_{}j_{}ms.pickl'
        .format(t_step, day, ticker_i, ticker_j, t_step), 'wb'))

    print('Average product data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def zero_correlation_model_data(ticker_i, day, tau_val, t_step):
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

    print('Zero correlation model data')
    print('Processing data for the stock i ' + ticker_i + ' and a random'
          + ' trade sign array the day ' + day + ' March, 2016')
    print('Time step: ', t_step, 'ms')

    # Load data
    midpoint_i = pickle.load(open(
        '../Data/midpoint_data/midpoint_201603{}_{}.pickl'
        .format(day, ticker_i), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Setting variables to work with 1s accuracy

    # Array of the average of each tau. 10^3 s used by Wang
    cross_response_tau = np.zeros(tau_val)

    # Using values each second
    midpoint_i_sec = midpoint_i[::t_step]
    # Changing time from ms to s
    time_t_step = time[::t_step]

    # Calculating the midpoint log return and the cross response functions

    for tau in range(1, tau_val):

        # Every t_step have a log-return
        log_return_i_sec = 0. * time_t_step

        # Obtain the midpoint log return. Displace the numerator tau values to
        # the right and compute the return, and append the remaining values of
        # tau with zeros
        log_return_i_sec = np.append(np.log(
            midpoint_i_sec[tau:] / midpoint_i_sec[:-tau]), np.zeros(tau))

        trade_sign_rand = np.random.rand(len(time_t_step))
        trade_sign_rand_j = (1 * (trade_sign_rand > 0.5)
                             - 1 * (trade_sign_rand <= 0.5))

        cross_response_tau[tau] = np.mean(
            log_return_i_sec * trade_sign_rand_j)

    if (not os.path.isdir('../Data/zero_correlation_data_{}ms/'
                          .format(t_step))):

        os.mkdir('../Data/zero_correlation_data_{}ms/'.format(t_step))
        print('Folder to save data created')

    pickle.dump(cross_response_tau, open("".join(
        '../Data/zero_correlation_data_{}ms/zero_correlation_201603{}_{}i_\
        rand_{}ms.pickl'.split())
        .format(t_step, day, ticker_i, t_step), 'wb'))

    print('Zero correlation model data saved')
    print()

    return None
