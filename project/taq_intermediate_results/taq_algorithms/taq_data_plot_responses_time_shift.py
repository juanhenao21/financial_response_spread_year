'''Test average responses time shift.

Implementation of the average of the responses shift results. This script takes
the data of all the self- and cross-responses computed with a time shift, join
the data with the same shift value, and find the average reaction time.

This script requires the following modules:
    * matplotlib
    * numpy
    * itertools

The module contains the following functions:
    * taq_self_response_year_avg_responses_time_shift_plot - plots the self-
      response average for a year.
    * taq_cross_response_year_avg_responses_time_shift_plot - plots the cross-
      response average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules


from matplotlib import pyplot as plt
import numpy as np
import os
import pickle
from itertools import product as iprod

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_shift_plot(tickers, year,
                                                         shifts):
    """Plots the average of the self-response average for a year for each
     shift.

    :param tickers: list of strings of the abbreviation of the stock to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2008').
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = taq_self_response_year_avg_responses_time_shift_plot. \
                        __name__

        for shift in shifts:

            figure = plt.figure(figsize=(16, 9))
            avg_val = np.zeros(10000)

            # Figure with the average of different stocks for the same shift
            for ticker in tickers:

                # Load data
                self_ = pickle.load(open(''.join((
                                f'../../taq_data/responses_time_shift_data_'
                                + f'{year}/taq_self_response_year_responses'
                                + f'_time_shift_data_shift_{shift}/taq_self'
                                + f'_response_year_responses_time_shift_data'
                                + f'_shift_{shift}_{year}_{ticker}.pickle'
                                ).split()), 'rb'))

                plt.semilogx(self_, linewidth=3, alpha=0.1, label=f'{ticker}')

                avg_val += self_

            plt.semilogx(avg_val / len(tickers), linewidth=5, label='Average')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=7,
                       fontsize=15)
            plt.title(f'Self-response - shift {shift}s', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=35)
            plt.ylabel(r'$R_{ii}(\tau)$', fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            plt.xlim(1, 10000)
            # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            plt.savefig(''.join((
                f'../taq_plot/taq_data_plot_responses_time_shift_average/'
                + f'{function_name}_{shift}.png').split()))

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_shift_plot(tickers, year,
                                                          shifts):
    """Plots the average of the cross-response average for a year for each
     shift.

    :param tickers: list of strings of the abbreviation of the stock to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2008')
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    ticker_couples = list(iprod(tickers, tickers))

    try:
        function_name = \
            taq_cross_response_year_avg_responses_time_shift_plot.__name__

        for shift in shifts:

            figure = plt.figure(figsize=(16, 9))
            avg_val = np.zeros(10000)

            # Figure with the average of different stocks for the same shift
            for couple in ticker_couples:

                ticker_i = couple[0]
                ticker_j = couple[1]

                if (ticker_i == ticker_j):
                    # Self-response
                    pass

                else:

                    # Load data
                    cross = pickle.load(open(''.join((
                                    f'../../taq_data/responses_time_shift_data'
                                    + f'_{year}/taq_cross_response_year'
                                    + f'_responses_time_shift_data_shift'
                                    + f'_{shift}/taq_cross_response_year'
                                    + f'_responses_time_shift_data_shift'
                                    + f'_{shift}_{year}_{ticker_i}i'
                                    + f'_{ticker_j}j.pickle').split()), 'rb'))

                    plt.semilogx(cross, linewidth=3, alpha=0.1,
                                 label=f'{ticker_i}-{ticker_j}')

                    avg_val += cross

            plt.semilogx(avg_val / 30, linewidth=5,
                         label='Average')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=7,
                       fontsize=15)
            plt.title(f'Cross-response - shift {shift}s', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=35)
            plt.ylabel(r'$R_{ij}(\tau)$', fontsize=35)
            plt.xticks(fontsize=25)
            plt.yticks(fontsize=25)
            plt.xlim(1, 10000)
            # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

            # Plotting
            plt.savefig(''.join((
                f'../taq_plot/taq_data_plot_responses_time_shift_average/'
                + f'{function_name}_{shift}.png').split()))

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

    # Tickers and days to analyze
    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    year = '2008'
    shifts = [1, 5, 10, 50, 100, 500, 1000, 5000]

    taq_self_response_year_avg_responses_time_shift_plot(tickers, year,
                                                         shifts)
    taq_cross_response_year_avg_responses_time_shift_plot(tickers, year,
                                                          shifts)

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
