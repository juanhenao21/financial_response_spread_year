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

import itch_data_analysis
import itch_data_plot
import itch_data_tools

# -----------------------------------------------------------------------------------------------------------------------


def itch_data_plot_generator(tickers, year, month, days):
    """
    Generates all the data and relevant plots from ITCH data. It uses
    the multiprocessing module to parallelize functions.
    """

    # Basic data
    tau_val = [1000, 10000, 100000, 1000000]
    t_step = [1000, 100, 10, 1]

    # Basic folders
    itch_data_tools.itch_start_folders(year)

    # Parallel computing
    pool = mp.Pool(processes=mp.cpu_count())

    # Basic functions
    pool.starmap(itch_data_generator.itch_midpoint_data,
                 product(tickers, [year], [month], days, [1]))
    pool.starmap(itch_data_generator.itch_trade_signs_data,
                 product(tickers, [year], [month], days, [1]))

    for tau, t in zip(tau_val, t_step):

        # Especific functions
        pool.starmap(itch_data_generator.itch_self_response_data,
                     product(tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_self_response_abs_data,
                     product(tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_zero_correlation_model_data,
                     product(tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_cross_response_data,
                     product(tickers, tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_avg_return_avg_trade_prod_data,
                     product(tickers, tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.
                     itch_difference_cross_response_avg_prod_data,
                     product(tickers, tickers, [year], [month], days, [t]))
        pool.starmap(itch_data_generator.itch_trade_sign_self_correlator_data,
                     product(tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_trade_sign_autocorrelation_data,
                     product(tickers, [year], [month], days, [tau], [t]))
        pool.starmap(itch_data_generator.itch_trade_sign_cross_correlator_data,
                     product(tickers, tickers, [year], [month], days, [tau], [t]))

        # Plot
        pool.starmap(itch_data_plot.itch_midpoint_week_plot,
                     product(tickers, [year], [month], [days], [t]))
        pool.starmap(itch_data_plot.itch_self_response_self_abs_zero_corr_plot,
                     product(tickers, [year], [month], [days], [t]))
        pool.starmap(itch_data_plot.
                     itch_cross_response_avg_return_avg_trade_plot,
                     product(tickers, tickers, [year], [month], [days], [t]))
        pool.starmap(itch_data_plot.
                     itch_difference_cross_response_avg_prod_plot,
                     product(tickers, tickers, [year], [month], [days], [t]))
        pool.starmap(itch_data_plot.
                     itch_trade_sign_self_correlator_autocorrelation_plot,
                     product(tickers, [year], [month], [days], [t]))
        pool.starmap(itch_data_plot.itch_trade_sign_cross_correlator_plot,
                     product(tickers, tickers, [year], [month], [days], [t]))

    pool.close()
    pool.join()

    return None


# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    # ticker_i = 'AAPL'
    # ticker_j = 'MSFT'
    # tau_val = [1000000, 100000, 10000, 1000]
    # t_step = [1, 10, 100, 1000]

    tickers = ['AAPL', 'MSFT']
    days = ['07', '08', '09', '10', '11']
    itch_data_plot_generator(tickers, '2016', '03', days)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
