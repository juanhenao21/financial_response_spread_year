'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_responses_physical_short_long module.

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle
    * taq_data_tools_responses_physical_short_long

The module contains the following functions:
    * taq_self_response_year_avg_responses_physical_short_long_plot - plots
      the self-response average for a year.
    * taq_cross_response_year_avg_responses_physical_short_long_plot - plots
      the cross-response average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import pickle

import taq_data_tools_responses_physical_short_long

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_physical_short_long_plot(ticker, year,
                                                                  tau, tau_p):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2008').
    :param tau: integer greater than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:

        function_name = \
            taq_self_response_year_avg_responses_physical_short_long_plot. \
            __name__
        taq_data_tools_responses_physical_short_long \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        # Load data
        (self_short,
         self_long,
         self_response,
         self_shuffle) = pickle.load(open(
             f'../../taq_data/responses_physical_short_long_data_{year}/taq'
             + f'_self_response_year_physical_short_long_data_tau_{tau}_tau_p'
             + f'_{tau_p}/taq_self_response_year_responses_physical_short_long'
             + f'_data_tau_{tau}_tau_p_{tau_p}_{year}_{ticker}.pickle', 'rb'))

        # Addition of the short and long response signal
        sum = np.zeros(tau)
        sum[:tau_p + 1] = self_short[:tau_p + 1]
        sum[tau_p + 1:] = self_short[tau_p + 1:] + self_long[tau_p + 1:]

        figure = plt.figure(figsize=(16, 9))
        plt.semilogx(self_short, linewidth=5, label=f'{ticker} - Short')
        plt.semilogx(self_long, linewidth=5, label=f'{ticker} - Long')
        plt.semilogx(sum, linewidth=5, label=f'{ticker} - Sum')
        plt.semilogx(self_response, linewidth=5,
                     label=f'{ticker} - Self-response')
        plt.semilogx(self_shuffle, linewidth=5, label=f'{ticker} - Shuffle')
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
        taq_data_tools_responses_physical_short_long \
            .taq_save_plot(f'{function_name}_tau_{tau}_tau_p_{tau_p}', figure,
                           ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_physical_short_long_plot(ticker_i,
                                                                   ticker_j,
                                                                   year, tau,
                                                                   tau_p):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL')
    :param year: string of the year to be analyzed (i.e '2008')
    :param tau: integer greater than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = \
                taq_cross_response_year_avg_responses_physical_short_long_plot. \
                __name__
            taq_data_tools_responses_physical_short_long \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            # Load data
            (cross_short,
             cross_long,
             cross_response,
             cross_shuffle) = pickle.load(open(
                f'../../taq_data/responses_physical_short_long_data_{year}/taq'
                + f'_cross_response_year_responses_physical_short_long_data'
                + f'_tau_{tau}_tau_p_{tau_p}/taq_cross_response_year_responses'
                + f'_physical_short_long_data_tau_{tau}_tau_p_{tau_p}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            # Addition of the short and long response signal
            sum = np.zeros(tau)
            sum[:tau_p + 1] = cross_short[:tau_p + 1]
            sum[tau_p + 1:] = cross_short[tau_p + 1:] + cross_long[tau_p + 1:]

            figure = plt.figure(figsize=(16, 9))
            plt.semilogx(cross_short, linewidth=5,
                         label=f'{ticker_i} - {ticker_j} - Short')
            plt.semilogx(cross_long, linewidth=5,
                         label=f'{ticker_i} - {ticker_j} - Long')
            plt.semilogx(sum, linewidth=5,
                         label=f'{ticker_i} - {ticker_j} - Sum')
            plt.semilogx(cross_response, linewidth=5,
                         label=f'{ticker_i} - {ticker_j} - Cross-response')
            plt.semilogx(cross_shuffle, linewidth=5,
                         label=f'{ticker_i} - {ticker_j} - Shuffle')
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
            taq_data_tools_responses_physical_short_long \
                .taq_save_plot(f'{function_name}_tau_{tau}_tau_p_{tau_p}',
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
