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

import itch_data_generator
import itch_data_plot

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Tickers and days to analyze
    # tickers = ["AAL", "AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN", "AMAT", "AMGN",
    #            "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB", "BMRN", "CA",  "CELG", "CERN",
    #            "CHKP", "CHRW", "CHTR", "CMCSA", "COST", "CSCO", "CTSH", "CTXS", "DISCA", "DISH",
    #            "DLTR", "EA",  "EBAY", "EQIX", "ESRX", "EXPD", "FAST", "FB",  "FISV", "FOXA",
    #            "GILD", "GOOG", "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "JD",  "KHC",
    #            "KLAC", "LBTYA", "LLTC", "LMCA", "LRCX", "LVNTA", "MAR", "MAT", "MDLZ", "MNST",
    #            "MSFT", "MU",  "MYL", "NFLX", "NTAP", "NVDA", "NXPI", "ORLY", "PAYX", "PCAR",
    #            "PCLN", "QCOM", "REGN", "ROST", "SBAC", "SBUX", "SIRI", "SNDK", "SPLS", "SRCL",
    #            "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP", "VOD", "VRSK",
    #            "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO"]

    days = ['07', '08', '09', '10', '11']

    ticker = 'AAPL'

    day = '07'


    itch_data_plot.self_response_self_abs_zero_corr_plot('AAPL', days, 1000)

    print('Ay vamos!!')

    return None


if __name__ == '__main__':
    main()
