'''
Script to plot the TAQ time shift response ind a different format from the
orginal implementation.

Juan Camilo Henao Londono
AG Guhr - Universität Duisburg-Essen
17.07.19
'''

# Modules
from matplotlib import pyplot as plt
import numpy as np
import pickle

__tau__ = 10000


def taq_self_response_year_avg_time_shift_plot(ticker, year, taus):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param taus: list with the values of taus (i.e. [1, 2])
    """

    figure = plt.figure(figsize=(16, 9))

    for tau_idx, tau_val in enumerate(taus):

        ax = plt.subplot(len(taus) // 2, 2, tau_idx + 1)

        times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))
        self_ = pickle.load(open(''.join((
                            '../../taq_data/time_shift_data_{1}/taq_self'
                            + '_response_year_time_shift_data_tau_{2}/taq'
                            + '_self_response_year_time_shift_data_tau_{2}'
                            + '_{1}_{0}.pickle').split())
                            .format(ticker, year, tau_val), 'rb'))

        max_pos = np.where(max(self_) == self_)[0][0]

        ax.plot(times, self_, linewidth=5, label=r'{}'.format(ticker))
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


    plt.savefig('../taq_plot/taq_self_response_year_avg_time_shift_plot_{}_{}.png'
                .format(year, ticker))
    return None


def taq_cross_response_year_avg_time_shift_plot(ticker_i, ticker_j, year,
                                                taus):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param taus: list with the values of taus (i.e. [1, 2])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(16, 9))

        for tau_idx, tau_val in enumerate(taus):

            ax = plt.subplot(len(taus) // 2, 2, tau_idx + 1)

            times = np.array(range(- 10 * tau_val, 10 * tau_val, 1))
            cross = pickle.load(open(''.join((
                                '../../taq_data/time_shift_data_{2}/taq'
                                + '_cross_response_year_time_shift_data_tau'
                                + '_{3}/taq_cross_response_year_time_shift'
                                + '_data_tau_{3}_{2}_{0}i_{1}j.pickle')
                                .split())
                                .format(ticker_i, ticker_j, year, tau_val),
                                'rb'))

            max_pos = np.where(max(cross) == cross)[0][0]

            ax.plot(times, cross, linewidth=5, label=r'{} - {}'
                    .format(ticker_i, ticker_j))
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

        plt.savefig('../taq_plot/taq_cross_response_year_avg_time_shift_plot_{}_{}_{}.png'
                    .format(year, ticker_i, ticker_j))
        return None


def taq_cross_response_year_avg_heat_map_responses_time_shift_plot(ticker_i,
                                                                   ticker_j,
                                                                   year,
                                                                   shifts):
    """
    Plot the average cross response during a month and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param shifts: list with the values of shifts (i. e. [1, 2])
    """

    if (ticker_i == ticker_j):

        return None

    else:


        figure = plt.figure(figsize=(16, 9))

        ax1 = plt.subplot(1, 2, 1)

        for shift in shifts:

            cross = pickle.load(open(''.join((
                            '../../taq_data/responses_time_shift_data_{2}/'
                            + 'taq_cross_response_year_responses_time'
                            + '_shift_data_shift_{3}/taq_cross_response'
                            + '_year_responses_time_shift_data_shift_{3}'
                            + '_{2}_{0}i_{1}j.pickle').split())
                            .format(ticker_i, ticker_j, year, shift),
                            'rb'))


            ax1.semilogx(cross, linewidth=5, label='Shift {} s'
                            .format(shift))

        ax1.legend(loc='best', fontsize=15)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=25)
        ax1.set_ylabel(r'$R_{ij}(\tau)$', fontsize=25)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.grid(True)


        ax2 = plt.subplot(1, 2, 2)

        # Generate two 2D grids for the x and y bounds
        x, y = np.meshgrid(range(__tau__), range(len(shifts) + 1))
        z = []

        for shift in shifts:

            z.append(pickle.load(open(''.join((
                                    '../../taq_data/responses_time_shift_data_{2}/'
                                    + 'taq_cross_response_year_responses_time'
                                    + '_shift_data_shift_{3}/taq_cross_response'
                                    + '_year_responses_time_shift_data_shift_{3}'
                                    + '_{2}_{0}i_{1}j.pickle').split())
                                    .format(ticker_i, ticker_j, year, shift),
                                    'rb')))

            z_min, z_max = np.amin(z), np.amax(z)

        c = ax2.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)

        # set the limits of the plot to the limits of the data
        tick_pos = [0.5 + i for i in range(len(shifts))]
        plt.xticks(fontsize=15)
        plt.yticks(tick_pos, shifts, fontsize=15)
        plt.xlabel(r'$\tau \, [s]$', fontsize=25)
        plt.ylabel('Time shift $[s]$', fontsize=25)
        cbar = figure.colorbar(c, ax=ax2)
        ax2.set_xscale('symlog')
        cbar.set_label('Cross-responses values', fontsize=25)
        cbar.ax.tick_params(labelsize=15)
        cbar.formatter.set_powerlimits((0, 0))
        cbar.update_ticks

        plt.tight_layout()


        plt.savefig('../taq_plot/taq_cross_response_year_avg_heat_map_responses_time_shift_plot.png')

def main():

    tickers = ['AAPL', 'MSFT']
    year = '2008'
    taus = [1, 10, 100, 1000]
    shifts = [1, 5, 10, 50, 100, 500, 1000, 5000]

    for ticker in tickers:
        taq_self_response_year_avg_time_shift_plot(ticker, year, taus)

    taq_cross_response_year_avg_time_shift_plot(tickers[0], tickers[1], year, taus)
    taq_cross_response_year_avg_heat_map_responses_time_shift_plot(tickers[0], tickers[1], year, shifts)

if __name__ == "__main__":
    main()