'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_responses_event_trades_minute module.

This script requires the following modules:
    * matplotlib
    * numpy
    * taq_data_tools_event_shift

The module contains the following functions:
    * taq_self_response_year_responses_event_trades_minute_plot - plots the
      self- response for a year.
    * taq_self_response_year_avg_responses_event_trades_minute_plot - plots
      the self- response average for a year.
    * taq_cross_response_year_responses_event_trades_minute_plot - plots the
      cross- response for a year.
    * taq_cross_response_year_avg_responses_event_trades_minute_plot - plots
      the cross- response average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

import taq_data_tools_responses_event_trades_minute

__tau__ = 10000

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_event_trades_minute_plot(ticker, year,
                                                              tau):
    """Plots the self-response for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param tau: integer greater than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:

        function_name = \
            taq_self_response_year_responses_event_trades_minute_plot.__name__
        taq_data_tools_responses_event_trades_minute \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        figure = plt.figure(figsize=(16, 9))

        # Load data
        points = pickle.load(open(''.join((
                            '../../taq_data/responses_event_trades_minute_data'
                            + '_{1}/taq_self_response_year_responses_event'
                            + '_trades_minute_data_tau_{2}/taq_self_response'
                            + '_year_responses_event_trades_minute_data_tau'
                            + '_{2}_{1}_{0}.pickle').split())
                            .format(ticker, year, tau), 'rb'))

        plt.scatter(*zip(*points), label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response event {}'.format(ticker), fontsize=40)
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
        taq_data_tools_responses_event_trades_minute \
            .taq_save_plot('{}_tau_{}'.format(function_name, tau), figure,
                           ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_event_trades_minute_plot(ticker, year,
                                                                  tau):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param tau: integer greater than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = \
         taq_self_response_year_avg_responses_event_trades_minute_plot.__name__
        taq_data_tools_responses_event_trades_minute \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        figure = plt.figure(figsize=(16, 9))

        x, y = pickle.load(open(''.join((
                            '../../taq_data/responses_event_trades_minute_data'
                            + '_{1}/taq_self_response_year_avg_responses_event'
                            + '_trades_minute_data_tau_{2}/taq_self'
                            + '_response_year_avg_responses_event_trades'
                            + '_minute_data_tau_{2}_{1}_{0}.pickle').split())
                            .format(ticker, year, tau), 'rb'))

        plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response event {}'.format(ticker), fontsize=40)
        plt.xlabel(r'Trades per minute', fontsize=35)
        plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)\cdot'
                   + r'\varepsilon_{i}\left(t\right)\right\rangle _{t}$')
                   .split()), fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        # plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools_responses_event_trades_minute \
            .taq_save_plot('{}_tau_{}'.format(function_name, tau), figure,
                           ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_event_trades_minute_plot(ticker_i,
                                                               ticker_j, year,
                                                               tau):
    """Plots the cross-response for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :param tau: integer greater than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Cross-response
        return None

    else:
        try:
            function_name = \
              taq_cross_response_year_responses_event_trades_minute_plot. \
              __name__
            taq_data_tools_responses_event_trades_minute \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            figure = plt.figure(figsize=(16, 9))

            # Load data
            points = pickle.load(open(''.join((
                        '../../taq_data/responses_event_trades_minute_data_{2}'
                        + '/taq_cross_response_year_responses_event_trades'
                        + '_minute_data_tau_{3}/taq_cross_response_year'
                        + '_responses_event_trades_minute_data_tau_{3}_{2}'
                        + '_{0}i_{1}j.pickle').split())
                        .format(ticker_i, ticker_j, year, tau), 'rb'))

            plt.scatter(*zip(*points), label=r'$\tau = {}$'.format(tau))

            plt.legend(loc='best', fontsize=25)
            plt.title('Cross-response event {} - {}'.format(ticker_i,
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
            taq_data_tools_responses_event_trades_minute \
                .taq_save_plot('{}_tau_{}'.format(function_name, tau), figure,
                               ticker_i, ticker_j, year, '')

            return None

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_event_trades_minute_plot(ticker_i,
                                                                   ticker_j,
                                                                   year, tau):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :param tau: integer greater than zero (i.e. 50).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Cross-response
        return None

    else:
        try:
            function_name = \
                taq_cross_response_year_avg_responses_event_trades_minute_plot\
                .__name__
            taq_data_tools_responses_event_trades_minute \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            figure = plt.figure(figsize=(16, 9))

            # Load data
            x, y = pickle.load(open(''.join((
                                '../../taq_data/responses_event_trades_minute'
                                + '_data_{2}/taq_cross_response_year_avg'
                                + '_responses_event_trades_minute_data_tau_{3}'
                                + '/taq_cross_response_year_avg_responses'
                                + '_event_trades_minute_data_tau_{3}_{2}_{0}i'
                                + '_{1}j.pickle').split())
                                .format(ticker_i, ticker_j, year, tau), 'rb'))

            plt.semilogx(x, y, linewidth=5, label=r'$\tau = {}$'.format(tau))

            plt.legend(loc='best', fontsize=25)
            plt.title('Cross-response event {} - {}'.format(ticker_i,
                      ticker_j), fontsize=40)
            plt.xlabel(r'Trades per minute', fontsize=35)
            plt.ylabel(''.join((r'$\left\langle r_{i}\left(t-1,\tau\right)'
                       + r'\cdot\varepsilon_{j}\left(t\right)\right\rangle'
                       + r'_{t}$') .split()), fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            # plt.xlim(1, 1000)
            # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            taq_data_tools_responses_event_trades_minute \
                .taq_save_plot('{}_tau_{}'.format(function_name, tau), figure,
                               ticker_i, ticker_j, year, '')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    pass

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
