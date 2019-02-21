'''
ITCH data generator

Module to compute the following data

- Midpoint price data: using the TAQ data obtain the best bid, best ask,
  quotes and midpoint price data.

- Trade signs data: using the TAQ data obtain the trade signs data.

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

import taq_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------------------------------------------------


def taq_midpoint_data(ticker, year, month, day):
    """
    Obtain the midpoint price from the TAQ data. For further calculations
    we use the full time range from 9h40 to 15h50 in seconds (22200 seconds).
    To fill the time spaces when nothing happens we replicate
    the last value calculated until a change in the price happens. Save in a
    different pickle file the array of each of the following values: best bid,
    best ask, spread, midpoint price and time.
        :param ticker: string of the abbreviation of the stock to be analized
                       (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_midpoint_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    time_q, bid_q, ask_q = pickle.load(open(
        '../../TAQ_2008/TAQ_py/TAQ_{}_quotes_{}{}{}.pickl'
        .format(ticker, year, month, day), 'rb'))

    midpoint = (bid_q + ask_q) / 2
    spread = ask_q - bid_q

    # 34800 s = 9h40 - 57000 s = 15h50
    full_time = np.array(range(34800, 57000))

    # As there can be several values for the same second, we use the
    # last value of each second in the full time array as it behaves
    # quiet equal as the original input

    midpoint_last_val = 0. * full_time
    midpoint_last_val[-1] = midpoint[0]

    ask_last_val = 0. * full_time
    ask_last_val[-1] = ask_q[0]

    bid_last_val = 0. * full_time
    bid_last_val[-1] = bid_q[0]

    spread_last_val = 0. * full_time
    spread_last_val[-1] = spread[0]

    count = 0

    for t_idx, t_val in enumerate(full_time):

        if (count < len(time_q) and t_val == time_q[count]):

            count += 1

            while (count < len(time_q) and
                   time_q[count - 1] == time_q[count]):

                count += 1

            midpoint_last_val[t_idx] = midpoint[count - 1]
            ask_last_val[t_idx] = ask_q[count - 1]
            bid_last_val[t_idx] = bid_q[count - 1]
            spread_last_val[t_idx] = spread[count - 1]

        else:

            midpoint_last_val[t_idx] = midpoint_last_val[t_idx - 1]
            ask_last_val[t_idx] = ask_last_val[t_idx - 1]
            bid_last_val[t_idx] = bid_last_val[t_idx - 1]
            spread_last_val[t_idx] = spread_last_val[t_idx - 1]

    # Saving data

    if (not os.path.isdir('../taq_data_{1}/{0}/'.format(function_name, year))):

        os.mkdir('../taq_data_{1}/{0}/'.format(function_name, year))
        print('Folder to save data created')

    pickle.dump(ask_last_val,
                open('../taq_data_{2}/{0}/{0}_ask_{2}{3}{4}_{1}.pickl'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(bid_last_val,
                open('../taq_data_{2}/{0}/{0}_bid_{2}{3}{4}_{1}.pickl'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(spread_last_val,
                open('../taq_data_{2}/{0}/{0}_spread_{2}{3}{4}_{1}.pickl'
                     .format(function_name, ticker, year, month, day), 'wb'))
    pickle.dump(full_time, open('../taq_data_{2}/{0}/{0}_time.pickl'
                                .format(function_name, year), 'wb'))
    pickle.dump(midpoint_last_val,
                open('../taq_data_{2}/{0}/{0}_midpoint_{2}{3}{4}_{1}.pickl'
                     .format(function_name, ticker, year, month, day), 'wb'))

    print('Data saved')
    print()

    return None



