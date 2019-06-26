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

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_time_shift_plot(ticker, year, taus):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = taq_self_response_year_avg_time_shift_plot.__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        figure = plt.figure(figsize=(9, 16))

        for tau_idx, tau_val in enumerate(taus):

            ax = plt.subplot(len(taus), 1, tau_idx + 1)

            times = np.array(range(- 10 * tau_val, 10 * tau_val, tau_val))
            self = pickle.load(open(''.join((
                               '../../taq_data/time_shift_data_{1}/taq_self'
                               + '_response_year_time_shift_data_{2}/taq_self'
                               + '_response_year_time_shift_data_{2}_{1}_{0}'
                               + '.pickle').split())
                               .format(ticker, year, tau_val), 'rb'))

            ax.plot(times, self, linewidth=5, label=r'{}'.format(ticker))
            ax.legend(loc='best', fontsize=15)
            ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax.set_ylabel(r'$R_{ii}(\tau)$', fontsize=15)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            ax.grid(True)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
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


def taq_cross_response_year_avg_time_shift_plot(ticker_i, ticker_j, year,
                                                taus):
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

            function_name = taq_cross_response_year_avg_time_shift_plot. \
                            __name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')

            figure = plt.figure(figsize=(9, 16))

            for tau_idx, tau_val in enumerate(taus):

                ax = plt.subplot(len(taus), 1, tau_idx + 1)

                times = np.array(range(- 10 * tau_val, 10 * tau_val, tau_val))
                cross = pickle.load(open(''.join((
                                   '../../taq_data/time_shift_data_{2}/taq'
                                   + '_cross_response_year_time_shift_data_tau'
                                   + '_{3}/taq_cross_response_year_time_shift'
                                   + '_data_tau_{3}_{2}_{0}i_{1}j.pickle')
                                   .split())
                                   .format(ticker_i, ticker_j, year, tau_val),
                                   'rb'))

                ax.plot(times, cross, linewidth=5, label=r'{} - {}'
                        .format(ticker_i, ticker_j))
                ax.legend(loc='best', fontsize=15)
                ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
                ax.set_xlabel(r'Time shift $[s]$', fontsize=15)
                ax.set_ylabel(r'$R_{ij}(\tau)$', fontsize=15)
                plt.xticks(fontsize=10)
                plt.yticks(fontsize=10)
                ax.grid(True)
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
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
