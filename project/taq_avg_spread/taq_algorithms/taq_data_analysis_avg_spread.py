'''TAQ data analysis module.

The functions in the module analyze the statistics from the NASDAQ stock
market and compute the average spread of the stocks.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * numpy
    * pandas
    * pickle
    * taq_data_tools_avg_spread

The module contains the following functions:
    * taq_quotes_trades_day_avg_spread_data - statistics of quotes and trades
      for a day.
    * taq_quotes_trades_year_avg_spread_data - statistics of quotes and trades
      for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import numpy as np
import pandas as pd

import taq_data_tools_avg_spread

# ----------------------------------------------------------------------------


def taq_quotes_trades_day_avg_spread_data(ticker, date):
    """Obtain the quotes and trades statistics for a day.

    Using the quotes files, obtain the statistics of the average spread, number
    of quotes and number of trades for a day.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with float values.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:
        # Load data
        data_quotes = pd.read_hdf(f'../../taq_data/hdf5_daily_data_{year}/taq'
                              + f'_{ticker}_quotes_{date}.h5', key='/quotes',
                              columns=['Bid', 'Ask'])
        data_trades = pd.read_hdf(f'../../taq_data/hdf5_daily_data_{year}/taq'
                              + f'_{ticker}_trades_{date}.h5', key='/trades',
                              columns=['Ask'])

        # Some files are corrupted, so there are some zero values that does not
        # have sense
        condition_quotes = data_quotes['Ask'] != 0
        data_quotes = data_quotes[condition_quotes]
        condition_trades = data_trades['Ask'] != 0
        data_trades = data_trades[condition_trades]

        spread = (data_quotes['Ask'] - data_quotes['Bid']) / 10000

        num_quotes = len(data_quotes)
        num_trades = len(data_trades)
        avg_spread = np.mean(spread)

        return (num_quotes, num_trades, avg_spread)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return (np.NaN, np.NaN, np.NaN)

# ----------------------------------------------------------------------------


def taq_quotes_trades_year_avg_spread_data(tickers, year):
    """Obtain the quotes and trades statistics for a year.

    Using the taq_quotes_trades_day_avg_spread_data function computes the
    statistics of the average spread, number of quotes and number of trades
    for a year.

    :param tickers: list of the string abbreviation of the stocks to be
     analyzed (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    function_name = taq_quotes_trades_year_avg_spread_data.__name__

    # Pandas DataFrame to store the data
    spread_stats = pd.DataFrame(
        columns=['Ticker', 'Avg_Quotes', 'Avg_Trades', 'Avg_Spread'])

    dates = taq_data_tools_avg_spread.taq_bussiness_days(year)

    for idx, ticker in enumerate(tickers):

        taq_data_tools_avg_spread \
            .taq_function_header_print_data(function_name, ticker, ticker,
                                             year, '', '')

        stat = []
        args_prod = iprod([ticker], dates)

        # Parallel computation of the statistics. Every result is appended to
        # a list
        with mp.Pool(processes=mp.cpu_count()) as pool:
            stat.append(pool.starmap(taq_quotes_trades_day_avg_spread_data,
                        args_prod))

        # To obtain the average of the year, I average all the results of the
        # corresponding values (number quotes, trades and avg spread)
        stat_year = np.nanmean(stat[0], axis=0)

        spread_stats.loc[idx] = [ticker] + list(stat_year)

    spread_stats.sort_values(by='Avg_Spread', inplace=True)
    spread_stats.to_csv(f'../taq_avg_spread_{year}.csv')
    print(spread_stats)

    return None

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
