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
import scipy.stats as stats
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

    # Plot Ej,d(t)
    fig = plt.figure(figsize=(16,9))
    plt.plot(trades_sum, label='sum')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$E_{j,d}(t$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('Ejd.png')

    # Get the absolute value of Ej,d(t) to see the magnitud
    trades_sum_abs = np.abs(trades_sum)

    # Max number of imbalance and trades per second
    print()
    print('GENERAL INFO')
    print(f'The max number of imbalances is {max(trades_sum_abs)}')
    print(f'The max number of trades is {max(trades_num)}')

    print(f'On average, they are {int(np.mean(trades_num))} trades per second')
    print(f'On average, they are {int(np.mean(trades_sum_abs))} imbalance per second')

    # Plot |Ej,d(t)| with Nj,d(t)
    fig = plt.figure(figsize=(16,9))
    plt.plot(trades_num, label='$N_{j,d}(t)$')
    plt.plot(trades_sum_abs, label='$|E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$N_{j,d}(t)$ or $|E_{j,d}(t)|$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('Ejd_abs_vs_Njd.png')

    print()
    print('ZEROS INFO')
    print(f'The number of values equal in E and N are {np.sum(trades_num == trades_sum_abs)}')
    # Difference Nj,d(t) - |Ej,d(t)|
    difference_Njd_Ejd_abs = trades_num - trades_sum_abs

    print(f'The number of values greater than zero are {len(difference_Njd_Ejd_abs[difference_Njd_Ejd_abs > 0])}')
    print(f'The number of values equal to zero are {len(difference_Njd_Ejd_abs[difference_Njd_Ejd_abs == 0])}')

    # Plot Nj,d(t) - |Ej,d(t)|
    fig = plt.figure(figsize=(16,9))
    plt.plot(difference_Njd_Ejd_abs, label='$N_{j,d}(t) - |E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'Trades', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('difference_Ejd_abs_Njd.png')

    # PDF
    fig = plt.figure(figsize=(16,9))
    plt.hist(trades_num, bins='auto', label='$N_{j,d}(t)$')
    plt.hist(trades_sum_abs, bins='auto', label='$|E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'Number of trades or Imbalance number', fontsize=35)
    plt.ylabel(r'Counts', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlim((0,20))
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('Ejd_Njd_pdf.png')

    # |Ej,d(t)| and Nj,d(t) without zero with reference trade numbers
    condition_num_no_0 = trades_num != 0
    trades_num_no_0 = trades_num[condition_num_no_0]
    trades_sum_abs_no_0 = trades_sum_abs[condition_num_no_0]
    print(f'El número de segundos con balance es {np.sum(trades_sum_abs_no_0 == 0)}')

    # |Ej,d(t)| / Nj,d(t)
    rel_Ejd_Njd = trades_sum_abs_no_0 / trades_num_no_0

    print(f'The values equal to one are equal to {np.sum(rel_Ejd_Njd == 1)}')

    # Plot |Ej,d(t)| / Nj,d(t)
    fig = plt.figure(figsize=(16,9))
    plt.plot(rel_Ejd_Njd)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('Ejd_over_Njd.png')

    # PDF
    fig = plt.figure(figsize=(16,9))
    plt.hist(rel_Ejd_Njd, bins=100, label=r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}', fontsize=40)
    plt.xlabel(r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$', fontsize=35)
    plt.ylabel(r'Counts', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig('Ejd_over_Njd_pdf.png')

    # Normalization of the values to compare the PDF
    # trades_sum_norm = (trades_sum - np.mean(trades_sum)) / np.std(trades_sum)
    # trades_sum_abs_norm = (trades_sum_abs - np.mean(trades_sum_abs)) / np.std(trades_sum_abs)
    # trades_num_norm = (trades_num - np.mean(trades_num)) / np.std(trades_num)

    # plt.hist(trades_num_norm, bins='auto')
    # plt.hist(trades_sum_abs_norm, bins='auto')
    # plt.xlim((-1,5))
    # plt.show()

    # plt.hist(trades_num, bins=100)
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
