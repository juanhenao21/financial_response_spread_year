'''Event and time shift figures

Plot the event and time shift for the stocks AAPL, CVX, GS, JPM, MSFT, and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_shift_plot(ticker, year, taus):
    """Plots the self-response average for a year in event scale and time
    scale.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))

        # Figure with different plots for different taus
        for tau_idx, tau_val in enumerate(taus):

            ax1 = plt.subplot(2, len(taus), tau_idx + 1)
            ax2 = plt.subplot(2, len(taus), tau_idx + len(taus) + 1)

            times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))

            # Load data
            self_event = pickle.load(open(''.join((
                '../../project/taq_data/event_shift_data_{1}/taq_self'
                + '_response_year_event_shift_data_tau_{2}/taq'
                + '_self_response_year_event_shift_data_tau_{2}'
                + '_{1}_{0}.pickle').split())
                .format(ticker, year, tau_val), 'rb'))

            max_pos = np.where(max(self_event) == self_event)[0][0]

            ax1.plot(times, self_event, linewidth=5, label=r'$\tau = {}$'
                     .format(tau_val))
            # Plot line in the peak of the figure
            ax1.plot((times[max_pos], times[max_pos]),
                     (0, self_event[max_pos]), '--',
                     label=r'Max position $t$ = {}'
                     .format(max_pos - 10 * tau_val))
            ax1.legend(loc='lower left', fontsize=15)
            # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax1.set_xlabel(r'Event shift', fontsize=20)
            ax1.set_ylabel(r'$R_{ii}(\tau)$', fontsize=20)
            ax1.tick_params(axis='x', labelsize=15)
            ax1.tick_params(axis='y', labelsize=15)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(15)
            ax1.grid(True)

            # Load data
            self_time = pickle.load(open(''.join((
                '../../project/taq_data/time_shift_data_{1}/taq_self'
                + '_response_year_time_shift_data_tau_{2}/taq'
                + '_self_response_year_time_shift_data_tau_{2}'
                + '_{1}_{0}.pickle').split())
                .format(ticker, year, tau_val), 'rb'))

            max_pos = np.where(max(self_time) == self_time)[0][0]

            ax2.plot(times, self_time, linewidth=5, label=r'$\tau = {}$'
                     .format(tau_val))
            # Plot line in the peak of the figure
            ax2.plot((times[max_pos], times[max_pos]), (0, self_time[max_pos]),
                     '--', label=r'Max position $t$ = {}'
                     .format(max_pos - 10 * tau_val))
            ax2.legend(loc='lower left', fontsize=15)
            # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax2.set_xlabel(r'Time shift $[s]$', fontsize=20)
            ax2.set_ylabel(r'$R_{ii}(\tau)$', fontsize=20)
            ax2.tick_params(axis='x', labelsize=15)
            ax2.tick_params(axis='y', labelsize=15)
            ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax2.yaxis.offsetText.set_fontsize(15)
            ax2.grid(True)

        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/04_shift_self')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_shift_plot(ticker_i, ticker_j, year, taus):
    """Plots the cross-response average for a year in event scale and time
    scale.

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
            figure = plt.figure(figsize=(16, 9))

            # Figure with different plots for different taus
            for tau_idx, tau_val in enumerate(taus):

                ax1 = plt.subplot(2, len(taus), tau_idx + 1)
                ax2 = plt.subplot(2, len(taus), tau_idx + len(taus) + 1)

                times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))

                # Load data
                cross_event = pickle.load(open(''.join((
                                   '../../project/taq_data/event_shift_data'
                                   + '_{2}/taq_cross_response_year_event_shift'
                                   + '_data_tau_{3}/taq_cross_response_year'
                                   + '_event_shift_data_tau_{3}_{2}_{0}i_{1}j'
                                   + '.pickle').split())
                                   .format(ticker_i, ticker_j, year, tau_val),
                                   'rb'))

                max_pos = np.where(max(cross_event) == cross_event)[0][0]

                ax1.plot(times, cross_event, linewidth=5, label=r'$\tau = {}$'
                         .format(tau_val))
                # Plot line in the peak of the figure
                ax1.plot((times[max_pos], times[max_pos]),
                         (0, cross_event[max_pos]),
                         '--', label=r'Max position $t$ = {}'
                         .format(max_pos - 10 * tau_val))
                ax1.legend(loc='lower left', fontsize=15)
                # ax1.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
                ax1.set_xlabel(r'Event shift', fontsize=20)
                ax1.set_ylabel(r'$R_{ij}(\tau)$', fontsize=20)
                ax1.tick_params(axis='x', labelsize=15)
                ax1.tick_params(axis='y', labelsize=15)
                ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
                ax1.yaxis.offsetText.set_fontsize(15)
                ax1.grid(True)

                # Load data
                cross_time = pickle.load(open(''.join((
                                   '../../project/taq_data/time_shift_data_{2}'
                                   + '/taq_cross_response_year_time_shift_data'
                                   + '_tau_{3}/taq_cross_response_year_time'
                                   + '_shift_data_tau_{3}_{2}_{0}i_{1}j'
                                   + '.pickle').split())
                                   .format(ticker_i, ticker_j, year, tau_val),
                                   'rb'))

                max_pos = np.where(max(cross_time) == cross_time)[0][0]

                ax2.plot(times, cross_time, linewidth=5, label=r'$\tau = {}$'
                         .format(tau_val))
                # Plot line in the peak of the figure
                ax2.plot((times[max_pos], times[max_pos]),
                         (0, cross_time[max_pos]),
                         '--', label=r'Max position $t$ = {}'
                         .format(max_pos - 10 * tau_val))
                ax2.legend(loc='lower left', fontsize=15)
                # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
                ax2.set_xlabel(r'Time shift $[s]$', fontsize=20)
                ax2.set_ylabel(r'$R_{ij}(\tau)$', fontsize=20)
                ax2.tick_params(axis='x', labelsize=15)
                ax2.tick_params(axis='y', labelsize=15)
                ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
                ax2.yaxis.offsetText.set_fontsize(15)
                ax2.grid(True)

            plt.tight_layout()
            plt.show()

            # Save plot
            figure.savefig('../plot/04_shift_cross')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_responses_year_avg_shift_plot(ticker_i, ticker_j, year, shifts):
    """Plots the responses average for a year with event and time shifts.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e. '2008')
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)

        # Figure with different plots for different shifts
        for shift in shifts:

            # Load data
            self_event = pickle.load(open(''.join((
                '../../project/taq_data/responses_event_shift_data'
                + '_{1}/taq_self_response_year_responses_event'
                + '_shift_data_shift_{2}/taq_self_response_year'
                + '_responses_event_shift_data_shift_{2}_{1}_{0}'
                + '.pickle').split())
                .format(ticker_i, year, shift), 'rb'))

            ax1.semilogx(self_event, linewidth=5, label='Shift {} event'
                         .format(shift))

            self_time = pickle.load(open(''.join((
                '../../project/taq_data/responses_time_shift_data'
                + '_{1}/taq_self_response_year_responses_time'
                + '_shift_data_shift_{2}/taq_self_response_year'
                + '_responses_time_shift_data_shift_{2}_{1}_{0}.pickle')
                .split()).format(ticker_i, year, shift), 'rb'))

            ax2.semilogx(self_time, linewidth=5, label='Shift {} s'
                         .format(shift))

            cross_event = pickle.load(open(''.join((
                '../../project/taq_data/responses_event_shift_data_{2}/'
                + 'taq_cross_response_year_responses_event_shift'
                + '_data_shift_{3}/taq_cross_response_year'
                + '_responses_event_shift_data_shift_{3}_{2}_{0}i'
                + '_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, shift),
                'rb'))

            ax3.semilogx(cross_event, linewidth=5, label='Shift {} event'
                         .format(shift))

            cross_time = pickle.load(open(''.join((
                            '../../project/taq_data/responses_time_shift_data'
                            + '_{2}/taq_cross_response_year_responses_time'
                            + '_shift_data_shift_{3}/taq_cross_response'
                            + '_year_responses_time_shift_data_shift_{3}'
                            + '_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, shift),
                            'rb'))

            ax4.semilogx(cross_time, linewidth=5, label='Shift {} s'
                         .format(shift))

        ax1.legend(loc='upper left', fontsize=20)
        # ax1.title('Self-response transactions {}'.format(ticker),
        #           fontsize=40)
        ax1.set_xlabel(r'$\tau \, [event]$', fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau)$', fontsize=20)
        ax1.set_xlim(1, 10000)
        # ax1.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        # ax2.title('Self-response - {}'.format(ticker), fontsize=40)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax2.set_ylabel(r'$R_{ii}(\tau)$', fontsize=20)
        ax2.set_xlim(1, 10000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        ax3.legend(loc='upper left', fontsize=20)
        # ax3.title('Cross-response transactions {} - {}'.format(ticker_i,
        #           ticker_j), fontsize=40)
        ax3.set_xlabel(r'$\tau \, [event]$', fontsize=20)
        ax3.set_ylabel(r'$R_{ij}(\tau)$', fontsize=20)
        ax3.set_xlim(1, 10000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax3.tick_params(axis='x', labelsize=15)
        ax3.tick_params(axis='y', labelsize=15)
        ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.yaxis.offsetText.set_fontsize(15)
        ax3.grid(True)

        ax4.legend(loc='upper left', fontsize=20)
        # ax4.title('Cross-response {} - {}'.format(ticker_i, ticker_j),
        #           fontsize=40)
        ax4.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax4.set_ylabel(r'$R_{ij}(\tau)$', fontsize=20)
        ax4.set_xlim(1, 10000)
        # ax4.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax4.tick_params(axis='x', labelsize=15)
        ax4.tick_params(axis='y', labelsize=15)
        ax4.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax4.yaxis.offsetText.set_fontsize(15)
        ax4.grid(True)

        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/04_shift_responses')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def main():

    taus = [1, 10, 100, 1000]
    shifts = [1, 10, 100, 1000, 5000]
    year = '2008'

    taq_self_response_year_avg_shift_plot('GS', year, taus)
    taq_cross_response_year_avg_shift_plot('GS', 'JPM', year, taus)
    taq_responses_year_avg_shift_plot('GS', 'JPM', year, shifts)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
