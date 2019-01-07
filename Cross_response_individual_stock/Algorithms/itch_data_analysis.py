'''
ITCH data analysis

Script to analyze the ITCH data with the information of 96 stocks during a
week in 2016.

The 96 stocks are shown in the list used in main and the week values used are
from the week of the 7 - 11 March, 2016.

For the first proyect I need to obtain the cross response functions between
individual stocks. To compute these values I need to calculate the midpoint
price, the midpoint log returns and the trade signs. Each task is specified
in each function.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''
# -----------------------------------------------------------------------------------------------------------------------
# Modules

from itertools import product

import multiprocessing as mp
import pickle

import itch_data_generator
import itch_data_plot

# -----------------------------------------------------------------------------------------------------------------------


def data_plot_generator():
    """
    Generates all the data and plots from ITCH data
    """

    # Basic data
    #tickers = pickle.load(open('../Data/tickers.pickl', 'rb'))
    tickers = ['AAPL', 'MSFT']
    days = pickle.load(open('../Data/days.pickl', 'rb'))
    tau_val = [1000000, 100000, 10000, 1000]
    t_step = [1, 10, 100, 1000]

    # Parallel computing
    pool = mp.Pool(processes=8)
    # Basic functions
    #pool.starmap(itch_data_generator.midpoint_data, product(tickers, days))
    #pool.starmap(itch_data_generator.trade_signs_data, product(tickers, days))
    # Especific functions
    #pool.starmap(itch_data_generator.self_response_data, product(tickers, days, [1000], [1000]))
    #pool.starmap(itch_data_generator.self_response_abs_data, product(tickers, days, [1000], [1000]))
    #pool.starmap(itch_data_generator.zero_correlation_model_data, product(tickers, days, [1000], [1000]))
    pool.starmap(itch_data_generator.cross_response_data, product(tickers, tickers, days, [1000], [1000]))
    pool.starmap(itch_data_generator.avg_return_avg_trade_prod_data, product(tickers, tickers, days, [1000], [1000]))
    pool.starmap(itch_data_generator.difference_cross_response_avg_prod_data, product(tickers, tickers, days, [1000]))
    pool.starmap(itch_data_generator.trade_sign_self_correlator_data, product(tickers, days, [1000], [1000]))
    pool.starmap(itch_data_generator.trade_sign_autocorrelation_data, product(tickers, days, [1000], [1000]))
    pool.starmap(itch_data_generator.trade_sign_cross_correlator_data, product(tickers, tickers, days, [1000], [1000]))

    # Plot
    pool.starmap(itch_data_plot.midpoint_plot_week, product(tickers, [days], [1000]))
    pool.starmap(itch_data_plot.self_response_self_abs_zero_corr_plot, product(tickers, [days], [1000]))
    pool.starmap(itch_data_plot.cross_response_avg_return_avg_trade_plot, product(tickers, tickers, [days], [1000]))
    pool.starmap(itch_data_plot.difference_cross_response_avg_prod_plot, product(tickers, tickers, [days], [1000]))
    pool.starmap(itch_data_plot.trade_sign_self_correlator_autocorrelation_plot, product(tickers, [days], [1000]))
    pool.starmap(itch_data_plot.trade_sign_cross_correlator_plot, product(tickers, tickers, [days], [1000]))

    pool.close()
    pool.join()

    return None


# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    tickers = pickle.load(open('../Data/tickers.pickl', 'rb'))
    days = pickle.load(open('../Data/days.pickl', 'rb'))

    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    ticker = ['AAPL', 'MSFT']
    tau_val = [1000000, 100000, 10000, 1000]
    t_step = [1, 10, 100, 1000]

    #for day in days:

    #    itch_data_generator.trade_sign_cross_correlator_data(ticker_i, ticker_j, day, 1000, 1000)

    #itch_data_plot.trade_sign_self_correlator_autocorrelation_plot(ticker_i, days, 1000)

    data_plot_generator()

    print('Ay vamos!!')

    return None

if __name__ == '__main__':
    main()
