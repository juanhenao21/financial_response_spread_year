'''
Script to analyze the ITCH data with the information of 96 stocks during a week in 2016.

The 96 stocks are shown in the list used in main and the week values used are from the 
week of the 7 - 11 March, 2016.

For the first proyect I need to obtain the cross response functions between individual
stocks. To compute these values I need to calculate the midpoint price, the midpoint 
log returns and the trade signs. Each task is specified in each function.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''
# -----------------------------------------------------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import gzip
import pickle
import multiprocessing as mp
from itertools import product

# -----------------------------------------------------------------------------------------------------------------------

def midpoint_data(ticker, day):
    '''
    Obtain the midpoint price from the ITCH 2016 data. For further calculations we use the full time range from the 
    opening of the market at 9h30 to the closing at 16h in milliseconds and then convert the values to hours (23.4
    million data). To fill the time spaces when nothing happens we replicate the last value calculated until a change
    in the price happens. Save in a different pickle file the array of each of the following values: best bid, best 
    ask, spread, midpoint price and time.
    
    ticker -- String of the abbreviation of the stock to be analized (i.e. 'AAPL')
    day -- String of the day to be analized (i.e '07')
    
    return None
    '''

    print('Midpoint price data')
    print('Processing data for the stock', ticker, 'the day', day + ' March, 2016')

    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_2016/201603%s_%s.csv.gz' % (day,ticker)), 
                         dtype='str', skip_header = 1, delimiter = ',')
    
    # Lists of times, ids, types, volumes and prices
    # List of all the available information available in the data excluding the last two columns

    times_ = np.array([int(mytime) for mytime in data[:,0]])
    ids_ = np.array([int(myid) for myid in data[:,2]])             # List of order types: 
    types_ = np.array([1 * (mytype == 'B') +                       # "B" = 1 -> Add buy order
                    2 * (mytype == 'S') +                          # "S" = 2 -> Add sell order
                    3 * (mytype == 'E') +                          # "E" = 3 -> Execute outstanding order in part
                    4 * (mytype == 'C') +                          # "C" = 4 -> Cancel outstanding order in part
                    5 * (mytype == 'F') +                          # "F" = 5 -> Execute outstanding order in full
                    6 * (mytype == 'D') +                          # "D" = 6 -> Delete outstanding order in full
                    7 * (mytype == 'X') +                          # "X" = 7 -> Bulk volume for the cross event
                    8 * (mytype == 'T') for mytype in data[:,3]])  # "T" = 8 -> Execute non-displayed order
    volumes_ = np.array([int(myvolume) for myvolume in data[:,4]])
    prices_ = np.array([int(myprice) for myprice in data[:,5]])

    ids = ids_[types_<7]
    times = times_[types_<7]
    types = types_[types_<7]
    prices = prices_[types_<7]

    # Reference lists
    # Reference lists using the original values or the length of the original lists 

    prices_ref = 1 * prices
    types_ref = 0 * types
    times_ref = 0 * times
    volumes_ref = 0 * types
    index_ref= 0 * types
    newids = {}
    insertnr = {}
    hv = 0

    # Help lists with the data of the buy orders and sell orders

    hv_prices = prices[types < 3]
    hv_types = types[types < 3]
    hv_times = times[types < 3]

    # Fill the reference lists where the values of 'T' are 'E','C','F','D'

    for iii in range(len(ids)):                             # For the data in the length of the ids list (all data)

        if (types[iii] < 3):                                # If the data is a sell or buy order

            newids[ids[iii]] = hv                           # Insert in the dictionary newids a key with the valor of the id
                                                            # and the value of hv (a counter)
            insertnr[ids[iii]] = iii                        # Insert in the dictionary insertnr a key with the valor of the id
                                                            # and the value of the for counter
            hv += 1                                         # Increase the value of hv

        else:                                               # If the data is not a sell or buy order

            prices_ref[iii] = hv_prices[newids[ids[iii]]]   # Fill the values of prices_ref with no prices ('E','C','F','D') 
                                                            # with the price of the order
            types_ref[iii] = hv_types[newids[ids[iii]]]     # Fill the values of types_ref with no  prices ('E','C','F','D') 
                                                            # with the type of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]     # Fill the values of time_ref with no  prices ('E','C','F','D') 
                                                            # with the time of the order
            index_ref[iii] = insertnr[ids[iii]]             # Fill the values of index_ref with no  prices ('E','C','F','D') 
                                                            # with the position of the sell or buy order

    # Minimum and maximum trade price

    minP = round(0.9 * (1. * prices_ref[types == 5] / 10000).min(),2) # The minimum price allowed is 0.9 times the price of
                                                                      # the minimum value of all full executed orders.
    maxP = round(1.1 * (1. * prices_ref[types == 5] / 10000).max(),2) # The maximum price allowed is 1.1 times the price of
                                                                      # the maximum value of all full executed orders.
    valuesP = minP + 0.01 * np.arange(int((maxP - minP) / 0.01))         # Values between maxP and minP with step of 0.01 cents
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

    for iii in range(len(ids)):                                    # For the data in the length of the ids list (all data)

        # Incoming limit orders

        myPriceIndex = int(round(1. * (1.* prices_ref[iii] / 10000 - minP) / 0.01))

        bestAskOld = 1 * bestAsk                                   # Initializing bestAksOld and bestBidOld
        bestBidOld = 1 * bestBid

        if (myPriceIndex >= 0 and                                  # The price is greater than the minP
            myPriceIndex < len(valuesP)):

            if (types[iii] == 2):                                  # If the order is a sell

                if (nAsk[myPriceIndex] == 0):

                    bestAsk = min(bestAsk,valuesP[myPriceIndex])   # The bestAsk is the minimum value between the previous
                                                                   # bestAsk and the value in valuesP with id myPriceIndex

                nAsk[myPriceIndex] += 1                            # Increase the value of nAsk to 1 (value arrived the book)

            if (types[iii] == 1):                                  # If the order is a buy

                if (nBid[myPriceIndex] == 0):

                    bestBid = max(bestBid,valuesP[myPriceIndex])   # The bestBid is the maximum value between the previous
                                                                   # bestBid and the value in valuesP with id myPriceIndex

                nBid[myPriceIndex] += 1                            # Increase the value of nBid to 1 (value arrived the book)

            # limit orders completely leaving

            if (types[iii] == 5 or                                 # If the order is a full executed order or
                types[iii] == 6):                                  # If the order is a full delete order

                if (types_ref[iii] == 2):                          # If the order is a sell

                    nAsk[myPriceIndex] -= 1                        # Reduce the value in nAsk to 0 (value left the book)

                    if (nAsk[myPriceIndex] == 0 and                # If the value is not in the book
                        valuesP[myPriceIndex] == bestAsk):         # If the value is the best ask

                        bestAsk = valuesP[nAsk > 0].min()          # The best ask is the minimum value of the prices that are
                                                                   # currently in the order book

                else:

                    nBid[myPriceIndex] -= 1                        # Reduce the value in nBid to 0 (value left the book)

                    if (nBid[myPriceIndex] == 0 and                # If the value is not in the book
                        valuesP[myPriceIndex] == bestBid):         # If the value is the best bid

                        bestBid = valuesP[nBid > 0].max()          # The best bid is the maximum value of the prices that are
                                                                   # currently in the order book

        if (bestAsk != bestAskOld or                               # If the bestAsk changes or
            bestBid != bestBidOld):                                # If the bestBid changes

            bestTimes.append(times[iii])                           # Append the values of bestTimes, bestAsks and bestBids
            bestAsks.append(bestAsk)                               
            bestBids.append(bestBid)
            bestAskOld = bestAsk
            bestBidOld = bestBid

    # Calculating the spread, midpoint and time

    spread_ = np.array(bestAsks) - np.array(bestBids)              # Calculating the spread
    timesS = np.array(bestTimes)                                   # Transforming bestTimes in an array
    midpoint_ = 1. * (np.array(bestAsks) + np.array(bestBids)) / 2

    # Setting the values in the open market time
    
    day_times_ind = (1. * timesS / 3600 / 1000 > 9.5) * (1. * timesS / 3600 / 1000 < 16) > 0 # This line behaves as an or.
                                                                   # The two arrays must achieve a condition, in this case, be
                                                                   # in the market trade hours
    midpoint = 1. * midpoint_[day_times_ind]                       # Midpoint in the market trade hours
    times_spread = 1. * timesS[day_times_ind]                      # Time converted to hours in the market trade hours
    bestAsks = np.array(bestAsks)[day_times_ind]
    bestBids = np.array(bestBids)[day_times_ind]
    spread = spread_[day_times_ind]                                # Spread in the market trade hours
    
    # Completing the full time entrances

    full_time = np.array(range(34200000,57600000))                  # 34 200 000 ms = 9h30 - 57 600 000 ms = 16h
    
    # As there can be several values for the same millisecond, we use the first value of each millisecond in the full time
    # array as is the easier way to obtain the value and it behaves quiet equal as the original input

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

            while (count < len(times_spread) and times_spread[count - 1] == times_spread[count]):
                
                count += 1
                    
        else:
            
            midpoint_first_val[t_idx] = midpoint_first_val[t_idx - 1]
            bestAsks_first_val[t_idx] = bestAsks_first_val[t_idx - 1]
            bestBids_first_val[t_idx] = bestBids_first_val[t_idx - 1]
            spread_first_val[t_idx] = spread_first_val[t_idx - 1]

    # Saving data
    
    pickle.dump(bestAsks_first_val, open('../Data/midpoint_data/bestAsks_201603%s_%s.pickl' % (day,ticker), 'wb'))
    pickle.dump(bestBids_first_val, open('../Data/midpoint_data/bestBids_201603%s_%s.pickl' % (day,ticker), 'wb'))
    pickle.dump(spread_first_val, open('../Data/midpoint_data/spread_201603%s_%s.pickl' % (day,ticker), 'wb'))
    pickle.dump(full_time, open('../Data/midpoint_data/time_201603%s_%s.pickl' % (day,ticker), 'wb'))
    pickle.dump(midpoint_first_val, open('../Data/midpoint_data/midpoint_201603%s_%s.pickl' % (day,ticker), 'wb'))
    
    print('Midpoint price data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------

def midpoint_log_returns_data(ticker, day):

    # TO DO

    return None

# -----------------------------------------------------------------------------------------------------------------------

def midpoint_plot(ticker, day):
    '''
    Plot the midpoint behavior using the price vs time. The data is loaded from the mipoint data results.
    
    ticker -- String of the abbreviation of the stock to be analized (i.e. 'AAPL')
    day -- String of the day to be analized (i.e '07')
    
    return None
    '''
    # Load data

    print('Processing data for the stock', ticker, 'the day', day + ' March, 2016')

    midpoint = pickle.load(open('../Data/midpoint_data/midpoint_201603%s_%s.pickl' % (day,ticker), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time_201603%s_%s.pickl' % (day,ticker), 'rb'))
    
    # Plotting
    
    plt.title('%s' %ticker, fontsize=40)
    plt.plot(time, midpoint, label=('Day %s' %day))
    plt.xlabel(r'Time $[hour]$', fontsize=25)
    plt.ylabel(r'Price $ [\$] $', fontsize=25)
    plt.legend(loc=0,fontsize=20)
        
    return None

# -----------------------------------------------------------------------------------------------------------------------

def midpoint_plot_week(ticker, days):
    '''
    Plot the midpoint behavior using the price vs time during a time period. The data is loaded from the mipoint data
    results.
    
    ticker -- String of the abbreviation of the stock to be analized (i.e. 'AAPL')
    days -- List of the days that will be plotted (i.e ['07', '08', '09'])
    
    return None
    '''
        
    plt.figure(figsize=(16,9))
    
    days=['07','08','09','10','11']
    
    for day in days:
        midpoint_plot(ticker, day)
    
    plt.tight_layout()
    plt.savefig('../Data/midpoint_plot/midpoint_plot_%s.png' %ticker)
    
    return None

# -----------------------------------------------------------------------------------------------------------------------

def trade_signs_data(ticker, day):
    '''
    Obtain the trade signs from the ITCH 2016 data. For further calculations we use the whole time range from the 
    opening of the market at 9h30 to the closing at 16h in milliseconds and then convert the values to hours (23.4
    million data). To fill the time spaces when nothing happens we just fill with
    zeros indicating that there were neither a buy nor a sell. Save in a pickle file the array of the trade signs
    
    ticker -- String of the abbreviation of the stock to be analized (i.e. 'AAPL')
    day -- String of the day to be analized (i.e '07')
    
    return None
    '''
        
    print('Trade signs data')
    print('Processing data for the stock', ticker, 'the day', day + ' March, 2016')
    
    # Load data

    data = np.genfromtxt(gzip.open('../../ITCH_2016/201603%s_%s.csv.gz' % (day,ticker)), 
                         dtype='str', skip_header = 1, delimiter = ',')

    
    # Lists of times, ids, types, volumes and prices
    # List of all the available information available in the data excluding the last two columns

    times_ = np.array([int(mytime) for mytime in data[:,0]])
    ids_ = np.array([int(myid) for myid in data[:,2]])             # List of order types: 
    types_ = np.array([1 * (mytype == 'B') +                       # "B" = 1 -> Add buy order
                    2 * (mytype == 'S') +                          # "S" = 2 -> Add sell order
                    3 * (mytype == 'E') +                          # "E" = 3 -> Execute outstanding order in part
                    4 * (mytype == 'C') +                          # "C" = 4 -> Cancel outstanding order in part
                    5 * (mytype == 'F') +                          # "F" = 5 -> Execute outstanding order in full
                    6 * (mytype == 'D') +                          # "D" = 6 -> Delete outstanding order in full
                    7 * (mytype == 'X') +                          # "X" = 7 -> Bulk volume for the cross event
                    8 * (mytype == 'T') for mytype in data[:,3]])  # "T" = 8 -> Execute non-displayed order
    volumes_ = np.array([int(myvolume) for myvolume in data[:,4]])
    prices_ = np.array([int(myprice) for myprice in data[:,5]])

    ids = ids_[types_<7]
    times = times_[types_<7]
    types = types_[types_<7]

    # Reference lists
    # Reference lists using the original values or the length of the original lists 

    types_ref = 0 * types
    times_ref = 0 * times
    index_ref= 0 * types
    newids = {}
    insertnr = {}
    hv = 0

    # Help lists with the data of the buy orders and sell orders

    hv_types = types[types < 3]
    hv_times = times[types < 3]

    trade_sign = 0 * types

    # Fill the reference lists where the values of 'T' are 'E','C','F','D'

    for iii in range(len(ids)):                             # For the data in the length of the ids list (all data)

        if (types[iii] < 3):                                # If the data is a sell or buy order

            newids[ids[iii]] = hv                           # Insert in the dictionary newids a key with the valor of the id
                                                            # and the value of hv (a counter) that is the index in hv_types
            hv += 1                                         # Increase the value of hv

            trade_sign[iii] = 0

        elif (types[iii] == 3 or
                types[iii] == 5):                                            # If the data is not a sell or buy order

            types_ref[iii] = hv_types[newids[ids[iii]]]     # Fill the values of types_ref with no  prices ('E','C','F','D') 
                                                            # with the type of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]     # Fill the values of time_ref with no  prices ('E','C','F','D') 
                                                            # with the time of the order

            if (hv_types[newids[ids[iii]]] == 2):

                trade_sign[iii] = -1

            elif (hv_types[newids[ids[iii]]] == 1):

                trade_sign[iii] = 1

        else:

            types_ref[iii] = hv_types[newids[ids[iii]]]     # Fill the values of types_ref with no  prices ('E','C','F','D') 
                                                            # with the type of the order
            times_ref[iii] = hv_times[newids[ids[iii]]]     # Fill the values of time_ref with no  prices ('E','C','F','D') 
                                                            # with the time of the order

            trade_sign[iii] = 0

    # Ordering the data in the open market time 

    day_times_ind = (1. * times / 3600 / 1000 > 9.5) * (1. * times / 3600 / 1000 < 16) > 0 # This line behaves as an or.
                                                               # The two arrays must achieve a condition, in this case, be
                                                               # in the market trade hours
    trade_signs = trade_sign[day_times_ind]
    times_signs = times[day_times_ind]

    # Completing the full time entrances

    full_time = np.array(range(34200000,57600000))                  # 34 200 000 ms = 9h30 - 57 600 000 ms = 16h
    
    # As there can be several values for the same millisecond, we use the most used trade value of each millisecond in the full time
    # array as it behaves quiet similar as the original input

    count = 0
    trade_signs_complete_most = 0. * full_time

    for t_idx, t_val in enumerate(full_time):
        
        most = 0
        
        if (count < len(times_signs) and t_val == times_signs[count]):
            
            most += trade_signs[count]
            
            count += 1
            
            while (count < len(times_signs) and times_signs[count - 1] == times_signs[count]):
                
                most += trade_signs[count]
                count += 1
                
            if (most > 0):
                
                trade_signs_complete_most[t_idx] = 1
                
            elif (most < 0):
                
                trade_signs_complete_most[t_idx] = -1

    # Saving data
    
    pickle.dump(full_time, open('../Data/trade_signs_data/times_trade_signs_201603%s_%s.pickl' % (day,ticker), 'wb'))
    pickle.dump(trade_signs_complete_most, open('../Data/trade_signs_data/trade_signs_most_201603%s_%s.pickl' % (day,ticker), 'wb'))
    
    print('Trade signs data saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------

def cross_response_functions(ticker, day):

    # TO DO

    return None

# -----------------------------------------------------------------------------------------------------------------------

def main():

    # Tickers and days to analyze
    tickers = ["AAL", "AAPL","ADBE","ADI", "ADP", "ADSK","AKAM","ALXN","AMAT","AMGN",
               "AMZN","ATVI","AVGO","BBBY","BIDU","BIIB","BMRN","CA",  "CELG","CERN",
               "CHKP","CHRW","CHTR","CMCSA","COST","CSCO","CTSH","CTXS","DISCA","DISH",
               "DLTR","EA",  "EBAY","EQIX","ESRX","EXPD","FAST","FB",  "FISV","FOXA",
               "GILD","GOOG","GRMN","HSIC","ILMN","INTC","INTU","ISRG","JD",  "KHC",
               "KLAC","LBTYA","LLTC","LMCA","LRCX","LVNTA","MAR","MAT","MDLZ","MNST",
               "MSFT","MU",  "MYL", "NFLX","NTAP","NVDA","NXPI","ORLY","PAYX","PCAR",
               "PCLN","QCOM","REGN","ROST","SBAC","SBUX","SIRI","SNDK","SPLS","SRCL",
               "STX", "SYMC","TRIP","TSCO","TSLA","TXN", "VIAB","VIP", "VOD", "VRSK",
               "VRTX","WDC", "WFM", "WYNN","XLNX","YHOO"]

    days = ['07','08','09','10','11']

    #midpoint_data('GOOG', '07')
    #trade_signs_data('AAPL', '09')
    midpoint_plot_week('AAPL')

    print('Ay vamos!!')
    return None

if __name__ == '__main__':
    main()
    


