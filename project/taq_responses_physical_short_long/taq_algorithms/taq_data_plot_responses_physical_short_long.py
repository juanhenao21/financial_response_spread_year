'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_responses_time_short_long module.

This script requires the following modules:
    * matplotlib
    * numpy
    * taq_data_tools_responses_time_short_long

The module contains the following functions:
    * taq_self_response_year_avg_responses_time_short_long_plot - plots
      the self-response average for a year.
    * taq_cross_response_year_avg_responses_time_short_long_plot - plots
      the cross-response average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

import taq_data_tools_responses_time_short_long

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_short_long_plot(ticker, year,
                                                              tau, tau_p):
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
            taq_self_response_year_avg_responses_time_short_long_plot. \
            __name__
        taq_data_tools_responses_time_short_long \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        # Load data
        (self_short,
         self_long,
         self_response,
         self_shuffle) = pickle.load(open(''.join((
                                     '../../taq_data/responses_time_short'
                                     + '_long_data_{1}/taq_self_response_year'
                                     + '_time_short_long_tau_data_tau_{2}_tau'
                                     + '_p_{3}/taq_self_response_year_time'
                                     + '_short_long_tau_data_tau_{2}_tau_p_{3}'
                                     + '_{1}_{0}.pickle').split())
                                     .format(ticker, year, tau, tau_p), 'rb'))

        # Addition of the short and long response signal
        sum = np.zeros(tau)
        sum[:tau_p + 1] = self_short[:tau_p + 1]
        sum[tau_p + 1:] = self_short[tau_p + 1:] + self_long[tau_p + 1:]

        figure = plt.figure(figsize=(16, 9))
        plt.semilogx(self_short, linewidth=5, label='{} - Short'
                     .format(ticker))
        plt.semilogx(self_long, linewidth=5, label='{} - Long'.format(ticker))
        plt.semilogx(sum, linewidth=5, label='{} - Sum'.format(ticker))
        plt.semilogx(self_response, linewidth=5, label='{} - Self-response'
                     .format(ticker))
        plt.semilogx(self_shuffle, linewidth=5, label='{} - Shuffle'
                     .format(ticker))
        plt.plot((tau_p, tau_p), (0, max(self_short)), '--',
                 label=r"$\tau' $ = {}".format(tau_p))
        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=35)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.xlim(1, 1000)
        # plt.ylim(1.35 * 10 ** -4, 1.53 * 10 ** -4)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools_responses_time_short_long \
            .taq_save_plot('{}_tau_{}_tau_p_{}'
                           .format(function_name, tau, tau_p),
                           figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_short_long_plot(ticker_i,
                                                               ticker_j, year,
                                                               tau, tau_p):
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

        # Self-response
        return None

    else:
        try:
            function_name = \
                taq_cross_response_year_avg_responses_time_short_long_plot. \
                __name__
            taq_data_tools_responses_time_short_long \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            # Load data
            (cross_short,
             cross_long,
             cross_response,
             cross_shuffle) = pickle.load(open(''.join((
                                          '../../taq_data/responses_time'
                                          + '_short_long_data_{2}/taq_cross'
                                          + '_response_year_time_short_long'
                                          + '_tau_data_tau_{3}_tau_p_{4}/taq'
                                          + '_cross_response_year_time_short'
                                          + '_long_tau_data_tau_{3}_tau_p_{4}'
                                          + '_{2}_{0}i_{1}j.pickle').split())
                                          .format(ticker_i, ticker_j, year,
                                                  tau, tau_p), 'rb'))

            # Addition of the short and long response signal
            sum = np.zeros(tau)
            sum[:tau_p + 1] = cross_short[:tau_p + 1]
            sum[tau_p + 1:] = cross_short[tau_p + 1:] + cross_long[tau_p + 1:]

            figure = plt.figure(figsize=(16, 9))
            plt.semilogx(cross_short, linewidth=5, label='{} - {} - Short'
                         .format(ticker_i, ticker_j))
            plt.semilogx(cross_long, linewidth=5, label='{} - {} - Long'
                         .format(ticker_i, ticker_j))
            plt.semilogx(sum, linewidth=5, label='{} - {} - Sum'
                         .format(ticker_i, ticker_j))
            plt.semilogx(cross_response, linewidth=5,
                         label='{} - {} - Cross-response'.format(ticker_i,
                                                                 ticker_j))
            plt.semilogx(cross_shuffle, linewidth=5, label='{} - {} - Shuffle'
                         .format(ticker_i, ticker_j))
            plt.plot((tau_p, tau_p), (0, max(cross_short)), '--',
                     label=r"$\tau' $ = {}".format(tau_p))
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
            taq_data_tools_responses_time_short_long \
                .taq_save_plot('{}_tau_{}_tau_p_{}'
                               .format(function_name, tau, tau_p),
                               figure, ticker_i, ticker_j, year, '')

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
