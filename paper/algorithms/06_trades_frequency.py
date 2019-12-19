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


def taq_responses_year_trade_scale_minute_plot(ticker_i, ticker_j, year, tau):
    """Plots the non-averaged responses for a year in trade time scale.

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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Load data
        points_event_self = pickle.load(open(''.join((
                            f'../../project/taq_data/responses_event_trades'
                            + f'_minute_data_{year}/taq_self_response_year'
                            + f'_responses_event_trades_minute_data_tau_{tau}/'
                            + f'taq_self_response_year_responses_event_trades'
                            + f'_minute_data_tau_{tau}_{year}_{ticker_i}'
                            + f'.pickle').split()), 'rb'))

        ax1.scatter(*zip(*points_event_self), label=r'$\tau = {}s$'
                    .format(tau))

        points_event_cross = pickle.load(open(''.join((
                    f'../../project/taq_data/responses_event_trades_minute'
                    + f'_data_{year}/taq_cross_response_year_responses_event'
                    + f'_trades_minute_data_tau_{tau}/taq_cross_response_year'
                    + f'_responses_event_trades_minute_data_tau_{tau}_{year}'
                    + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        ax2.scatter(*zip(*points_event_cross), label=r'$\tau = {}s$'
                    .format(tau))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title(f'{ticker_i}', fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=20)
        ax1.set_ylabel(''.join((r'$r^{seconds}_{i} \left(t - 1, \tau \right) '
                       + r'\cdot \varepsilon_i^{trades} \left( t \right)$')
                       .split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title(f'{ticker_i} - {ticker_j}', fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=20)
        ax2.set_ylabel(''.join((r'$r^{seconds}_{i} \left(t - 1, \tau \right) '
                       + r'\cdot\varepsilon_j^{trades} \left( t \right)$')
                       .split()), fontsize=20)
        # ax2.xlim(1, 1000)
        # ax2.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/06_response_trade_time_scale_minute.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def taq_responses_year_second_scale_minute_plot(ticker_i, ticker_j, year, tau):
    """Plots the non-averaged responses for a year in second time scale.

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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Load data
        points_time_self = pickle.load(open(''.join((
                            f'../../project/taq_data/responses_time_trades'
                            + f'_minute_data_{year}/taq_self_response_year'
                            + f'_responses_time_trades_minute_data_tau_{tau}/'
                            + f'taq_self_response_year_responses_time_trades'
                            + f'_minute_data_tau_{tau}_{year}_{ticker_i}'
                            + f'.pickle').split()), 'rb'))

        ax1.scatter(*zip(*points_time_self), label=r'$\tau = {}s$'
                    .format(tau))

        points_time_cross = pickle.load(open(''.join((
                    f'../../project/taq_data/responses_time_trades_minute_data'
                    + f'_{year}/taq_cross_response_year_responses_time_trades'
                    + f'_minute_data_tau_{tau}/taq_cross_response_year'
                    + f'_responses_time_trades_minute_data_tau_{tau}_{year}'
                    + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        ax2.scatter(*zip(*points_time_cross), label=r'$\tau = {}s$'
                    .format(tau))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title(f'{ticker_i}', fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=20)
        ax1.set_ylabel(''.join((r'$r^{seconds}_{i} \left(t - 1, \tau \right) '
                       + r'\cdot\varepsilon_i^{seconds} \left( t \right)$')
                       .split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title(f'{ticker_i} - {ticker_j}', fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=20)
        ax2.set_ylabel(''.join((r'$r^{seconds}_{i} \left(t - 1, \tau \right) '
                       + r'\cdot\varepsilon_j^{seconds} \left( t \right)$')
                       .split()), fontsize=20)
        # ax2.xlim(1, 1000)
        # ax2.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/06_response_second_time_scale_minute.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def taq_responses_year_avg_trade_scale_minute_plot(ticker_i, ticker_j, year,
                                                   tau):
    """Plots the averaged responses for a year in trade time scale.

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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Load data
        x_event_self, y_event_self = pickle.load(open(''.join((
            f'../../project/taq_data/responses_event_trades_minute_data_{year}'
            + f'/taq_self_response_year_avg_responses_event_trades_minute_data'
            + f'_tau_{tau}/taq_self_response_year_avg_responses_event_trades'
            + f'_minute_data_tau_{tau}_{year}_{ticker_i}.pickle').split()),
            'rb'))

        ax1.semilogx(x_event_self, y_event_self, linewidth=5,
                     label=r'$\tau = {}s$'.format(tau))

        x_event_cross, y_event_cross = pickle.load(open(''.join((
            f'../../project/taq_data/responses_event_trades_minute_data_{year}'
            + f'/taq_cross_response_year_avg_responses_event_trades_minute'
            + f'_data_tau_{tau}/taq_cross_response_year_avg_responses_event'
            + f'_trades_minute_data_tau_{tau}_{year}_{ticker_i}i_{ticker_j}j'
            + f'.pickle').split()), 'rb'))

        ax2.semilogx(x_event_cross, y_event_cross, linewidth=5,
                     label=r'$\tau = {}s$'.format(tau))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title(f'{ticker_i}', fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=20)
        ax1.set_ylabel(''.join((r'$\left\langle r^{seconds}_{i}\left(t-1,\tau'
                       + r'\right)\cdot\varepsilon_{i}^{trades}\left(t\right)'
                       + r'\right\rangle_{trades}$').split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title(f'{ticker_i} - {ticker_j}', fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=20)
        ax2.set_ylabel(''.join((r'$\left\langle r^{seconds}_{i}\left(t-1,\tau'
                       + r'\right)\cdot\varepsilon_{j}^{trades}\left(t\right)'
                       + r'\right\rangle_{trades}$') .split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/06_avg_response_trade_time_scale_minute.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_responses_year_avg_second_scale_minute_plot(ticker_i, ticker_j, year,
                                                    tau):
    """Plots the averaged responses for a year in second time scale.

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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Load data
        x_time_self, y_time_self = pickle.load(open(''.join((
            f'../../project/taq_data/responses_time_trades_minute_data_{year}'
            + f'/taq_self_response_year_avg_responses_time_trades_minute'
            + f'_data_tau_{tau}/taq_self_response_year_avg_responses_time'
            + f'_trades_minute_data_tau_{tau}_{year}_{ticker_i}.pickle')
            .split()), 'rb'))

        ax1.semilogx(x_time_self, y_time_self, linewidth=5,
                     label=r'$\tau = {}s$'.format(tau))

        x_time_cross, y_time_cross = pickle.load(open(''.join((
            f'../../project/taq_data/responses_time_trades_minute_data_{year}'
            + f'/taq_cross_response_year_avg_responses_time_trades_minute'
            + f'_data_tau_{tau}/taq_cross_response_year_avg_responses_time'
            + f'_trades_minute_data_tau_{tau}_{year}_{ticker_i}i_{ticker_j}j'
            + f'.pickle').split()), 'rb'))

        ax2.semilogx(x_time_cross, y_time_cross, linewidth=5,
                     label=r'$\tau = {}s$'.format(tau))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title(f'{ticker_i}', fontsize=40)
        ax1.set_xlabel(r'Trades per minute', fontsize=20)
        ax1.set_ylabel(''.join((r'$\left\langle r^{seconds}_{i}\left(t-1,\tau'
                       + r'\right)\cdot\varepsilon_{i}^{seconds}\left(t\right)'
                       + r'\right\rangle_{seconds}$').split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title(f'{ticker_i} - {ticker_j}', fontsize=40)
        ax2.set_xlabel(r'Trades per minute', fontsize=20)
        ax2.set_ylabel(''.join((r'$\left\langle r^{seconds}_{i}\left(t-1,\tau'
                       + r'\right)\cdot\varepsilon_{j}^{seconds}\left(t\right)'
                       + r'\right\rangle_{seconds}$') .split()), fontsize=20)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/06_avg_response_second_time_scale_minute.png')

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

    taq_responses_year_trade_scale_minute_plot('CVX', 'XOM', year, tau)
    taq_responses_year_second_scale_minute_plot('CVX', 'XOM', year, tau)
    taq_responses_year_avg_trade_scale_minute_plot('CVX', 'XOM', year, tau)
    taq_responses_year_avg_second_scale_minute_plot('CVX', 'XOM', year, tau)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
