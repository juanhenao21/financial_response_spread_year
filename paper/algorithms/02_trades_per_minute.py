'''Trades per minute figures

Plot the self- and cross responses for the stocks AAPL, CVX, GS, JPM, MSFT,
and XOM, analyzing the frequency of trades.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------

def taq_self_response_year_plot(tickers, year):
    """Plot the self-response for a year
    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e. '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # TO DO:
    try:
        figure = plt.figure(figsize=(16, 9))

        for ticker in tickers:

            # Load data
            self_resp = pickle.load(open(
                ''.join(('../../project/taq_data/article_reproduction_data_{1}/taq_self'
                         + '_response_year_data/taq_self_response_year_data'
                         + '_{1}_{0}.pickle').split())
                         .format(ticker, year), 'rb'))

            plt.semilogx(self_resp, linewidth=5, label='{}'.format(ticker))

        plt.legend(loc='best', fontsize=25)
        # plt.title('Self-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=35)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Save Plot
        figure.savefig('../plot/01_self_responses_{}'.format(year))

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

