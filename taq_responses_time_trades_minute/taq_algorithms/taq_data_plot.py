'''
TAQ data plot

Module to plot different TAQ data results based on the results of the functions
set in the module taq_data_analysis. The module plot the following data

- Self response data: it is possible to plot a day, or a group of days in a
  week and the average, a month and the average or the year and the average.

- Cross response data: it is possible to plot a day, or a group of days in a
  week and the average, a month and the average or the year and the average.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
from matplotlib import pyplot as plt
import os

import pickle

import taq_data_tools

__tau__ = 10000

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_time_trades_minute_plot(ticker, year,
                                                                  tau):
    """
    Plot the self response during a year and the dayly self-response
    contributions in a figure. The data is loaded from the self response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = \
         taq_self_response_year_responses_time_trades_minute_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        points = pickle.load(open(''.join((
                            '../../taq_data/responses_time_trades_minute_data'
                            + '_{1}/taq_self_response_year_responses_time'
                            + '_trades_minute_data_tau_{2}/taq_self_response'
                            + '_year_responses_time_trades_minute_data_tau'
                            + '_{2}_{1}_{0}.pickle').split())
                            .format(ticker, year, tau), 'rb'))

        plt.scatter(*zip(*points), label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response time {}'.format(ticker), fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right) \cdot'
                   + r'\varepsilon_j \left( t \right)$').split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name, tau),
                                     figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_trades_minute_plot(ticker, year,
                                                                  tau):
    """
    Plot the self response during a year and the dayly self-response
    contributions in a figure. The data is loaded from the self response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = \
         taq_self_response_year_avg_responses_time_trades_minute_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        x, y = pickle.load(open(''.join((
                            '../../taq_data/responses_time_trades_minute_data'
                            + '_{1}/taq_self_response_year_avg_responses_time'
                            + '_trades_minute_data_tau_{2}/taq_self_response'
                            + '_year_avg_responses_time_trades_minute_data_tau'
                            + '_{2}_{1}_{0}.pickle').split())
                            .format(ticker, year, tau), 'rb'))

        plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response time {}'.format(ticker), fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)\cdot'
                   + r'\varepsilon_{i}\left(t\right)\right\rangle _{t}$').split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name, tau),
                                     figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_trades_minute_plot_v2(ticker, year,
                                                                     tau):
    """
    Plot the self response during a year and the dayly self-response
    contributions in a figure. The data is loaded from the self response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = \
         taq_self_response_year_avg_responses_time_trades_minute_plot_v2.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        x, y = pickle.load(open(''.join((
                            '../../taq_data/responses_time_trades_minute_data'
                            + '_{1}/taq_self_response_year_avg_responses_time'
                            + '_trades_minute_data_v2_tau_{2}/taq_self_response'
                            + '_year_avg_responses_time_trades_minute_data_v2_tau'
                            + '_{2}_{1}_{0}.pickle').split())
                            .format(ticker, year, tau), 'rb'))

        plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response time {}'.format(ticker), fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)\cdot'
                   + r'\varepsilon_{i}\left(t\right)\right\rangle _{t}$').split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name, tau),
                                     figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_time_trades_minute_plot(ticker_i,
                                                                   ticker_j,
                                                                   year, tau):
    """
    Plot the average cross response during a month and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    if (ticker_i == ticker_j):

        return None

    else:

        try:

            function_name = \
              taq_cross_response_year_responses_time_trades_minute_plot. \
              __name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')
            figure = plt.figure(figsize=(16, 9))

            points = pickle.load(open(''.join((
                        '../../taq_data/responses_time_trades_minute_data_{2}'
                        + '/taq_cross_response_year_responses_time_trades'
                        + '_minute_data_tau_{3}/taq_cross_response_year'
                        + '_responses_time_trades_minute_data_tau_{3}_{2}'
                        + '_{0}i_{1}j.pickle').split())
                        .format(ticker_i, ticker_j, year, tau), 'rb'))

            plt.scatter(*zip(*points), label=r'$\tau = {}$'.format(tau))

            plt.legend(loc='best', fontsize=25)
            plt.title('Cross-response time {} - {}'.format(ticker_i,
                      ticker_j), fontsize=40)
            plt.xlabel(r'Trades per minute', fontsize=35)
            plt.ylabel(''.join((r'$r_{i} \left(t - 1, \tau \right)'
                       + r'\cdot \varepsilon_j \left( t \right)$').split()),
                       fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            # plt.xlim(1, 1000)
            # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
            # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name,
                                         tau), figure, ticker_i, ticker_j,
                                         year, '')

            return None

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_trades_minute_plot(ticker_i,
                                                                   ticker_j,
                                                                   year, tau):
    """
    Plot the self response during a year and the dayly self-response
    contributions in a figure. The data is loaded from the self response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = \
         taq_cross_response_year_avg_responses_time_trades_minute_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker_i,
                                                      ticker_j, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        x, y = pickle.load(open(''.join((
                            '../../taq_data/responses_time_trades_minute_data'
                            + '_{2}/taq_cross_response_year_avg_responses_time'
                            + '_trades_minute_data_tau_{3}/taq_cross_response'
                            + '_year_avg_responses_time_trades_minute_data_tau'
                            + '_{3}_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, tau), 'rb'))

        plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Cross-response time {} - {}'.format(ticker_i, ticker_j),
                  fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)\cdot'
                   + r'\varepsilon_{j}\left(t\right)\right\rangle _{t}$').split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name, tau),
                                     figure, ticker_i, ticker_j, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_trades_minute_plot_v2(ticker_i,
                                                                   ticker_j,
                                                                   year, tau):
    """
    Plot the self response during a year and the dayly self-response
    contributions in a figure. The data is loaded from the self response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = \
         taq_cross_response_year_avg_responses_time_trades_minute_plot_v2.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker_i,
                                                      ticker_j, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        x, y = pickle.load(open(''.join((
                            '../../taq_data/responses_time_trades_minute_data'
                            + '_{2}/taq_cross_response_year_avg_responses_time'
                            + '_trades_minute_data_v2_tau_{3}/taq_cross_response'
                            + '_year_avg_responses_time_trades_minute_data_v2_tau'
                            + '_{3}_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, tau), 'rb'))

        plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Cross-response time {} - {}'.format(ticker_i, ticker_j),
                  fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)\cdot'
                   + r'\varepsilon_{j}\left(t\right)\right\rangle _{t}$').split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot('{}_tau_{}'.format(function_name, tau),
                                     figure, ticker_i, ticker_j, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def main():

    ticker = 'AAPL'
    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    year = '2008'
    tau = 50

    taq_self_response_year_responses_time_trades_minute_plot(ticker, year, tau)
    taq_cross_response_year_responses_time_trades_minute_plot(ticker_i,
                                                              ticker_j,
                                                              year, tau)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
