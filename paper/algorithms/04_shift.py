'''Event and physical shift figures

Plot the trade and physical shift for the stocks AAPL, CVX, GS, JPM, MSFT, and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import pickle

# ----------------------------------------------------------------------------


def taq_trade_scale_shift_year_avg_plot(ticker_i, ticker_j, year, taus):
    """Plots the self- and cross-response for a year in trade physical scale.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param taus: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            figure, axs = plt.subplots(2, len(taus), figsize=(16, 6),
                                       sharex='col', sharey='row',
                                       gridspec_kw={'hspace': 0, 'wspace': 0})

            (ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8) = axs

            # Figure with different plots for different taus
            t_ax_1_5 = np.array(range(- 10 * taus[0], 10 * taus[0], 1))
            t_ax_2_6 = np.array(range(- 10 * taus[1], 10 * taus[1], 1))
            t_ax_3_7 = np.array(range(- 10 * taus[2], 10 * taus[2], 1))
            t_ax_4_8 = np.array(range(- 10 * taus[3], 10 * taus[3], 1))

            # Load data
            self_trade_ax1 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[0]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}.pickle' ,'rb'))

            max_pos_ax1 = np.where(max(self_trade_ax1) == self_trade_ax1)[0][0]

            ax1.plot(t_ax_1_5, self_trade_ax1, linewidth=5,
                     label=r'$\tau= %d trades$' % (taus[0]))

            # Plot line in the peak of the figure
            ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                     (0, self_trade_ax1[max_pos_ax1]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax1 - 10 * taus[0]))

            ax1.legend(loc='upper left', fontsize=15)
            ax1.set_ylabel(r'$R^{t}_{ii}(\tau)$', fontsize=15)
            ax1.tick_params(axis='y', labelsize=10)
            ax1.set_ylim(-0.5 * 10**-4, 7 * 10**-4)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(10)
            ax1.grid(True)

            # Load data
            self_trade_ax2 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[1]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}.pickle','rb'))

            max_pos_ax2 = np.where(max(self_trade_ax2) == self_trade_ax2)[0][0]

            ax2.plot(t_ax_2_6, self_trade_ax2, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[1]))

            # Plot line in the peak of the figure
            ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                     (0, self_trade_ax2[max_pos_ax2]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax2 - 10 * taus[1]))

            ax2.legend(loc='upper left', fontsize=15)
            ax2.grid(True)

            # Load data
            self_trade_ax3 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[2]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            max_pos_ax3 = np.where(max(self_trade_ax3) == self_trade_ax3)[0][0]

            ax3.plot(t_ax_3_7, self_trade_ax3, linewidth=5,
                    label=r'$\tau_{seconds} = %d$' % (taus[2]))

            # Plot line in the peak of the figure
            ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                     (0, self_trade_ax3[max_pos_ax3]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax3 - 10 * taus[2]))

            ax3.legend(loc='upper left', fontsize=15)
            ax3.grid(True)

            # Load data
            self_trade_ax4 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[3]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            max_pos_ax4 = np.where(max(self_trade_ax4) == self_trade_ax4)[0][0]

            ax4.plot(t_ax_4_8, self_trade_ax4, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[3]))

            # Plot line in the peak of the figure
            ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                    (0, self_trade_ax4[max_pos_ax4]), '--',
                    label=r'Max $t$ = {} trades'
                    .format(max_pos_ax4 - 10 * taus[3]))

            ax4.legend(loc='upper left', fontsize=15)
            ax4.grid(True)

            # Load data
            cross_trade_ax5 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[0]}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax5 = np.where(max(cross_trade_ax5)
                                   == cross_trade_ax5)[0][0]

            ax5.plot(t_ax_1_5, cross_trade_ax5, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[0]))
            # Plot line in the peak of the figure
            ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                     (0, cross_trade_ax5[max_pos_ax5]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax5 - 10 * taus[0]))
            ax5.legend(loc='upper left', fontsize=15)
            ax5.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax5.set_ylabel(r'$R^{t}_{ij}(\tau)$', fontsize=15)
            ax5.tick_params(axis='x', labelsize=10)
            ax5.tick_params(axis='y', labelsize=10)
            ax5.set_ylim(-0.025 * 10**-4, 3 * 10**-4)
            ax5.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax5.yaxis.offsetText.set_fontsize(0)
            ax5.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax5.grid(True)

            # Load data
            cross_trade_ax6 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[1]}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax6 = np.where(max(cross_trade_ax6)
                                   == cross_trade_ax6)[0][0]

            ax6.plot(t_ax_2_6, cross_trade_ax6, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[1]))
            # Plot line in the peak of the figure
            ax6.plot((t_ax_2_6[max_pos_ax6], t_ax_2_6[max_pos_ax6]),
                     (0, cross_trade_ax6[max_pos_ax6]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax6 - 10 * taus[1]))
            ax6.legend(loc='upper left', fontsize=15)
            ax6.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax6.tick_params(axis='x', labelsize=10)
            ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax6.grid(True)

            # Load data
            cross_trade_ax7 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data'
                + f'_{year}/taq_cross_response_year_trade_shift_data_tau_{taus[2]}'
                + f'/taq_cross_response_year_trade_shift_data_tau_{taus[2]}'
                + f'_{year}_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax7 = np.where(max(cross_trade_ax7)
                                   == cross_trade_ax7)[0][0]

            ax7.plot(t_ax_3_7, cross_trade_ax7, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[2]))
            # Plot line in the peak of the figure
            ax7.plot((t_ax_3_7[max_pos_ax7], t_ax_3_7[max_pos_ax7]),
                    (0, cross_trade_ax7[max_pos_ax7]),
                    '--', label=r'Max $t$ = {} trades'
                    .format(max_pos_ax7 - 10 * taus[2]))
            ax7.legend(loc='upper left', fontsize=15)
            ax7.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax7.tick_params(axis='x', labelsize=10)
            ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax7.grid(True)

            # Load data
            cross_trade_ax8 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[3]}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax8 = np.where(max(cross_trade_ax8)
                                   == cross_trade_ax8)[0][0]

            ax8.plot(t_ax_4_8, cross_trade_ax8, linewidth=5,
                    label=r'$\tau = %d trades$' % (taus[3]))
            # Plot line in the peak of the figure
            ax8.plot((t_ax_4_8[max_pos_ax8], t_ax_4_8[max_pos_ax8]),
                     (0, cross_trade_ax8[max_pos_ax8]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax8 - 10 * taus[3]))
            ax8.legend(loc='upper left', fontsize=15)
            ax8.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax8.tick_params(axis='x', labelsize=10)
            ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax8.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig('../plot/04_shift_trade.png')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_physical_scale_shift_year_avg_plot(ticker_i, ticker_j, year,
                                       taus):
    """Plots the self- and cross-response for a year in second physical scale.

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
            figure, axs = plt.subplots(2, len(taus), figsize=(16, 6),
                                       sharex='col', sharey='row',
                                       gridspec_kw={'hspace': 0, 'wspace': 0})

            (ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8) = axs

            # Figure with different plots for different taus
            t_ax_1_5 = np.array(range(- 10 * taus[0], 10 * taus[0], 1))
            t_ax_2_6 = np.array(range(- 10 * taus[1], 10 * taus[1], 1))
            t_ax_3_7 = np.array(range(- 10 * taus[2], 10 * taus[2], 1))
            t_ax_4_8 = np.array(range(- 10 * taus[3], 10 * taus[3], 1))

            # Load data
            self_physical_ax1 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[0]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}.pickle','rb'))

            max_pos_ax1 = np.where(max(self_physical_ax1)
                                   == self_physical_ax1)[0][0]

            ax1.plot(t_ax_1_5, self_physical_ax1, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[0]))

            # Plot line in the peak of the figure
            ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                     (0, self_physical_ax1[max_pos_ax1]), '--',
                     label=r'Max $t$ = {} s'
                     .format(max_pos_ax1 - 10 * taus[0]))

            ax1.legend(loc='upper left', fontsize=15)
            ax1.set_ylabel(r'$R^{p}_{ii}(\tau)$', fontsize=15)
            ax1.tick_params(axis='y', labelsize=10)
            ax1.set_ylim(-0.5 * 10**-4, 8 * 10**-4)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(10)
            ax1.grid(True)

            # Load data
            self_physical_ax2 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[1]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            max_pos_ax2 = np.where(max(self_physical_ax2)
                                   == self_physical_ax2)[0][0]

            ax2.plot(t_ax_2_6, self_physical_ax2, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[1]))

            # Plot line in the peak of the figure
            ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                     (0, self_physical_ax2[max_pos_ax2]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax2 - 10 * taus[1]))

            ax2.legend(loc='upper left', fontsize=15)
            ax2.grid(True)

            # Load data
            self_physical_ax3 = pickle.load(open(''.join((
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[2]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax3 = np.where(max(self_physical_ax3)
                                   == self_physical_ax3)[0][0]

            ax3.plot(t_ax_3_7, self_physical_ax3, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[2]))

            # Plot line in the peak of the figure
            ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                     (0, self_physical_ax3[max_pos_ax3]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax3 - 10 * taus[2]))

            ax3.legend(loc='upper left', fontsize=15)
            ax3.grid(True)

            # Load data
            self_physical_ax4 = pickle.load(open(''.join((
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[3]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            max_pos_ax4 = np.where(max(self_physical_ax4)
                                   == self_physical_ax4)[0][0]

            ax4.plot(t_ax_4_8, self_physical_ax4, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[3]))

            # Plot line in the peak of the figure
            ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                     (0, self_physical_ax4[max_pos_ax4]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax4 - 10 * taus[3]))

            ax4.legend(loc='upper left', fontsize=15)
            ax4.grid(True)

            # Load data
            cross_physical_ax5 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[0]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax5 = np.where(max(cross_physical_ax5)
                                   == cross_physical_ax5)[0][0]

            ax5.plot(t_ax_1_5, cross_physical_ax5, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[0]))
            # Plot line in the peak of the figure
            ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                     (0, cross_physical_ax5[max_pos_ax5]),
                     '--', label=r'Max $t$ = {}s'
                     .format(max_pos_ax5 - 10 * taus[0]))
            ax5.legend(loc='upper left', fontsize=15)
            ax5.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax5.set_ylabel(r'$R^{p}_{ij}(\tau)$', fontsize=15)
            ax5.tick_params(axis='x', labelsize=10)
            ax5.tick_params(axis='y', labelsize=10)
            ax5.set_ylim(-0.025 * 10**-4, 4.5 * 10**-4)
            ax5.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax5.yaxis.offsetText.set_fontsize(0)
            ax5.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax5.grid(True)

            # Load data
            cross_physical_ax6 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[1]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax6 = np.where(max(cross_physical_ax6)
                                   == cross_physical_ax6)[0][0]

            ax6.plot(t_ax_2_6, cross_physical_ax6, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[1]))
            # Plot line in the peak of the figure
            ax6.plot((t_ax_2_6[max_pos_ax6], t_ax_2_6[max_pos_ax6]),
                     (0, cross_physical_ax6[max_pos_ax6]),
                     '--', label=r'Max $t$ = {}s'
                     .format(max_pos_ax6 - 10 * taus[1]))
            ax6.legend(loc='upper left', fontsize=15)
            ax6.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax6.tick_params(axis='x', labelsize=10)
            ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax6.grid(True)

            # Load data
            cross_physical_ax7 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[2]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax7 = np.where(max(cross_physical_ax7)
                                   == cross_physical_ax7)[0][0]

            ax7.plot(t_ax_3_7, cross_physical_ax7, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[2]))
            # Plot line in the peak of the figure
            ax7.plot((t_ax_3_7[max_pos_ax7], t_ax_3_7[max_pos_ax7]),
                     (0, cross_physical_ax7[max_pos_ax7]),
                     '--', label=r'Max $t$ = {}s'
                     .format(max_pos_ax7 - 10 * taus[2]))
            ax7.legend(loc='upper left', fontsize=15)
            ax7.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax7.tick_params(axis='x', labelsize=10)
            ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax7.grid(True)

            # Load data
            cross_physical_ax8 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[3]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            max_pos_ax8 = np.where(max(cross_physical_ax8)
                                   == cross_physical_ax8)[0][0]

            ax8.plot(t_ax_4_8, cross_physical_ax8, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[3]))
            # Plot line in the peak of the figure
            ax8.plot((t_ax_4_8[max_pos_ax8], t_ax_4_8[max_pos_ax8]),
                     (0, cross_physical_ax8[max_pos_ax8]),
                     '--', label=r'Max $t$ = {}s'
                     .format(max_pos_ax8 - 10 * taus[3]))
            ax8.legend(loc='upper left', fontsize=15)
            ax8.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax8.tick_params(axis='x', labelsize=10)
            ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax8.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig('../plot/04_shift_physical.png')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_scale_responses_year_avg_shift_plot(ticker_i, ticker_j, year,
                                                  shifts):
    """Plots the responses average for a year with trade physical shifts.

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
            self_trade = pickle.load(open(''.join((
                '../../project/taq_data/responses_trade_shift_data'
                + '_{1}/taq_self_response_year_responses_trade'
                + '_shift_data_shift_{2}/taq_self_response_year'
                + '_responses_trade_shift_data_shift_{2}_{1}_{0}'
                + '.pickle').split())
                .format(ticker_i, year, shift), 'rb'))

            ax1.semilogx(self_trade, linewidth=5, label='Shift {} s'
                         .format(shift))

            cross_trade = pickle.load(open(''.join((
                '../../project/taq_data/responses_trade_shift_data_{2}/'
                + 'taq_cross_response_year_responses_trade_shift'
                + '_data_shift_{3}/taq_cross_response_year'
                + '_responses_trade_shift_data_shift_{3}_{2}_{0}i'
                + '_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, shift),
                'rb'))

            ax2.semilogx(cross_trade, linewidth=5, label='Shift {} s'
                         .format(shift))

        ax1.legend(loc='upper left', fontsize=20)
        ax1.set_title('{}'.format(ticker_i), fontsize=40)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax1.set_ylabel(r'$R^{trades}_{ii}(\tau)$', fontsize=20)
        ax1.set_xlim(1, 10000)
        # ax1.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        ax2.legend(loc='upper left', fontsize=20)
        ax2.set_title('{} - {}'.format(ticker_i, ticker_j), fontsize=40)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax2.set_ylabel(r'$R^{trades}_{ij}(\tau)$', fontsize=20)
        ax2.set_xlim(1, 10000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_responses_trades.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_physical_scale_responses_year_avg_shift_plot(tickers, sectors, year,
                                                     shifts):
    """Plots the average of the responses average for a year for each shift.

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
        figure, axs = plt.subplots(2, 2, figsize=(16, 6), sharex='col',
                                   sharey='row',
                                   gridspec_kw={'hspace': 0, 'wspace': 0})

        (ax1, ax2) , (ax3, ax4) = axs

        # Figure with different plots for different shifts

        avg_val_self_1 = np.zeros(1000)
        avg_val_self_2 = np.zeros(1000)
        avg_val_cross_1 = np.zeros(1000)
        avg_val_cross_2 = np.zeros(1000)

        for ticker in tickers:

            # Load data
            self_physical_1 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_self_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[0]}/taq_self_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[0]}_{year}'
                + f'_{ticker}.pickle', 'rb'))

            ax1.semilogx(self_physical_1, linewidth=3, alpha=0.3,
                        label=f'Shift {shifts[0]}s')
            avg_val_self_1 += self_physical_1

            # Load data
            self_physical_2 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_self_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[1]}/taq_self_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[1]}_{year}'
                + f'_{ticker}.pickle', 'rb'))

            ax2.semilogx(self_physical_2, linewidth=3, alpha=0.3,
                        label=f'Shift {shifts[1]}s')
            avg_val_self_2 += self_physical_2

        for sector in sectors:

            # Load data
            cross_physical_1 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_cross_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[0]}/taq_cross_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[0]}_{year}'
                + f'_{sector[0]}i_{sector[1]}j.pickle', 'rb'))

            ax3.semilogx(cross_physical_1, linewidth=5, alpha=0.3,
                        label=f'Shift {shifts[0]}s')
            avg_val_cross_1 += cross_physical_1

            # Load data
            cross_physical_2 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_cross_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[1]}/taq_cross_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[1]}_{year}'
                + f'_{sector[0]}i_{sector[1]}j.pickle', 'rb'))

            ax4.semilogx(cross_physical_2, linewidth=5, alpha=0.3,
                        label=f'Shift {shifts[1]}s')
            avg_val_cross_2 += cross_physical_2

        ax1.semilogx(avg_val_self_1, linewidth=5, label=f'Average')
        ax1.set_ylabel(r'$R^{p}_{ii}(\tau)$', fontsize=15)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        ax2.semilogx(avg_val_self_2, linewidth=5, label=f'Average')
        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                fontsize=15)
        ax2.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.grid(True)

        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                fontsize=15)
        ax3.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax3.set_ylabel(r'$R^{p}_{ij}(\tau)$', fontsize=15)
        ax3.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax3.tick_params(axis='x', labelsize=10)
        ax3.tick_params(axis='y', labelsize=10)
        ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.yaxis.offsetText.set_fontsize(0)
        ax3.grid(True)

        ax4.semilogx(avg_val_cross_2, linewidth=5, label=f'Average')
        ax4.set_xlabel(r'$\tau \, [s]$', fontsize=20)
        ax4.set_xlim(1, 1000)
        # ax4.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax4.tick_params(axis='x', labelsize=10)
        ax4.tick_params(axis='y', labelsize=10)
        ax4.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax4.yaxis.offsetText.set_fontsize(0)
        ax4.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_responses_physical.png')

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
    tickers = ['AAPL', 'MSFT', 'GS', 'JPM', 'XOM', 'CVX']
    sectors = [('AAPL', 'MSFT'), ('MSFT', 'AAPL'),
               ('GS', 'JPM'), ('JPM', 'GS'),
               ('CVX', 'XOM'), ('XOM', 'CVX')]
    year = '2008'

    taq_trade_scale_shift_year_avg_plot('GS', 'JPM', year, taus)
    taq_physical_scale_shift_year_avg_plot('GS', 'JPM', year, taus)
    taq_physical_scale_responses_year_avg_shift_plot(tickers, sectors, year,
                                                     [10,100])

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
