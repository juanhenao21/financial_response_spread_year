'''
TAQ data plot

Module to plot different TAQ data results based on the results of the functions
set in the module taq_data_analysis. The module plot the following data

- Self response data: it is possible to plot a day, or a group of days in a
  week and the average, a month and the average or the year and the average.

- Cross response data: it is possible to plot a day, or a group of days in a
  week and the average, a month and the average or the year and the average.

- Trade sign self correlator: plot the trade sign self correlator for
  every day for one stock in independent plots in one figure.

- Trade sign cross correlator: plot the trade sign cross correlator for
  every day for two stocks in independent pltos in one figure.

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

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_plot(ticker, year):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = taq_self_response_year_avg_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        self_ = pickle.load(open(''.join((
                        '../../taq_data/article_reproduction_data_{1}/taq_self'
                        + '_response_year_data/taq_self_response_year_data'
                        + '_{1}_{0}.pickle').split())
                        .format(ticker, year), 'rb'))

        figure = plt.figure(figsize=(16, 9))
        plt.semilogx(self_, linewidth=5, label='{}'.format(ticker))
        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=35)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker,
                                     year, '')

        return None

    except FileNotFoundError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_plot(ticker_i, ticker_j, year):
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

            function_name = taq_cross_response_year_avg_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')
            cross = pickle.load(open(''.join((
                            '../../taq_data/article_reproduction_data_{2}/taq'
                            + '_cross_response_year_data/taq_cross_response'
                            + '_year_data_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year), 'rb'))

            figure = plt.figure(figsize=(16, 9))
            plt.semilogx(cross, linewidth=5, label='{} - {}'.format(ticker_i,
                                                                    ticker_j))
            plt.legend(loc='best', fontsize=25)
            plt.title('Cross-response', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=35)
            plt.ylabel(r'$R_{ij}(\tau)$', fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            plt.xlim(1, 1000)
            # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                         ticker_j, year, '')

            return None

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_year_avg_plot(ticker, year):
    """
    Plot the average trade sign self correlator during a year and the dayly
    self response contributions in a figure. The data is loaded from the trade
    sign self correlator data results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = taq_trade_sign_self_correlator_year_avg_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        t_self = pickle.load(open(''.join((
                        '../../taq_data/article_reproduction_data_{1}/taq'
                        + '_trade_sign_self_correlator_year_data/taq_trade'
                        + '_sign_self_correlator_year_data_{1}_{0}.pickle')
                        .split()).format(ticker, year), 'rb'))

        figure = plt.figure(figsize=(16, 9))
        plt.loglog(t_self, linewidth=5, label='{}'.format(ticker))
        plt.legend(loc='best', fontsize=25)
        plt.title('Trade sign self-correlator', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=35)
        plt.ylabel(r'$\Theta_{ii}(\tau)$', fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.xlim(1, 1000)
        plt.ylim(10 ** -6, 1)
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker,
                                     year, '')

        return None

    except FileNotFoundError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_year_avg_plot(ticker_i, ticker_j, year):
    """
    Plot the average trade sign cross correlator during a year and the dayly
    self response contributions in a figure. The data is loaded from the trade
    sign cross correlator data results.
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

            function_name = taq_trade_sign_cross_correlator_year_avg_plot. \
                             __name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')

            t_cross = pickle.load(open(''.join((
                        '../../taq_data/article_reproduction_data_{2}/taq'
                        + '_trade_sign_cross_correlator_year_data/taq_trade'
                        + '_sign_cross_correlator_year_data_{2}_{0}i_{1}j'
                        + '.pickle')
                        .split()).format(ticker_i, ticker_j, year), 'rb'))

            figure = plt.figure(figsize=(16, 9))
            plt.loglog(t_cross, linewidth=5, label='{} - {}'
                       .format(ticker_i, ticker_j))
            plt.legend(loc='best', fontsize=25)
            plt.title('Trade sign cross-correlation', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=35)
            plt.ylabel(r'$\Theta_{ij}(\tau)$', fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            plt.xlim(1, 1000)
            plt.ylim(10 ** -6, 1)
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                         ticker_j, year, '')

            return None

        except FileNotFoundError:
            print('No data')
            print()
            return None

# ----------------------------------------------------------------------------


def main():
    pass

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()