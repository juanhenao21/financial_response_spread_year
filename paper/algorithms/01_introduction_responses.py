'''Self- and cross responses figures

Plot the self- and cross responses for the stocks AAPL, CVX, GS, JPM, MSFT,
and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_plot(tickers, year):
    """Plots the self-response average for a year.

    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e. '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax = figure.add_subplot(111)

        for ticker in tickers:

            # Load data
            self_resp = pickle.load(open(
                ''.join(('../../project/taq_data/article_reproduction_data_{1}'
                         + '/taq_self_response_year_data/taq_self_response'
                         + '_year_data_{1}_{0}.pickle').split())
                .format(ticker, year), 'rb'))

            plt.semilogx(self_resp, linewidth=5, label='{}'.format(ticker))

        plt.legend(loc='best', fontsize=30)
        # plt.title('Self-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=40)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=40)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(30)
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

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_plot(sectors):
    """Plots the cross-response average for a year.

    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax = figure.add_subplot(111)

        for sector in sectors:

            # Load data
            cross_resp = pickle.load(open(
                ''.join(('../../project/taq_data/article_reproduction_data'
                         + '_{2}/taq_cross_response_year_data/taq_cross'
                         + '_response_year_data_{2}_{0}i_{1}j.pickle').split())
                .format(sector[0], sector[1], sector[2]), 'rb'))

            plt.semilogx(cross_resp, linewidth=5, label='{} - {}'
                         .format(sector[0], sector[1]))

        plt.legend(loc='best', fontsize=30)
        # plt.title('Cross-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=40)
        plt.ylabel(r'$R_{ij}(\tau)$', fontsize=40)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.xlim(1, 1000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(30)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/01_cross_responses_{}'.format(sector[2]))

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def main():

    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    sectors = [['AAPL', 'MSFT', '2008'], ['MSFT', 'AAPL', '2008'],
               ['XOM', 'CVX', '2008'], ['CVX', 'XOM', '2008'],
               ['GS', 'JPM', '2008'], ['JPM', 'GS', '2008']]
    year = '2008'

    taq_self_response_year_avg_plot(tickers, year)
    taq_cross_response_year_avg_plot(sectors)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
