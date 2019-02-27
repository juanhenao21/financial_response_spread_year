'''
TAQ data main

Script to analyze the TAQ data with the information of 6 stocks during a 2008.

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

import taq_data_analysis
import taq_data_plot
import taq_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year, months, days):
    """
    docstring here
        :param ticker: list of the strings of the abbreviations of the stock
                       to be analized (i.e. ['AAPL', 'MSFT'])
        :param year: string of the year to be analized (i.e '2008')
        :param months: list of the strings of the months to be analized
                       (i.e ['07', '08', '09'])
        :param day: list of lists of the strings of the days to be analized
                    in each month (i.e [['07', '08', '09'], ['01', '02']])
    """

    # Basic folders
    taq_data_tools.taq_start_folders(year)

    # Parallel computing
    pool = mp.Pool(processes=mp.cpu_count())

    # Basic functions
    for month in months:

        # Especific functions
        pool.starmap(taq_data_analysis.taq_midpoint_data,
                    product(tickers, [year], [month], days[int(month) - 1]))
        pool.starmap(taq_data_analysis.taq_trade_signs_data,
                    product(tickers, [year], [month], days[int(month) - 1]))
        pool.starmap(taq_data_analysis.taq_cross_response_data,
                     product(tickers, tickers, [year], [month],
                             days[int(month) - 1]))

        # Plot
        pool.starmap(taq_data_plot.taq_cross_response_month_avg_plot,
                     product(tickers, tickers, [year], [month], [days[int(month) - 1]]))

    pool.starmap(taq_data_plot.taq_cross_response_year_avg_plot,
                     product(tickers, tickers, [year], [months], [days]))

    pool.close()
    pool.join()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    tickers = ['AAPL', 'MSFT']

    months_list = []
    days_list = []

    for i in range(1,13):
        if (i < 10):
            months_list.append('0' + str(i))
        else:
            months_list.append(str(i))

    for month in months_list:

        m = pickle.load(open('../../Basic/days_{}.pickle'.format(month), 'rb'))
        days_list += [m]

    taq_data_plot_generator(tickers, '2008', months_list, days_list)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
