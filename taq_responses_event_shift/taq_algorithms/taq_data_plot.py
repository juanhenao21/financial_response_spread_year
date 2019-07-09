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


def taq_self_response_year_avg_responses_event_shift_plot(ticker, year,
                                                          shifts):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
    """

    try:

        function_name = taq_self_response_year_avg_responses_event_shift_plot\
                        .__name__
        taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                      ticker, year, '', '')

        figure = plt.figure(figsize=(16, 9))

        for shift in shifts:

            self_ = pickle.load(open(''.join((
                            '../../taq_data/responses_event_shift_data_{1}/'
                            + 'taq_self_response_year_responses_event_shift'
                            + '_data_shift_{2}/taq_self_response_year'
                            + '_responses_event_shift_data_shift_{2}_{1}_{0}'
                            + '.pickle').split())
                            .format(ticker, year, shift), 'rb'))

            plt.semilogx(self_, linewidth=5, label='Shift {} s'.format(shift))

        self_ = pickle.load(open(''.join((
                            '../../taq_data/responses_event_shift_data_{1}/taq'
                            + '_self_response_year_responses_event_shift_data'
                            + '_shift_tau/taq_self_response_year_responses'
                            + '_event_shift_data_shift_tau_{1}_{0}.pickle')
                            .split()).format(ticker, year), 'rb'))

        plt.semilogx(self_, linewidth=5, label=r'Shift $\tau / 2$')

        plt.legend(loc='best', fontsize=25)
        plt.title('Self-response transactions {}'.format(ticker), fontsize=40)
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

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_event_shift_plot(ticker_i, ticker_j,
                                                           year, shifts):
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
                taq_cross_response_year_avg_responses_event_shift_plot. \
                __name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, '', '')
            figure = plt.figure(figsize=(16, 9))

            for shift in shifts:

                cross = pickle.load(open(''.join((
                            '../../taq_data/responses_event_shift_data_{2}/'
                            + 'taq_cross_response_year_responses_event_shift'
                            + '_data_shift_{3}/taq_cross_response_year'
                            + '_responses_event_shift_data_shift_{3}_{2}_{0}i'
                            + '_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, shift),
                            'rb'))

                plt.semilogx(cross, linewidth=5, label='Shift {} s'
                             .format(shift))

            cross = pickle.load(open(''.join((
                                '../../taq_data/responses_event_shift_data'
                                + '_{2}/taq_cross_response_year_responses'
                                + '_event_shift_data_shift_tau/taq_cross'
                                + '_response_year_responses_event_shift_data'
                                + '_shift_tau_{2}_{0}i_{1}j.pickle').split())
                                .format(ticker_i, ticker_j, year), 'rb'))

            plt.semilogx(cross, linewidth=5, label=r'Shift $\tau / 2$')

            plt.legend(loc='best', fontsize=25)
            plt.title('Cross-response transactions {} - {}'.format(ticker_i,
                      ticker_j), fontsize=40)
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
    pass

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
