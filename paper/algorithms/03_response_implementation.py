'''TAQ response comparison.

Plot the results of the response of different scales in the same figure to
compare.

This script requires the following modules:
    * matplotlib
    * numpy

The module contains the following functions:
    * taq_self_response_year_avg_plot - plots the self-response average for a
      year.
    * taq_cross_response_year_avg_plot - plots the cross-response average for a
      year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import os
import pickle
from itertools import product

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

        # Load data
        self_time = pickle.load(open(''.join((
                        f'../../project/taq_data/article_reproduction_data'
                        + f'_{year}/taq_self_response_year_data/taq_self'
                        + f'_response_year_data_{year}_{ticker}.pickle')
                        .split()), 'rb'))
        self_event = pickle.load(open(''.join((
                        f'../../project/taq_data/responses_event_data_{year}/'
                        + f'taq_self_response_year_responses_event_data/taq'
                        + f'_self_response_year_responses_event_data_{year}'
                        + f'_{ticker}.pickle').split()), 'rb'))
        self_activity = pickle.load(open(''.join((
                        f'../../project/taq_data/responses_time_activity_data'
                        + f'_{year}/taq_self_response_year_responses_time'
                        + f'_activity_data/taq_self_response_year_responses'
                        + f'_time_activity_data_{year}_{ticker}.pickle')
                        .split()), 'rb'))

        figure = plt.figure(figsize=(16, 9))
        ax = figure.add_subplot(111)
        plt.semilogx(self_time, linewidth=5, label=f'Time')
        plt.semilogx(self_event, linewidth=5, label=f'Event')
        plt.semilogx(self_activity, linewidth=5, label=f'Activity')
        plt.legend(loc='best', fontsize=35)
        # plt.title(f'Self-response {ticker}', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=40)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=40)
        plt.xticks(fontsize=35)
        plt.yticks(fontsize=35)
        plt.xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(35)
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        plt.savefig(f'../plot/03_self_response_implementation_{year}.png')

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

            cross_time = pickle.load(open(''.join((
                            f'../../project/taq_data/article_reproduction_data'
                            + f'_{year}/taq_cross_response_year_data/taq_cross'
                            + f'_response_year_data_{year}_{ticker_i}i'
                            + f'_{ticker_j}j.pickle').split()), 'rb'))
            cross_event = pickle.load(open(''.join((
                            f'../../project/taq_data/responses_event_data'
                            + f'_{year}/taq_cross_response_year_responses'
                            + f'_event_data/taq_cross_response_year_responses'
                            + f'_event_data_{year}_{ticker_i}i_{ticker_j}j'
                            + f'.pickle').split()), 'rb'))
            cross_activity = pickle.load(open(''.join((
                            f'../../project/taq_data/responses_time_activity'
                            + f'_data_{year}/taq_cross_response_year_responses'
                            + f'_time_activity_data/taq_cross_response_year'
                            + f'_responses_time_activity_data_{year}'
                            + f'_{ticker_i}i_{ticker_j}j.pickle').split()),
                            'rb'))

            figure = plt.figure(figsize=(16, 9))
            ax = figure.add_subplot(111)
            plt.semilogx(cross_time, linewidth=5, label='Time')
            plt.semilogx(cross_event, linewidth=5, label='Event')
            plt.semilogx(cross_activity, linewidth=5, label='Activity')
            plt.legend(loc='best', fontsize=35)
            # plt.title(f'Cross-response {ticker_i}-{ticker_j}', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=45)
            plt.ylabel(r'$R_{ij}(\tau)$', fontsize=45)
            plt.xticks(fontsize=35)
            plt.yticks(fontsize=35)
            plt.xlim(1, 1000)
            # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax.yaxis.offsetText.set_fontsize(35)
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            plt.savefig(f'../plot/03_cross_response_implementation_{year}.png')

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

    ticker_i = 'AAPL'
    ticker_j = 'MSFT'
    year = '2008'

    taq_self_response_year_avg_plot(ticker_i, year)
    taq_cross_response_year_avg_plot(ticker_i, ticker_j, year)

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
