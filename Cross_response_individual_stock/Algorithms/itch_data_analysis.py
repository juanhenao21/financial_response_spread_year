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
# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze

    tickers = pickle.load(open('../Data/tickers.pickl', 'rb'))
    days = pickle.load(open('../Data/days.pickl', 'rb'))

    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    tau_val = 1000
    ticker = ['AAPL', 'MSFT']

    for t in [1, 10, 100, 1000]:
        for day in days:
            itch_data_generator.trade_sign_self_correlator_data(ticker_i, day, tau_val, t)
        itch_data_plot.trade_sign_self_correlator_plot(ticker_i, days, t)

    print('Ay vamos!!')

    return None

if __name__ == '__main__':
    main()
