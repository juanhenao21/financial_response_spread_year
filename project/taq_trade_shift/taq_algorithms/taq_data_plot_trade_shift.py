'''TAQ data plot module.

The functions in the module plot the data obtained in the
taq_data_analysis_trade_shift module.

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle
    * taq_data_tools_trade_shift

The module contains the following functions:
    * taq_self_response_year_avg_trade_shift_plot - plots the self-response
      average for a year.
    * taq_cross_response_year_avg_trade_shift_plot - plots the cross-response
      average for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import pickle

import taq_data_tools_trade_shift

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_trade_shift_plot(ticker, year, taus):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = taq_self_response_year_avg_trade_shift_plot.__name__
        taq_data_tools_trade_shift \
            .taq_function_header_print_plot(function_name, ticker, ticker,
                                            year, '', '')

        figure = plt.figure(figsize=(9, 16))

        # Figure with different plots for different taus
        for tau_idx, tau_val in enumerate(taus):

            ax = plt.subplot(len(taus), 1, tau_idx + 1)

            times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))
            # Load data
            self_ = pickle.load(open(
                               f'../../taq_data/trade_shift_data_{year}/taq'
                               + f'_self_response_year_trade_shift_data_tau'
                               + f'_{tau_val}/taq_self_response_year_trade'
                               + f'_shift_data_tau_{tau_val}_{year}_{ticker}'
                               + f'.pickle', 'rb'))

            if np.where(max(self_) == self_)[0]:
                max_pos = np.where(max(self_) == self_)[0][0]
            else:
                max_pos = 0

            ax.plot(times, self_, linewidth=5, label=r'{}'.format(ticker))
            # Plot line in the peak of the figure
            ax.plot((times[max_pos], times[max_pos]), (0, self_[max_pos]),
                    '--', label=r'Max position $t$ = {}'
                    .format(max_pos - 10 * tau_val))
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
        taq_data_tools_trade_shift \
            .taq_save_plot(function_name, figure, ticker, ticker, year, '')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_trade_shift_plot(ticker_i, ticker_j, year,
                                                 taus):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = taq_cross_response_year_avg_trade_shift_plot. \
                            __name__
            taq_data_tools_trade_shift \
                .taq_function_header_print_plot(function_name, ticker_i,
                                                ticker_j, year, '', '')

            figure = plt.figure(figsize=(9, 16))

            # Figure with different plots for different taus
            for tau_idx, tau_val in enumerate(taus):

                ax = plt.subplot(len(taus), 1, tau_idx + 1)

                times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))
                # Load data
                cross = pickle.load(open(
                                   f'../../taq_data/trade_shift_data_{year}'
                                   + f'/taq_cross_response_year_trade_shift'
                                   + f'_data_tau_{tau_val}/taq_cross_response'
                                   + f'_year_trade_shift_data_tau_{tau_val}'
                                   + f'_{year}_{ticker_i}i_{ticker_j}j.pickle',
                                   'rb'))

                if np.where(max(cross) == cross)[0]:
                    max_pos = np.where(max(cross) == cross)[0][0]
                else:
                    max_pos = 0

                ax.plot(times, cross, linewidth=5, label=r'{} - {}'
                        .format(ticker_i, ticker_j))
                # Plot line in the peak of the figure
                ax.plot((times[max_pos], times[max_pos]), (0, cross[max_pos]),
                        '--', label=r'Max position $t$ = {}'
                        .format(max_pos - 10 * tau_val))
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
            taq_data_tools_trade_shift.taq_save_plot(function_name, figure,
                                                     ticker_i, ticker_j, year,
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
