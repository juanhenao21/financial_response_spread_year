'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_article_reproduction module.

This script requires the following modules:
    * matplotlib
    * numpy
    * taq_data_tools_article_reproduction

The module contains the following functions:
    * taq_self_response_year_avg_plot - plots the self-response average for a
      year.
    * taq_cross_response_year_avg_plot - plots the cross-response average for a
      year.
    * taq_trade_sign_self_correlator_year_avg_plot - plots the trade sign self-
      correlator average for a year.
    * taq_trade_sign_cross_correlator_year_avg_plot - plots the trade sign
      cross-correlator average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

import taq_data_tools_article_reproduction

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_plot(ticker, year):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = taq_self_response_year_avg_plot.__name__
        taq_data_tools_article_reproduction \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        # Load data
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
        taq_data_tools_article_reproduction \
            .taq_save_plot(function_name, figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_plot(ticker_i, ticker_j, year):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = taq_cross_response_year_avg_plot.__name__
            taq_data_tools_article_reproduction \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

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
            taq_data_tools_article_reproduction \
                .taq_save_plot(function_name, figure, ticker_i, ticker_j,
                               year, '')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_year_avg_plot(ticker, year):
    """Plots the trade sign self-correlator average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = taq_trade_sign_self_correlator_year_avg_plot.__name__
        taq_data_tools_article_reproduction \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

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
        taq_data_tools_article_reproduction \
            .taq_save_plot(function_name, figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_year_avg_plot(ticker_i, ticker_j, year):
    """Plots the trade sign cross-correlator average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = taq_trade_sign_cross_correlator_year_avg_plot. \
                             __name__
            taq_data_tools_article_reproduction \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

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
            taq_data_tools_article_reproduction \
                .taq_save_plot(function_name, figure, ticker_i, ticker_j, year,
                               '')

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
