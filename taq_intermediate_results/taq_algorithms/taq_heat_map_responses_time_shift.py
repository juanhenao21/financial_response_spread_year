'''
Script to plot a heat map with the responses of different time shifts.

Juan Camilo Henao Londono
AG Guhr - Universität Duisburg-Essen
16.07.19
'''

# Modules
from matplotlib import pyplot as plt
import numpy as np
import pickle

__tau__ = 10000


def taq_heat_map_self_responses_time_shift_plot(ticker, year, shifts):
    """
    Plot the heat map of the TAQ self responses with time shift.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e. '2008')
        :param shifts: list with the values of the time shifts. (i.e. [1, 2])
    """

    # Generate two 2D grids for the x and y bounds
    x, y = np.meshgrid(range(__tau__), range(len(shifts) + 1))
    z = []

    for shift in shifts:

        z.append(pickle.load(open(''.join((
                                '../taq_data/responses_time_shift_data_{1}'
                                + '/taq_self_response_year_responses_time'
                                + '_shift_data_shift_{2}/taq_self_response'
                                + '_year_responses_time_shift_data_shift'
                                + '_{2}_{1}_{0}.pickle').split())
                                .format(ticker, year, shift), 'rb')))

        z_min, z_max = np.amin(z), np.amax(z)

    fig, ax = plt.subplots()
    c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
    ax.set_title('Self-responses {}'.format(ticker), fontsize=35)
    # set the limits of the plot to the limits of the data
    tick_pos = [0.5 + i for i in range(len(shifts))]
    plt.xticks(fontsize=15)
    plt.yticks(tick_pos, shifts, fontsize=15)
    plt.xlabel(r'$\tau \, [s]$', fontsize=25)
    plt.ylabel('Time shift $[s]$', fontsize=25)
    cbar = fig.colorbar(c, ax=ax)
    ax.set_xscale('symlog')
    cbar.set_label('Self-responses values', fontsize=25)
    cbar.ax.tick_params(labelsize=15)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks

    plt.show()

    return None


def taq_heat_map_cross_responses_time_shift_plot(ticker_i, ticker_j, year, shifts):
    """
    Plot the heat map of the TAQ cross responses with time shift.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e. '2008')
        :param shifts: list with the values of the time shifts. (i.e. [1, 2])
    """

    # Generate two 2D grids for the x and y bounds
    x, y = np.meshgrid(range(__tau__), range(len(shifts) + 1))
    z = []

    for shift in shifts:

        z.append(pickle.load(open(''.join((
                                '../taq_data/responses_time_shift_data_{2}/'
                                + 'taq_cross_response_year_responses_time'
                                + '_shift_data_shift_{3}/taq_cross_response'
                                + '_year_responses_time_shift_data_shift_{3}'
                                + '_{2}_{0}i_{1}j.pickle').split())
                                .format(ticker_i, ticker_j, year, shift),
                                'rb')))

        z_min, z_max = np.amin(z), np.amax(z)

    fig, ax = plt.subplots()
    c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
    ax.set_title('Cross-responses {} - {}'.format(ticker_i, ticker_j),
                 fontsize=35)
    # set the limits of the plot to the limits of the data
    tick_pos = [0.5 + i for i in range(len(shifts))]
    plt.xticks(fontsize=15)
    plt.yticks(tick_pos, shifts, fontsize=15)
    plt.xlabel(r'$\tau \, [s]$', fontsize=25)
    plt.ylabel('Time shift $[s]$', fontsize=25)
    cbar = fig.colorbar(c, ax=ax)
    ax.set_xscale('symlog')
    cbar.set_label('Cross-responses values', fontsize=25)
    cbar.ax.tick_params(labelsize=15)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks

    plt.show()

    return None


def main():

    tickers = ['AAPL', 'MSFT']
    year = '2008'
    shifts = [1, 5, 10, 50, 100, 500, 1000, 5000]

    taq_heat_map_self_responses_time_shift_plot(tickers[0], year, shifts)
    taq_heat_map_self_responses_time_shift_plot(tickers[1], year, shifts)
    taq_heat_map_cross_responses_time_shift_plot(tickers[0], tickers[1],
                                            year, shifts)
    taq_heat_map_cross_responses_time_shift_plot(tickers[1], tickers[0],
                                            year, shifts)

    return None

if __name__ == "__main__":
    main()
