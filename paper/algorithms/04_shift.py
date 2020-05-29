'''TAQ trade and physical shift figures

Plots the figures of the trade and physical shift implementation for the paper.

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle

The module contains the following functions:
    * taq_trade_scale_shift_year_avg_plot - plots the shift for a year in trade
      time scale.
    * taq_physical_scale_shift_year_avg_plot - plots the shift for a year in
      physical time scale.
    * taq_trade_scale_responses_year_avg_shift_plot - plots the shifted
      response for a year in trade time scale.
    * taq_physical_scale_responses_year_avg_shift_plot - plots the shifted
      response for a year in physical time scale.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import pickle

# ----------------------------------------------------------------------------


def taq_trade_scale_shift_year_avg_plot(ticker_i, ticker_j, year, taus):
    """Plots the shift in self- and cross-response for a year in trade physical
       scale.

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
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_trade_ax1) == self_trade_ax1)[0]:
                max_pos_ax1 = np.where(max(self_trade_ax1)
                                    == self_trade_ax1)[0][0]
            else:
                max_pos_ax1 = 0

            ax1.plot(t_ax_1_5, self_trade_ax1, linewidth=5,
                     label=r'$\tau= %d$ trade' % (taus[0]))

            # Plot line in the peak of the figure
            ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                     (0, self_trade_ax1[max_pos_ax1]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax1 - 10 * taus[0]))

            ax1.legend(loc='upper left', fontsize=15)
            ax1.set_ylabel(r'$R^{s,t}_{ii}(\tau)$', fontsize=15)
            ax1.tick_params(axis='y', labelsize=10)
            ax1.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(10)
            ax1.grid(True)

            # Load data
            self_trade_ax2 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[1]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_trade_ax2) == self_trade_ax2)[0]:
                max_pos_ax2 = np.where(max(self_trade_ax2)
                                    == self_trade_ax2)[0][0]
            else:
                max_pos_ax2 = 0

            ax2.plot(t_ax_2_6, self_trade_ax2, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[1]))

            # Plot line in the peak of the figure
            ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                     (0, self_trade_ax2[max_pos_ax2]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax2 - 10 * taus[1]))

            ax2.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax2.legend(loc='upper left', fontsize=15)
            ax2.grid(True)

            # Load data
            self_trade_ax3 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[2]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_trade_ax3) == self_trade_ax3)[0]:
                max_pos_ax3 = np.where(max(self_trade_ax3)
                                    == self_trade_ax3)[0][0]
            else:
                max_pos_ax3 = 0

            ax3.plot(t_ax_3_7, self_trade_ax3, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[2]))

            # Plot line in the peak of the figure
            ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                     (0, self_trade_ax3[max_pos_ax3]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax3 - 10 * taus[2]))

            ax3.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax3.legend(loc='upper left', fontsize=15)
            ax3.grid(True)

            # Load data
            self_trade_ax4 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[3]}/taq_self'
                + f'_response_year_trade_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_trade_ax4) == self_trade_ax4)[0]:
                max_pos_ax4 = np.where(max(self_trade_ax4)
                                    == self_trade_ax4)[0][0]
            else:
                max_pos_ax4 = 0

            ax4.plot(t_ax_4_8, self_trade_ax4, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[3]))

            # Plot line in the peak of the figure
            ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                     (0, self_trade_ax4[max_pos_ax4]), '--',
                     label=r'Max $t$ = {} trades'
                     .format(max_pos_ax4 - 10 * taus[3]))

            ax4.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax4.legend(loc='upper left', fontsize=15)
            ax4.grid(True)

            # Load data
            cross_trade_ax5 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[0]}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_trade_ax5) == cross_trade_ax5)[0]:
                max_pos_ax5 = np.where(max(cross_trade_ax5)
                                    == cross_trade_ax5)[0][0]
            else:
                max_pos_ax5 = 0

            ax5.plot(t_ax_1_5, cross_trade_ax5, linewidth=5,
                     label=r'$\tau = %d$ trade' % (taus[0]))
            # Plot line in the peak of the figure
            ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                     (0, cross_trade_ax5[max_pos_ax5]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax5 - 10 * taus[0]))
            ax5.legend(loc='upper left', fontsize=15)
            ax5.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax5.set_ylabel(r'$R^{s,t}_{ij}(\tau)$', fontsize=15)
            ax5.tick_params(axis='x', labelsize=10)
            ax5.tick_params(axis='y', labelsize=10)
            ax5.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
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

            if np.where(max(cross_trade_ax6) == cross_trade_ax6)[0]:
                max_pos_ax6 = np.where(max(cross_trade_ax6)
                                    == cross_trade_ax6)[0][0]
            else:
                max_pos_ax6 = 0

            ax6.plot(t_ax_2_6, cross_trade_ax6, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[1]))
            # Plot line in the peak of the figure
            ax6.plot((t_ax_2_6[max_pos_ax6], t_ax_2_6[max_pos_ax6]),
                     (0, cross_trade_ax6[max_pos_ax6]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax6 - 10 * taus[1]))
            ax6.legend(loc='upper left', fontsize=15)
            ax6.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax6.tick_params(axis='x', labelsize=10)
            ax6.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax6.grid(True)

            # Load data
            cross_trade_ax7 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data'
                + f'_{year}/taq_cross_response_year_trade_shift_data_tau'
                + f'_{taus[2]}/taq_cross_response_year_trade_shift_data_tau'
                + f'_{taus[2]}_{year}_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_trade_ax7) == cross_trade_ax7)[0]:
                max_pos_ax7 = np.where(max(cross_trade_ax7)
                                    == cross_trade_ax7)[0][0]
            else:
                max_pos_ax7 = 0

            ax7.plot(t_ax_3_7, cross_trade_ax7, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[2]))
            # Plot line in the peak of the figure
            ax7.plot((t_ax_3_7[max_pos_ax7], t_ax_3_7[max_pos_ax7]),
                     (0, cross_trade_ax7[max_pos_ax7]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax7 - 10 * taus[2]))
            ax7.legend(loc='upper left', fontsize=15)
            ax7.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax7.tick_params(axis='x', labelsize=10)
            ax7.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax7.grid(True)

            # Load data
            cross_trade_ax8 = pickle.load(open(
                f'../../project/taq_data/trade_shift_data_{year}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[3]}/taq_cross'
                + f'_response_year_trade_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_trade_ax8) == cross_trade_ax8)[0]:
                max_pos_ax8 = np.where(max(cross_trade_ax8)
                                    == cross_trade_ax8)[0][0]
            else:
                max_pos_ax8 = 0

            ax8.plot(t_ax_4_8, cross_trade_ax8, linewidth=5,
                     label=r'$\tau = %d$ trades' % (taus[3]))
            # Plot line in the peak of the figure
            ax8.plot((t_ax_4_8[max_pos_ax8], t_ax_4_8[max_pos_ax8]),
                     (0, cross_trade_ax8[max_pos_ax8]),
                     '--', label=r'Max $t$ = {} trades'
                     .format(max_pos_ax8 - 10 * taus[3]))
            ax8.legend(loc='upper left', fontsize=15)
            ax8.set_xlabel(r'Trade shift [trades]', fontsize=15)
            ax8.tick_params(axis='x', labelsize=10)
            ax8.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax8.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig(f'../plot/04_shift_trade_{ticker_i}_{ticker_j}.png')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_physical_scale_shift_year_avg_plot(ticker_i, ticker_j, year, taus):
    """Plots the shift in self- and cross-response for a year in second
       physical scale.

    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL')
    :param year: string of the year to be analyzed (i.e '2008')
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
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_physical_ax1) == self_physical_ax1)[0]:
                max_pos_ax1 = np.where(max(self_physical_ax1)
                                    == self_physical_ax1)[0][0]
            else:
                max_pos_ax1 = 0

            ax1.plot(t_ax_1_5, self_physical_ax1, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[0]))

            # Plot line in the peak of the figure
            ax1.plot((t_ax_1_5[max_pos_ax1], t_ax_1_5[max_pos_ax1]),
                     (0, self_physical_ax1[max_pos_ax1]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax1 - 10 * taus[0]))

            ax1.legend(loc='upper left', fontsize=15)
            ax1.set_ylabel(r'$R^{s,p}_{ii}(\tau)$', fontsize=15)
            ax1.tick_params(axis='y', labelsize=10)
            ax1.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(10)
            ax1.grid(True)

            # Load data
            self_physical_ax2 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[1]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[1]}_{year}'
                + f'_{ticker_i}.pickle', 'rb'))

            if np.where(max(self_physical_ax2) == self_physical_ax2)[0]:
                max_pos_ax2 = np.where(max(self_physical_ax2)
                                    == self_physical_ax2)[0][0]
            else:
                max_pos_ax2 = 0

            ax2.plot(t_ax_2_6, self_physical_ax2, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[1]))

            # Plot line in the peak of the figure
            ax2.plot((t_ax_2_6[max_pos_ax2], t_ax_2_6[max_pos_ax2]),
                     (0, self_physical_ax2[max_pos_ax2]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax2 - 10 * taus[1]))

            ax2.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax2.legend(loc='upper left', fontsize=15)
            ax2.grid(True)

            # Load data
            self_physical_ax3 = pickle.load(open(''.join((
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[2]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            if np.where(max(self_physical_ax3) == self_physical_ax3)[0]:
                max_pos_ax3 = np.where(max(self_physical_ax3)
                                    == self_physical_ax3)[0][0]
            else:
                max_pos_ax3 = 0

            ax3.plot(t_ax_3_7, self_physical_ax3, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[2]))

            # Plot line in the peak of the figure
            ax3.plot((t_ax_3_7[max_pos_ax3], t_ax_3_7[max_pos_ax3]),
                     (0, self_physical_ax3[max_pos_ax3]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax3 - 10 * taus[2]))

            ax3.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax3.legend(loc='upper left', fontsize=15)
            ax3.grid(True)

            # Load data
            self_physical_ax4 = pickle.load(open(''.join((
                f'../../project/taq_data/physical_shift_data_{year}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[3]}/taq_self'
                + f'_response_year_physical_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}.pickle').split()), 'rb'))

            if np.where(max(self_physical_ax4) == self_physical_ax4)[0]:
                max_pos_ax4 = np.where(max(self_physical_ax4)
                                    == self_physical_ax4)[0][0]
            else:
                max_pos_ax4 = 0

            ax4.plot(t_ax_4_8, self_physical_ax4, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[3]))

            # Plot line in the peak of the figure
            ax4.plot((t_ax_4_8[max_pos_ax4], t_ax_4_8[max_pos_ax4]),
                     (0, self_physical_ax4[max_pos_ax4]), '--',
                     label=r'Max $t$ = {}s'
                     .format(max_pos_ax4 - 10 * taus[3]))

            ax4.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax4.legend(loc='upper left', fontsize=15)
            ax4.grid(True)

            # Load data
            cross_physical_ax5 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[0]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[0]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_physical_ax5) == cross_physical_ax5)[0]:
                max_pos_ax5 = np.where(max(cross_physical_ax5)
                                    == cross_physical_ax5)[0][0]
            else:
                max_pos_ax5 = 0

            ax5.plot(t_ax_1_5, cross_physical_ax5, linewidth=5,
                     label=r'$\tau = %d s$' % (taus[0]))
            # Plot line in the peak of the figure
            ax5.plot((t_ax_1_5[max_pos_ax5], t_ax_1_5[max_pos_ax5]),
                     (0, cross_physical_ax5[max_pos_ax5]),
                     '--', label=r'Max $t$ = {}s'
                     .format(max_pos_ax5 - 10 * taus[0]))
            ax5.legend(loc='upper left', fontsize=15)
            ax5.set_xlabel(r'Time shift $[s]$', fontsize=15)
            ax5.set_ylabel(r'$R^{s,p}_{ij}(\tau)$', fontsize=15)
            ax5.tick_params(axis='x', labelsize=10)
            ax5.tick_params(axis='y', labelsize=10)
            ax5.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
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

            if np.where(max(cross_physical_ax6) == cross_physical_ax6)[0]:
                max_pos_ax6 = np.where(max(cross_physical_ax6)
                                    == cross_physical_ax6)[0][0]
            else:
                max_pos_ax6 = 0

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
            ax6.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax6.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax6.grid(True)

            # Load data
            cross_physical_ax7 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[2]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[2]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_physical_ax7) == cross_physical_ax7)[0]:
                max_pos_ax7 = np.where(max(cross_physical_ax7)
                                    == cross_physical_ax7)[0][0]
            else:
                max_pos_ax7 = 0

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
            ax7.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax7.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax7.grid(True)

            # Load data
            cross_physical_ax8 = pickle.load(open(
                f'../../project/taq_data/physical_shift_data_{year}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[3]}/taq_cross'
                + f'_response_year_physical_shift_data_tau_{taus[3]}_{year}'
                + f'_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            if np.where(max(cross_physical_ax8) == cross_physical_ax8)[0]:
                max_pos_ax8 = np.where(max(cross_physical_ax8)
                                    == cross_physical_ax8)[0][0]
            else:
                max_pos_ax8 = 0

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
            ax8.set_ylim(-0.5 * 10**-4, 9 * 10**-4)
            ax8.xaxis.set_major_locator(ticker.MaxNLocator(4))
            ax8.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig(f'../plot/04_shift_physical_{ticker_i}_{ticker_j}'
                           + f'.png')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_trade_scale_responses_year_avg_shift_plot(tickers, sectors, year,
                                                  shifts):
    """Plots the average of the responses average for a year for each shift.

    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :param year: string of the year to be analized (i.e. '2008')
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure, axs = plt.subplots(2, 2, figsize=(16, 9), sharex='col',
                                   sharey='row',
                                   gridspec_kw={'hspace': 0, 'wspace': 0})

        (ax1, ax2), (ax3, ax4) = axs

        # Figure with different plots for different shifts

        avg_val_self_1 = np.zeros(1000)
        avg_val_self_2 = np.zeros(1000)
        avg_val_cross_1 = np.zeros(1000)
        avg_val_cross_2 = np.zeros(1000)

        for ticker in tickers:

            # Load data
            self_trade_1 = pickle.load(open(
                f'../../project/taq_data/responses_trade_shift_data'
                + f'_{year}/taq_self_response_year_responses_trade'
                + f'_shift_data_shift_{shifts[0]}/taq_self_response_year'
                + f'_responses_trade_shift_data_shift_{shifts[0]}_{year}'
                + f'_{ticker}.pickle', 'rb'))

            ax1.semilogx(self_trade_1, linewidth=3, alpha=0.3,
                         label=f'{ticker}')
            avg_val_self_1 += self_trade_1

            # Load data
            self_trade_2 = pickle.load(open(
                f'../../project/taq_data/responses_trade_shift_data'
                + f'_{year}/taq_self_response_year_responses_trade'
                + f'_shift_data_shift_{shifts[1]}/taq_self_response_year'
                + f'_responses_trade_shift_data_shift_{shifts[1]}_{year}'
                + f'_{ticker}.pickle', 'rb'))

            ax2.semilogx(self_trade_2, linewidth=3, alpha=0.3,
                         label=f'{ticker}')
            avg_val_self_2 += self_trade_2

        for sector in sectors:

            # Load data
            cross_trade_1 = pickle.load(open(
                f'../../project/taq_data/responses_trade_shift_data'
                + f'_{year}/taq_cross_response_year_responses_trade'
                + f'_shift_data_shift_{shifts[0]}/taq_cross_response_year'
                + f'_responses_trade_shift_data_shift_{shifts[0]}_{year}'
                + f'_{sector[0]}i_{sector[1]}j.pickle', 'rb'))

            ax3.semilogx(cross_trade_1, linewidth=5, alpha=0.3,
                         label=f'{sector[0]} - {sector[1]}')
            avg_val_cross_1 += cross_trade_1

            # Load data
            cross_trade_2 = pickle.load(open(
                f'../../project/taq_data/responses_trade_shift_data'
                + f'_{year}/taq_cross_response_year_responses_trade'
                + f'_shift_data_shift_{shifts[1]}/taq_cross_response_year'
                + f'_responses_trade_shift_data_shift_{shifts[1]}_{year}'
                + f'_{sector[0]}i_{sector[1]}j.pickle', 'rb'))

            ax4.semilogx(cross_trade_2, linewidth=5, alpha=0.3,
                         label=f'{sector[0]} - {sector[1]}')
            avg_val_cross_2 += cross_trade_2

        ax1.semilogx(avg_val_self_1 / len(tickers), '-k', linewidth=5,
                     label=f'Average')
        ax1.legend(loc='upper center', bbox_to_anchor=(1.0, 1.3), ncol=4,
                   fontsize=15)
        ax1.set_ylabel(r'$R^{s,t}_{ii}(\tau)$', fontsize=15)
        ax1.set_xlim(1, 1000)
        ax1.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        ax2.semilogx(avg_val_self_2 / len(tickers), '-k', linewidth=5,
                     label=f'Average')
        ax2.set_xlim(1, 1000)
        ax2.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax2.grid(True)

        ax3.semilogx(avg_val_cross_1 / len(sectors), '-k', linewidth=5,
                     label=f'Average')
        ax3.legend(loc='upper center', bbox_to_anchor=(1.0, -0.2), ncol=4,
                   fontsize=15)
        ax3.set_xlabel(r'$\tau \, [trades]$', fontsize=15)
        ax3.set_ylabel(r'$R^{s,t}_{ij}(\tau)$', fontsize=15)
        ax3.set_xlim(1, 1000)
        ax3.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax3.tick_params(axis='x', labelsize=10)
        ax3.tick_params(axis='y', labelsize=10)
        ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.yaxis.offsetText.set_fontsize(0)
        ax3.grid(True)

        ax4.semilogx(avg_val_cross_2 / len(sectors), '-k', linewidth=5,
                     label=f'Average')
        ax4.set_xlabel(r'$\tau \, [trades]$', fontsize=15)
        ax4.set_xlim(1, 1000)
        ax4.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax4.tick_params(axis='x', labelsize=10)
        ax4.tick_params(axis='y', labelsize=10)
        ax4.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax4.yaxis.offsetText.set_fontsize(0)
        ax4.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig('../plot/04_shift_responses_trade.png')

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

    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :param year: string of the year to be analized (i.e. '2008')
    :param shifts: list of integers greater than zero (i.e. [1, 10, 50]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure, axs = plt.subplots(2, 2, figsize=(16, 9), sharex='col',
                                   sharey='row',
                                   gridspec_kw={'hspace': 0, 'wspace': 0})

        (ax1, ax2), (ax3, ax4) = axs

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
                         label=f'{ticker}')
            avg_val_self_1 += self_physical_1

            # Load data
            self_physical_2 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_self_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[1]}/taq_self_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[1]}_{year}'
                + f'_{ticker}.pickle', 'rb'))

            ax2.semilogx(self_physical_2, linewidth=3, alpha=0.3,
                         label=f'{ticker}')
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
                         label=f'{sector[0]} - {sector[1]}')
            avg_val_cross_1 += cross_physical_1

            # Load data
            cross_physical_2 = pickle.load(open(
                f'../../project/taq_data/responses_physical_shift_data'
                + f'_{year}/taq_cross_response_year_responses_physical'
                + f'_shift_data_shift_{shifts[1]}/taq_cross_response_year'
                + f'_responses_physical_shift_data_shift_{shifts[1]}_{year}'
                + f'_{sector[0]}i_{sector[1]}j.pickle', 'rb'))

            ax4.semilogx(cross_physical_2, linewidth=5, alpha=0.3,
                         label=f'{sector[0]} - {sector[1]}')
            avg_val_cross_2 += cross_physical_2

        ax1.semilogx(avg_val_self_1 / len(tickers), '-k', linewidth=5,
                     label=f'Average')
        ax1.legend(loc='upper center', bbox_to_anchor=(1.0, 1.3), ncol=4,
                   fontsize=15)
        ax1.set_ylabel(r'$R^{s,p}_{ii}(\tau)$', fontsize=15)
        ax1.set_xlim(1, 1000)
        ax1.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        ax2.semilogx(avg_val_self_2 / len(tickers), '-k', linewidth=5,
                     label=f'Average')
        ax2.set_xlim(1, 1000)
        ax2.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax2.grid(True)

        ax3.semilogx(avg_val_cross_1 / len(sectors), '-k', linewidth=5,
                     label=f'Average')
        ax3.legend(loc='upper center', bbox_to_anchor=(1.0, -0.2), ncol=4,
                   fontsize=15)
        ax3.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax3.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
        ax3.set_xlim(1, 1000)
        ax3.set_ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax3.tick_params(axis='x', labelsize=10)
        ax3.tick_params(axis='y', labelsize=10)
        ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.yaxis.offsetText.set_fontsize(0)
        ax3.grid(True)

        ax4.semilogx(avg_val_cross_2 / len(sectors), '-k', linewidth=5,
                     label=f'Average')
        ax4.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax4.set_xlim(1, 1000)
        ax4.set_ylim(-0.5 * 10 ** -4, 10 * 10 ** -4)
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
    tickers = ['GOOG', 'MA', 'CME', 'GS', 'RIG', 'APA']
    sectors = [('GOOG', 'MA'), ('MA', 'GOOG'),
               ('CME', 'GS'), ('GS', 'CME'),
               ('RIG', 'APA'), ('APA', 'RIG')]
    year = '2008'

    for sector in sectors:
        taq_trade_scale_shift_year_avg_plot(sector[0], sector[1], year,
                                            taus)
        taq_physical_scale_shift_year_avg_plot(sector[0], sector[1], year,
                                               taus)

    taq_physical_scale_responses_year_avg_shift_plot(tickers, sectors, year,
                                                     [10, 100])
    taq_trade_scale_responses_year_avg_shift_plot(tickers, sectors, year,
                                                     [10, 100])

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
