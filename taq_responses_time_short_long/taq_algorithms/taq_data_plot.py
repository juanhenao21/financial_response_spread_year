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


def taq_self_response_year_avg_time_short_long_plot(ticker, year, tau, tau_p):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = taq_self_response_year_avg_time_short_long_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        self_short, self_long, self_response, self_shuffle = pickle.load(open(''.join((
                        '../../taq_data/responses_time_short_long_data_{1}/taq_self'
                        + '_response_year_time_short_long_tau_data_tau_{2}_tau_p_{3}/taq_self_response_year_time_short_long_tau_data_tau_{2}_tau_p_{3}'
                        + '_{1}_{0}.pickle').split())
                        .format(ticker, year, tau, tau_p), 'rb'))
        sum = np.zeros(tau)
        sum[:tau_p + 1] = self_short[:tau_p + 1]
        sum[tau_p + 1:] = self_short[tau_p + 1:] + self_long[tau_p + 1:]

        figure = plt.figure(figsize=(16, 9))
        plt.semilogx(self_short, linewidth=5, label='{} - Short'.format(ticker))
        plt.semilogx(self_long, linewidth=5, label='{} - Long'.format(ticker))
        plt.semilogx(sum, linewidth=5, label='{} - Sum'.format(ticker))
        plt.semilogx(self_response, linewidth=5, label='{} - Self-response'.format(ticker))
        plt.semilogx(self_shuffle, linewidth=5, label='{} - Shuffle'.format(ticker))
        plt.plot((tau_p, tau_p), (0, max(self_short)), '--', label=r"$\tau' $ = {}"
                    .format(tau_p))
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
        taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker,
                                     year, '')

        return None

    except FileNotFoundError:
        print('No data')
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_time_short_long_plot(ticker_i, ticker_j, year, tau, tau_p):
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

            function_name =  taq_cross_response_year_avg_time_short_long_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')
            cross = pickle.load(open(''.join((
                            '../../taq_data/responses_time_short_long_data_{2}/taq_cross'
                            + '_response_year_time_short_long_tau_data_tau_{3}_tau_p_{4}/taq_cross_response_year_time_short_long_tau_data_tau_{3}_tau_p_{4}'
                            + '_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, tau, tau_p), 'rb'))

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


def main():
    # taq_cross_response_year_avg_time_short_long_plot('AAPL', 'MSFT', '2008', 1000, 10)
    taq_self_response_year_avg_time_short_long_plot('AAPL', '2008', 1000, 10)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()