'''Trades per minute figures

Plot the averaged and non-averaged self- and cross responses for the stocks
AAPL, CVX, GS, JPM, MSFT, and XOM, analyzing the frequency of trades.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------


def taq_responses_year_trades_minute_plot(ticker_i, ticker_j, year, tau):
    """Plots the non-averaged responses for a year

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e. '2008')
    :param tau: integer great than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)

        # Load data
        points_event_self = pickle.load(open(''.join((
                            '../../project/taq_data/responses_event_trades'
                            + '_minute_data_{1}/taq_self_response_year'
                            + '_responses_event_trades_minute_data_tau_{2}/taq'
                            + '_self_response_year_responses_event_trades'
                            + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
                            .format(ticker_i, year, tau), 'rb'))

        ax1.scatter(*zip(*points_event_self), label=r'$\tau = {}$'.format(tau))

        points_time_self = pickle.load(open(''.join((
                            '../../project/taq_data/responses_time_trades'
                            + '_minute_data_{1}/taq_self_response_year'
                            + '_responses_time_trades_minute_data_tau_{2}/taq'
                            + '_self_response_year_responses_time_trades'
                            + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
                            .format(ticker_i, year, tau), 'rb'))

        ax2.scatter(*zip(*points_time_self), label=r'$\tau = {}$'.format(tau))

        points_event_cross = pickle.load(open(''.join((
                    '../../project/taq_data/responses_event_trades_minute_data'
                    + '_{2}/taq_cross_response_year_responses_event_trades'
                    + '_minute_data_tau_{3}/taq_cross_response_year'
                    + '_responses_event_trades_minute_data_tau_{3}_{2}'
                    + '_{0}i_{1}j.pickle').split())
                    .format(ticker_i, ticker_j, year, tau), 'rb'))

        ax3.scatter(*zip(*points_event_cross), label=r'$\tau = {}$'
                    .format(tau))

        points_time_cross = pickle.load(open(''.join((
                    '../../project/taq_data/responses_time_trades_minute_data'
                    + '_{2}/taq_cross_response_year_responses_time_trades'
                    + '_minute_data_tau_{3}/taq_cross_response_year'
                    + '_responses_time_trades_minute_data_tau_{3}_{2}'
                    + '_{0}i_{1}j.pickle').split())
                    .format(ticker_i, ticker_j, year, tau), 'rb'))

        ax4.scatter(*zip(*points_time_cross), label=r'$\tau = {}$'.format(tau))

        ax1.legend(loc='best', fontsize=25)
        # ax1.title('Self-response event {}'.format(ticker), fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=35)
        ax1.set_ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right) \cdot'
                       + r'\varepsilon_j \left( t \right)$').split()),
                       fontsize=35)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.grid(True)

        ax2.legend(loc='best', fontsize=25)
        # ax2.title('Self-response time {}'.format(ticker), fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=35)
        ax2.set_ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right) \cdot'
                       + r'\varepsilon_j \left( t \right)$').split()),
                       fontsize=35)
        # ax2.xlim(1, 1000)
        # ax2.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        # ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.grid(True)

        ax3.legend(loc='best', fontsize=25)
        # ax3.title('Cross-response event {} - {}'.format(ticker_i,
        #           ticker_j), fontsize=40)
        ax3.set_xlabel(r'Trades per minute', fontsize=35)
        ax3.set_ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right)'
                       + r'\cdot \varepsilon_j \left( t \right)$').split()),
                       fontsize=35)
        # ax3.xlim(1, 1000)
        # ax3.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        # ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.grid(True)

        ax4.legend(loc='best', fontsize=25)
        # ax4.title('Cross-response time {} - {}'.format(ticker_i,
        #           ticker_j), fontsize=40)
        ax4.set_xlabel(r'Trades per minute', fontsize=35)
        ax4.set_ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right)'
                       + r'\cdot \varepsilon_j \left( t \right)$').split()),
                       fontsize=35)
        # ax4.xlim(1, 1000)
        # ax4.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        # ax4.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax4.grid(True)

        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/02_response_trades_minute')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


    """Plots the self-response average for a year.
def taq_responses_year_avg_trades_minute_plot(ticker_i, ticker_j, year, tau):

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e. '2008')
    :param tau: integer great than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)

        # Load data
        x_event_self, y_event_self = pickle.load(open(''.join((
            '../../project/taq_data/responses_event_trades_minute_data_{1}'
            + '/taq_self_response_year_avg_responses_event'
            + '_trades_minute_data_tau_{2}/taq_self'
            + '_response_year_avg_responses_event_trades'
            + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
            .format(ticker_i, year, tau), 'rb'))

        ax1.semilogx(x_event_self, y_event_self, linewidth=5,
                     label=r'$\tau = {}$'.format(tau))

        x_time_self, y_time_self = pickle.load(open(''.join((
            '../../project/taq_data/responses_time_trades_minute_data'
            + '_{1}/taq_self_response_year_avg_responses_time'
            + '_trades_minute_data_tau_{2}/taq_self'
            + '_response_year_avg_responses_time_trades_minute'
            + '_data_tau_{2}_{1}_{0}.pickle').split())
            .format(ticker_i, year, tau), 'rb'))

        ax2.semilogx(x_time_self, y_time_self, linewidth=5,
                     label=r'$\tau = {}$'.format(tau))

        x_event_cross, y_event_cross = pickle.load(open(''.join((
            '../../project/taq_data/responses_event_trades_minute'
            + '_data_{2}/taq_cross_response_year_avg'
            + '_responses_event_trades_minute_data_tau_{3}'
            + '/taq_cross_response_year_avg_responses'
            + '_event_trades_minute_data_tau_{3}_{2}_{0}i'
            + '_{1}j.pickle').split())
            .format(ticker_i, ticker_j, year, tau), 'rb'))

        ax3.semilogx(x_event_cross, y_event_cross, linewidth=5,
                     label=r'$\tau = {}$'.format(tau))

        x_time_cross, y_time_cross = pickle.load(open(''.join((
            '../../project/taq_data/responses_time_trades_minute'
            + '_data_{2}/taq_cross_response_year_avg'
            + '_responses_time_trades_minute_data_tau_{3}'
            + '/taq_cross_response_year_avg_responses_time'
            + '_trades_minute_data_tau_{3}_{2}_{0}i_{1}j'
            + '.pickle').split())
            .format(ticker_i, ticker_j, year, tau), 'rb'))

        ax4.semilogx(x_time_cross, y_time_cross, linewidth=5,
                     label=r'$\tau = {}$'.format(tau))

        ax1.legend(loc='best', fontsize=25)
        # ax1.title('Self-response event {}'.format(ticker), fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=35)
        ax1.set_ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)'
                       + r'\cdot\varepsilon_{i}\left(t\right)\right\rangle')
                       + '_{t}$'.split()), fontsize=35)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.grid(True)

        ax2.legend(loc='best', fontsize=25)
        # ax2.title('Self-response time {}'.format(ticker), fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=35)
        ax2.set_ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)'
                       + r'\cdot\varepsilon_{i}\left(t\right)\right\rangle')
                       + '_{t}$'.split()), fontsize=35)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.grid(True)

        ax3.legend(loc='best', fontsize=25)
        # ax3.title('Cross-response event {} - {}'.format(ticker_i,
        #           ticker_j), fontsize=40)
        ax3.set_xlabel(r'Trades per minute', fontsize=35)
        ax3.set_ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)'
                       + r'\cdot\varepsilon_{j}\left(t\right)\right\rangle'
                       + r'_{t}$') .split()), fontsize=35)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.grid(True)

        ax4.legend(loc='best', fontsize=25)
        # ax4.title('Cross-response time {} - {}'.format(ticker_i, ticker_j),
        #           fontsize=40)
        ax4.set_xlabel(r'Trades per minute', fontsize=35)
        ax4.set_ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)'
                       + r'\cdot\varepsilon_{j}\left(t\right)\right\rangle'
                       + r'_{t}$').split()), fontsize=35)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax4.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax4.grid(True)

        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/02_avg_response_trades_minute')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def main():

    year = '2008'
    tau = 1000

    # taq_responses_year_trades_minute_plot('AAPL', 'MSFT', year, tau)
    taq_responses_year_avg_trades_minute_plot('AAPL', 'MSFT', year, tau)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
