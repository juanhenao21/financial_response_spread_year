'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_responses_physical_shift module.

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle
    * taq_data_tools_event_shift

The module contains the following functions:
    * taq_self_response_year_avg_responses_physical_shift_plot - plots the
      self-response average for a year.
    * taq_cross_response_year_avg_responses_physical_shift_plot - plots the
      cross-response average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules


from matplotlib import pyplot as plt
import numpy as np
import pickle

import taq_data_tools_responses_physical_shift

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_physical_shift_plot(ticker, year,
                                                             shifts):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = \
            taq_self_response_year_avg_responses_physical_shift_plot.__name__
        taq_data_tools_responses_physical_shift \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        figure = plt.figure(figsize=(16, 9))

        # Figure with different plots for different shifts
        for shift in shifts:

            # Load data
            self_ = pickle.load(open(
                f'../../taq_data/responses_physical_shift_data_{year}/taq_self'
                + f'_response_year_responses_physical_shift_data_shift_{shift}'
                + f'/taq_self_response_year_responses_physical_shift_data'
                + f'_shift_{shift}_{year}_{ticker}.pickle', 'rb'))

            plt.semilogx(self_, linewidth=5, label='Shift {} s'.format(shift))

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=6,
                   fontsize=15)
        plt.title(f'Self-response - {ticker}', fontsize=40)
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
        taq_data_tools_responses_physical_shift \
            .taq_save_plot(function_name, figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_physical_shift_plot(ticker_i,
                                                              ticker_j, year,
                                                              shifts):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Cross-response
        return None

    else:
        try:
            function_name = \
                taq_cross_response_year_avg_responses_physical_shift_plot \
                .__name__
            taq_data_tools_responses_physical_shift \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            figure = plt.figure(figsize=(16, 9))

            # Figure with different plots for different shifts
            for shift in shifts:

                cross = pickle.load(open(
                    f'../../taq_data/responses_physical_shift_data_{year}/taq'
                    + f'_cross_response_year_responses_physical_shift_data'
                    + f'_shift_{shift}/taq_cross_response_year_responses'
                    + f'_physical_shift_data_shift_{shift}_{year}_{ticker_i}i'
                    + f'_{ticker_j}j.pickle', 'rb'))

                plt.semilogx(cross, linewidth=5, label=f'Shift {shift} s')

            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=6,
                       fontsize=15)
            plt.title(f'Cross-response {ticker_i} - {ticker_j}', fontsize=40)
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
            taq_data_tools_responses_physical_shift \
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
