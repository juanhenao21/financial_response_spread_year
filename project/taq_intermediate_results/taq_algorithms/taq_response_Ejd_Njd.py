'''TAQ response analysis.

Analize and plot the results of the response of different scales using the
values of $E_{j,d}\left(t\right)$ (sum of the trades in event scale) defined as

$$E_{j,d}\left(t\right)&=\sum_{n=1}^{N\left(t\right)}\varepsilon_{j,d}^{event}
  \left(t,n\right)$$

and $N_{j,d}\left(t\right)$ (number of trades per second).

This script requires the following modules:
    * matplotlib
    * numpy

The module contains the following functions:
    * taq_self_response_year_avg_plot - plots the self-response average for a
      year.
    * taq_cross_response_year_avg_plot - plots the cross-response average for a
      year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import os
import pickle
from itertools import product

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_plot(ticker, year):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        function_name = taq_self_response_year_avg_plot.__name__

        # Load data
        self_time = pickle.load(open(''.join((
                        f'../../taq_data/article_reproduction_data_{year}/taq'
                        + f'_self_response_year_data/taq_self_response_year'
                        + f'_data_{year}_{ticker}.pickle').split()), 'rb'))
        self_event = pickle.load(open(''.join((
                        f'../../taq_data/responses_event_data_{year}/taq_self'
                        + f'_response_year_responses_event_data/taq_self'
                        + f'_response_year_responses_event_data_{year}'
                        + f'_{ticker}.pickle').split()), 'rb'))
        self_activity = pickle.load(open(''.join((
                        f'../../taq_data/responses_time_activity_data_{year}/'
                        + f'taq_self_response_year_responses_time_activity'
                        + f'_data/taq_self_response_year_responses_time'
                        + f'_activity_data_{year}_{ticker}.pickle').split()),
                        'rb'))

        figure = plt.figure(figsize=(16, 9))
        plt.semilogx(self_time, linewidth=5, label=f'Time')
        plt.semilogx(self_event, linewidth=5, label=f'Event')
        plt.semilogx(self_activity, linewidth=5, label=f'Activity')
        plt.legend(loc='best', fontsize=25)
        plt.title(f'Self-response {ticker}', fontsize=40)
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
        plt.savefig(''.join((
            f'../taq_plot/taq_response_comparison/{function_name}_{ticker}'
            + f'.png').split()))

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_plot(ticker_i, ticker_j, year):
    """Plots the cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            function_name = taq_cross_response_year_avg_plot.__name__

            cross_time = pickle.load(open(''.join((
                            f'../../taq_data/article_reproduction_data_{year}'
                            + f'/taq_cross_response_year_data/taq_cross'
                            + f'_response_year_data_{year}_{ticker_i}i'
                            + f'_{ticker_j}j.pickle').split()), 'rb'))
            cross_event = pickle.load(open(''.join((
                            f'../../taq_data/responses_event_data_{year}/taq'
                            + f'_cross_response_year_responses_event_data/taq'
                            + f'_cross_response_year_responses_event_data'
                            + f'_{year}_{ticker_i}i_{ticker_j}j.pickle')
                            .split()), 'rb'))
            cross_activity = pickle.load(open(''.join((
                            f'../../taq_data/responses_time_activity_data'
                            + f'_{year}/taq_cross_response_year_responses_time'
                            + f'_activity_data/taq_cross_response_year'
                            + f'_responses_time_activity_data_{year}'
                            + f'_{ticker_i}i_{ticker_j}j.pickle').split()),
                            'rb'))

            figure = plt.figure(figsize=(16, 9))
            plt.semilogx(cross_time, linewidth=5, label='Time')
            plt.semilogx(cross_event, linewidth=5, label='Event')
            plt.semilogx(cross_activity, linewidth=5, label='Activity')
            plt.legend(loc='best', fontsize=25)
            plt.title(f'Cross-response {ticker_i}-{ticker_j}', fontsize=40)
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
            plt.savefig(''.join((
                f'../taq_plot/taq_response_comparison/{function_name}'
                + f'_{ticker_i}_{ticker_j}.png').split()))

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

    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']

    ticker = 'AAPL'
    year = '2008'
    month = '01'
    day = '02'

    time_t, ask_t, identified_trades = pickle.load(open(''.join((
        f'../../taq_data/responses_event_shift_data_{year}/taq_trade_signs'
        + f'_responses_event_shift_data/taq_trade_signs_responses _event_shift'
        + f'_data_{year}{month}{day}_{ticker}.pickle').split()), 'rb'))

    # Reproducing S. Wang values. In her results the time interval for the
    # trade signs is [34801, 57000]
    full_time = np.array(range(34801, 57001))

    trades_sum = 0. * full_time
    trades_num = 0. * full_time

    # Implementation of equation (2). Trade sign in each second
    for t_idx, t_val in enumerate(full_time):

        condition = (time_t >= t_val) * (time_t < t_val + 1)
        # Empirical
        trades_same_t_exp = identified_trades[condition]
        t_sum = np.sum(trades_same_t_exp)
        t_num = np.sum(condition)
        trades_sum[t_idx] = t_sum
        trades_num[t_idx] = t_num

    plt.plot(trades_sum, label='sum')
    plt.legend()
    plt.title('$E_{j,d}(t)$')
    plt.xlabel('Time $[s]$')
    plt.ylabel('$E_{j,d}(t)$')
    plt.show()

    trades_sum_abs = np.abs(trades_sum)

    plt.plot(trades_sum_abs, label='sum')
    plt.legend()
    plt.title('$|E_{j,d}(t)|$')
    plt.xlabel('Time $[s]$')
    plt.ylabel('$|E_{j,d}(t)|$')
    plt.show()

    plt.plot(trades_num, label='num')
    plt.legend()
    plt.title('$N_{j,d}(t)$')
    plt.xlabel('Time $[s]$')
    plt.ylabel('Number of trades')
    plt.show()

    trades_sum_norm = (trades_sum - np.mean(trades_sum)) / np.std(trades_sum)
    trades_sum_abs_norm = (trades_sum_abs - np.mean(trades_sum_abs)) / np.std(trades_sum_abs)
    trades_num_norm = (trades_num - np.mean(trades_num)) / np.std(trades_num)

    plt.hist(trades_sum_norm, bins=100)
    plt.hist(trades_num_norm, bins=100)
    plt.hist(trades_sum_abs_norm, bins=100)
    plt.show()

    # plt.hist(trades_num, bins=100)
    # plt.show()

    # plt.plot(np.abs(trades_sum[trades_num != 0]) / trades_num[trades_num != 0])
    # plt.show()

    # plt.hist(np.abs(trades_sum[trades_num != 0]) / trades_num[trades_num != 0], bins=100)
    # plt.show()

    # Parallel computing
    # with mp.Pool(processes=mp.cpu_count()) as pool:
    #     pool.starmap(taq_self_response_year_avg_plot,
    #                  product(tickers, [year]))
    #     pool.starmap(taq_cross_response_year_avg_plot,
    #                  product(tickers, tickers, [year]))

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
