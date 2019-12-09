'''Event and time shift figures

Plot the event and time shift for the stocks AAPL, CVX, GS, JPM, MSFT, and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------


def taq_trade_scale_shift_year_avg_plot(ticker_i, ticker_j, year,
                                                 taus):
    """Plots the self- and cross-response for a year in trade time scale.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure, axs = plt.subplots(2, len(taus), figsize=(16,9), sharex='col',
                                   sharey='row', gridspec_kw={'hspace': 0,
                                   'wspace': 0})

        (ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8) = axs

        # Figure with different plots for different taus
        t_ax_1_5 = np.array(range(- 10 * taus[0], 10 * taus[0], 1))
        t_ax_2_6 = np.array(range(- 10 * taus[1], 10 * taus[1], 1))
        t_ax_3_7 = np.array(range(- 10 * taus[2], 10 * taus[2], 1))
        t_ax_4_8 = np.array(range(- 10 * taus[3], 10 * taus[3], 1))

        # Load data
        self_event_ax1 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data_{year}/taq_self_response'
            + f'_year_event_shift_data_tau_{taus[0]}/taq_self_response_year'
            + f'_event_shift_data_tau_{taus[0]}_{year}_{ticker_i}.pickle')
            .split()), 'rb'))

        max_pos_ax1 = np.where(max(self_event_ax1) == self_event_ax1)[0][0]

        ax1.plot(t_ax_1_5, self_event_ax1, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[0]))

        # Plot line in the peak of the figure
        ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                 (0, self_event_ax1[max_pos_ax1]), '--',
                 label=r'Max $t$ = {} trades'
                 .format(max_pos_ax1 - 10 * taus[0]))

        ax1.legend(loc='upper left', fontsize=15)
        # ax.set_title(r'$\tau_{trade}$ = {}'.format(tau_val), fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau_{trades})$', fontsize=20)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        # Load data
        self_event_ax2 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data_{year}/taq_self_response'
            + f'_year_event_shift_data_tau_{taus[1]}/taq_self_response_year'
            + f'_event_shift_data_tau_{taus[1]}_{year}_{ticker_i}.pickle')
            .split()), 'rb'))

        max_pos_ax2 = np.where(max(self_event_ax2) == self_event_ax2)[0][0]

        ax2.plot(t_ax_2_6, self_event_ax2, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[1]))

        # Plot line in the peak of the figure
        ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                 (0, self_event_ax2[max_pos_ax2]), '--',
                 label=r'Max $t$ = {} trades'
                 .format(max_pos_ax2 - 10 * taus[1]))

        ax2.legend(loc='upper left', fontsize=15)
        # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax2.grid(True)

        # Load data
        self_event_ax3 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data_{year}/taq_self_response'
            + f'_year_event_shift_data_tau_{taus[2]}/taq_self_response_year'
            + f'_event_shift_data_tau_{taus[2]}_{year}_{ticker_i}.pickle')
            .split()), 'rb'))

        max_pos_ax3 = np.where(max(self_event_ax3) == self_event_ax3)[0][0]

        ax3.plot(t_ax_3_7, self_event_ax3, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[2]))

        # Plot line in the peak of the figure
        ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                 (0, self_event_ax3[max_pos_ax3]), '--',
                 label=r'Max $t$ = {} trades'
                 .format(max_pos_ax3 - 10 * taus[2]))

        ax3.legend(loc='upper left', fontsize=15)
        # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax3.grid(True)

        # Load data
        self_event_ax4 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data_{year}/taq_self_response'
            + f'_year_event_shift_data_tau_{taus[3]}/taq_self_response_year'
            + f'_event_shift_data_tau_{taus[3]}_{year}_{ticker_i}.pickle')
            .split()), 'rb'))

        max_pos_ax4 = np.where(max(self_event_ax4) == self_event_ax4)[0][0]

        ax4.plot(t_ax_4_8, self_event_ax4, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[3]))

        # Plot line in the peak of the figure
        ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                 (0, self_event_ax4[max_pos_ax4]), '--',
                 label=r'Max $t$ = {} trades'
                 .format(max_pos_ax4 - 10 * taus[3]))

        ax4.legend(loc='upper left', fontsize=15)
        # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax4.grid(True)

        # Load data
        cross_event_ax5 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data'
            + f'_{year}/taq_cross_response_year_event_shift_data_tau_{taus[0]}'
            + f'/taq_cross_response_year_event_shift_data_tau_{taus[0]}'
            + f'_{year}_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        max_pos_ax5 = np.where(max(cross_event_ax5) == cross_event_ax5)[0][0]

        ax5.plot(t_ax_1_5, cross_event_ax5, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[0]))
        # Plot line in the peak of the figure
        ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                    (0, cross_event_ax5[max_pos_ax5]),
                    '--', label=r'Max $t$ = {} trades'
                    .format(max_pos_ax5 - 10 * taus[0]))
        ax5.legend(loc='upper left', fontsize=15)
        # ax1.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax5.set_xlabel(r'Trade shift [trades]', fontsize=20)
        ax5.set_ylabel(r'$R_{ij}(\tau_{trades})$', fontsize=20)
        ax5.tick_params(axis='x', labelsize=15)
        ax5.tick_params(axis='y', labelsize=15)
        ax5.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax5.yaxis.offsetText.set_fontsize(15)
        ax5.xaxis.set_major_locator(ticker.MaxNLocator(4))
        ax5.grid(True)

        # Load data
        cross_event_ax6 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data'
            + f'_{year}/taq_cross_response_year_event_shift_data_tau_{taus[1]}'
            + f'/taq_cross_response_year_event_shift_data_tau_{taus[1]}'
            + f'_{year}_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        max_pos_ax6 = np.where(max(cross_event_ax6) == cross_event_ax6)[0][0]

        ax6.plot(t_ax_2_6, cross_event_ax6, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[2]))
        # Plot line in the peak of the figure
        ax6.plot((t_ax_2_6[max_pos_ax6], t_ax_2_6[max_pos_ax6]),
                    (0, cross_event_ax6[max_pos_ax6]),
                    '--', label=r'Max $t$ = {} trades'
                    .format(max_pos_ax6 - 10 * taus[1]))
        ax6.legend(loc='upper left', fontsize=15)
        # ax1.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax6.set_xlabel(r'Trade shift [trades]', fontsize=20)
        ax6.tick_params(axis='x', labelsize=15)
        ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
        ax6.grid(True)

        # Load data
        cross_event_ax7 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data'
            + f'_{year}/taq_cross_response_year_event_shift_data_tau_{taus[2]}'
            + f'/taq_cross_response_year_event_shift_data_tau_{taus[2]}'
            + f'_{year}_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        max_pos_ax7 = np.where(max(cross_event_ax7) == cross_event_ax7)[0][0]

        ax7.plot(t_ax_3_7, cross_event_ax7, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[2]))
        # Plot line in the peak of the figure
        ax7.plot((t_ax_3_7[max_pos_ax7], t_ax_3_7[max_pos_ax7]),
                    (0, cross_event_ax7[max_pos_ax7]),
                    '--', label=r'Max $t$ = {} trades'
                    .format(max_pos_ax7 - 10 * taus[2]))
        ax7.legend(loc='upper left', fontsize=15)
        # ax1.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax7.set_xlabel(r'Trade shift [trades]', fontsize=20)
        ax7.tick_params(axis='x', labelsize=15)
        ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
        ax7.grid(True)

        # Load data
        cross_event_ax8 = pickle.load(open(''.join((
            f'../../project/taq_data/event_shift_data'
            + f'_{year}/taq_cross_response_year_event_shift_data_tau_{taus[3]}'
            + f'/taq_cross_response_year_event_shift_data_tau_{taus[3]}'
            + f'_{year}_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

        max_pos_ax8 = np.where(max(cross_event_ax8) == cross_event_ax8)[0][0]

        ax8.plot(t_ax_4_8, cross_event_ax8, linewidth=5,
                 label=r'$\tau_{trades} = %d$' %(taus[3]))
        # Plot line in the peak of the figure
        ax8.plot((t_ax_4_8[max_pos_ax8], t_ax_4_8[max_pos_ax8]),
                    (0, cross_event_ax8[max_pos_ax8]),
                    '--', label=r'Max $t$ = {} trades'
                    .format(max_pos_ax8 - 10 * taus[3]))
        ax8.legend(loc='upper left', fontsize=15)
        # ax1.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
        ax8.set_xlabel(r'Trade shift [trades]', fontsize=20)
        ax8.tick_params(axis='x', labelsize=15)
        ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
        ax8.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_trade')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_time_scale_shift_year_avg_plot(ticker_i, ticker_j, year,
                                                taus):
    """Plots the self- and cross-response for a year in second time scale.

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
            figure, axs = plt.subplots(2, len(taus), figsize=(16,9), sharex='col',
                                    sharey='row', gridspec_kw={'hspace': 0,
                                    'wspace': 0})

            (ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8) = axs

            # Figure with different plots for different taus
            t_ax_1_5 = np.array(range(- 10 * taus[0], 10 * taus[0], 1))
            t_ax_2_6 = np.array(range(- 10 * taus[1], 10 * taus[1], 1))
            t_ax_3_7 = np.array(range(- 10 * taus[2], 10 * taus[2], 1))
            t_ax_4_8 = np.array(range(- 10 * taus[3], 10 * taus[3], 1))

            # Load data
            self_time_ax1 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[0]}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax1 = np.where(max(self_time_ax1) == self_time_ax1)[0][0]

            ax1.plot(t_ax_1_5, self_time_ax1, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[0]))

            # Plot line in the peak of the figure
            ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                    (0, self_time_ax1[max_pos_ax1]), '--',
                    label=r'Max $t$ = {} seconds'
                    .format(max_pos_ax1 - 10 * taus[0]))

            ax1.legend(loc='upper left', fontsize=15)
            # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax1.set_ylabel(r'$R_{ii}(\tau_{seconds})$', fontsize=20)
            ax1.tick_params(axis='y', labelsize=15)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(15)
            ax1.grid(True)

            # Load data
            self_time_ax2 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[1]}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax2 = np.where(max(self_time_ax2) == self_time_ax2)[0][0]

            ax2.plot(t_ax_2_6, self_time_ax2, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[0]))

            # Plot line in the peak of the figure
            ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                    (0, self_time_ax2[max_pos_ax2]), '--',
                    label=r'Max $t$ = {} seconds'
                    .format(max_pos_ax2 - 10 * taus[1]))

            ax2.legend(loc='upper left', fontsize=15)
            # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax2.grid(True)

            # Load data
            self_time_ax3 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[2]}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax3 = np.where(max(self_time_ax3) == self_time_ax3)[0][0]

            ax3.plot(t_ax_3_7, self_time_ax3, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[0]))

            # Plot line in the peak of the figure
            ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                    (0, self_time_ax3[max_pos_ax3]), '--',
                    label=r'Max $t$ = {} seconds'
                    .format(max_pos_ax3 - 10 * taus[2]))

            ax3.legend(loc='upper left', fontsize=15)
            # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax3.grid(True)

            # Load data
            self_time_ax4 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[3]}/taq_self'
                + f'_response_year_time_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax4 = np.where(max(self_time_ax4) == self_time_ax4)[0][0]

            ax4.plot(t_ax_4_8, self_time_ax4, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[0]))

            # Plot line in the peak of the figure
            ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                    (0, self_time_ax4[max_pos_ax4]), '--',
                    label=r'Max $t$ = {} seconds'
                    .format(max_pos_ax4 - 10 * taus[3]))

            ax4.legend(loc='upper left', fontsize=15)
            # ax.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax4.grid(True)

            # Load data
            cross_time_ax5 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[0]}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

            max_pos_ax5 = np.where(max(cross_time_ax5) == cross_time_ax5)[0][0]

            ax5.plot(t_ax_1_5, cross_time_ax5, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[0]))
            # Plot line in the peak of the figure
            ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                        (0, cross_time_ax5[max_pos_ax5]),
                        '--', label=r'Max $t$ = {} seconds'
                        .format(max_pos_ax5 - 10 * taus[0]))
            ax5.legend(loc='upper left', fontsize=15)
            # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax5.set_xlabel(r'Time shift $[s]$', fontsize=20)
            ax5.set_ylabel(r'$R_{ij}(\tau_{seconds})$', fontsize=20)
            ax5.tick_params(axis='x', labelsize=15)
            ax5.tick_params(axis='y', labelsize=15)
            ax5.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax5.yaxis.offsetText.set_fontsize(15)
            ax5.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax5.grid(True)

            # Load data
            cross_time_ax6 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[1]}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

            max_pos_ax6 = np.where(max(cross_time_ax6) == cross_time_ax6)[0][0]

            ax6.plot(t_ax_2_6, cross_time_ax6, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[1]))
            # Plot line in the peak of the figure
            ax6.plot((t_ax_2_6[max_pos_ax6], t_ax_2_6[max_pos_ax6]),
                        (0, cross_time_ax6[max_pos_ax6]),
                        '--', label=r'Max $t$ = {} seconds'
                        .format(max_pos_ax6 - 10 * taus[1]))
            ax6.legend(loc='upper left', fontsize=15)
            # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax6.set_xlabel(r'Time shift $[s]$', fontsize=20)
            ax6.tick_params(axis='x', labelsize=15)
            ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax6.grid(True)

            # Load data
            cross_time_ax7 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[2]}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

            max_pos_ax7 = np.where(max(cross_time_ax7) == cross_time_ax7)[0][0]

            ax7.plot(t_ax_3_7, cross_time_ax7, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[2]))
            # Plot line in the peak of the figure
            ax7.plot((t_ax_3_7[max_pos_ax7], t_ax_3_7[max_pos_ax7]),
                        (0, cross_time_ax7[max_pos_ax7]),
                        '--', label=r'Max $t$ = {} seconds'
                        .format(max_pos_ax7 - 10 * taus[2]))
            ax7.legend(loc='upper left', fontsize=15)
            # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax7.set_xlabel(r'Time shift $[s]$', fontsize=20)
            ax7.tick_params(axis='x', labelsize=15)
            ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax7.grid(True)

            # Load data
            cross_time_ax8 = pickle.load(open(''.join((
                f'../../project/taq_data/time_shift_data_{year}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[3]}/taq_cross'
                + f'_response_year_time_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle').split()), 'rb'))

            max_pos_ax8 = np.where(max(cross_time_ax8) == cross_time_ax8)[0][0]

            ax8.plot(t_ax_4_8, cross_time_ax8, linewidth=5,
                     label=r'$\tau_{seconds} = %d$' %(taus[3]))
            # Plot line in the peak of the figure
            ax8.plot((t_ax_4_8[max_pos_ax8], t_ax_4_8[max_pos_ax8]),
                        (0, cross_time_ax8[max_pos_ax8]),
                        '--', label=r'Max $t$ = {} seconds'
                        .format(max_pos_ax8 - 10 * taus[3]))
            ax8.legend(loc='upper left', fontsize=15)
            # ax2.set_title(r'$\tau$ = {}'.format(tau_val), fontsize=20)
            ax8.set_xlabel(r'Time shift $[s]$', fontsize=20)
            ax8.tick_params(axis='x', labelsize=15)
            ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax8.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig('../plot/04_shift_time')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_scale_responses_year_avg_shift_plot(ticker_i, ticker_j, year,
                                                  shifts):
    """Plots the responses average for a year with trade time shifts.

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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

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

            ax1.semilogx(self_event, linewidth=5, label='Shift {} trades'
                         .format(shift))

            cross_event = pickle.load(open(''.join((
                '../../project/taq_data/responses_event_shift_data_{2}/'
                + 'taq_cross_response_year_responses_event_shift'
                + '_data_shift_{3}/taq_cross_response_year'
                + '_responses_event_shift_data_shift_{3}_{2}_{0}i'
                + '_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, shift),
                'rb'))

            ax2.semilogx(cross_event, linewidth=5, label='Shift {} trades'
                         .format(shift))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title('{}'.format(ticker_i), fontsize=40)
        ax1.set_xlabel(r'$\tau \, [trades]$', fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau_{trades})$', fontsize=20)
        ax1.set_xlim(1, 10000)
        # ax1.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title('{} - {}'.format(ticker_i, ticker_j), fontsize=40)
        ax2.set_xlabel(r'$\tau \, [trades]$', fontsize=20)
        ax2.set_ylabel(r'$R_{ij}(\tau_{trades})$', fontsize=20)
        ax2.set_xlim(1, 10000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_responses_trades')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------

def taq_time_scale_responses_year_avg_shift_plot(ticker_i, ticker_j, year,
                                                 shifts):
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
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Figure with different plots for different shifts
        for shift in shifts:

            # Load data
            self_time = pickle.load(open(''.join((
                '../../project/taq_data/responses_time_shift_data'
                + '_{1}/taq_self_response_year_responses_time'
                + '_shift_data_shift_{2}/taq_self_response_year'
                + '_responses_time_shift_data_shift_{2}_{1}_{0}.pickle')
                .split()).format(ticker_i, year, shift), 'rb'))

            ax1.semilogx(self_time, linewidth=5, label='Shift {} s'
                         .format(shift))

            cross_time = pickle.load(open(''.join((
                            '../../project/taq_data/responses_time_shift_data'
                            + '_{2}/taq_cross_response_year_responses_time'
                            + '_shift_data_shift_{3}/taq_cross_response'
                            + '_year_responses_time_shift_data_shift_{3}'
                            + '_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, shift),
                            'rb'))

            ax2.semilogx(cross_time, linewidth=5, label='Shift {} s'
                         .format(shift))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title('{}'.format(ticker_i), fontsize=40)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau_{seconds})$', fontsize=20)
        ax1.set_xlim(1, 10000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title('{} - {}'.format(ticker_i, ticker_j), fontsize=40)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax2.set_ylabel(r'$R_{ij}(\tau_{seconds})$', fontsize=20)
        ax2.set_xlim(1, 10000)
        # ax4.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_responses_time')

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

    # taq_trade_scale_shift_year_avg_plot('GS', 'JPM', year, taus)
    # taq_time_scale_shift_year_avg_plot('GS', 'JPM', year, taus)
    taq_trade_scale_responses_year_avg_shift_plot('GS', 'JPM', year, shifts)
    taq_time_scale_responses_year_avg_shift_plot('GS', 'JPM', year, shifts)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
