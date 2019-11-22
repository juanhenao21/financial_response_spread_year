'''TAQ response analysis.

Analize and plot the results of the response of different scales using the
values of $E_{j,d}\left(t\right)$ (sum of the trades in event scale) defined as

$$E_{j,d}\left(t\right)&=\sum_{n=1}^{N\left(t\right)}\varepsilon_{j,d}^{event}
  \left(t,n\right)$$

and $N_{j,d}\left(t\right)$ (number of trades per second).

This script requires the following modules:
    * matplotlib
    * numpy
    * scipy

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


def taq_trades_number_imbalance_day_data(ticker, date):
    """ Compute the number of trades an imbalance for a day.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    try:

        time_t, ask_t, identified_trades = pickle.load(open(''.join((
            f'../../taq_data/responses_event_shift_data_{year}/taq_trade_signs'
            + f'_responses_event_shift_data/taq_trade_signs_responses _event'
            + f'_shift_data_{year}{month}{day}_{ticker}.pickle').split()),
            'rb'))

        # Reproducing S. Wang values. In her results the time interval for the
        # trade signs is [34801, 57000]
        full_time = np.array(range(34801, 57001))

        # Arrays to store number of trades and imbalance of trades
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

        return (trades_num, trades_sum)

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_Ejd_Njd_general_info_day(ticker, date, trades_num, trades_sum):
    """General info of the trade number and imbalance for a day

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function print the info and does not return a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)
    # Filter trades and imbalance to only have seconds with activity
    condition_num_no_0 = trades_num != 0
    trades_num_no_0 = trades_num[condition_num_no_0]
    trades_sum_abs_no_0 = trades_sum_abs[condition_num_no_0]
    # |Ejd|(t) / Njd(t)
    rel_Ejd_Njd = trades_sum_abs_no_0 / trades_num_no_0

    print(f'General info - {ticker} - {date}')
    print()
    print(f'The max number of imbalances is {max(trades_sum_abs)}')
    print(f'The max number of trades is {max(trades_num)}')
    print()

    print(f'On average, they are {int(np.mean(trades_sum_abs))} imbalance per'
         + ' second')
    print(f'On average, they are {int(np.mean(trades_num))} trades per second')
    print()

    print('Zeros info')
    print(f'The trades have {np.sum(trades_num == 0)} second without events')
    print(f'The imbalance have {np.sum(trades_sum == 0)} seconds without'
         + 'events or with a balance')
    print(f'The number of balance is {np.sum(trades_sum_abs_no_0 == 0)}')
    print()

    print('Similarities')
    print(f'The number of values equal in E_j,d(t) and N_j,d(t) are '
         + f'{np.sum(trades_num == trades_sum_abs)} (excluding seconds '
         + f'without events)')
    print(f'The values equal to one in the relation E_jd(t)/N_jd(t) are'
          + f'{np.sum(rel_Ejd_Njd == 1)}')

    return None

# ----------------------------------------------------------------------------


def taq_imbalance_day_plot(ticker, date, trades_sum):
    """Plot the trades imbalance of one day

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    fig = plt.figure(figsize=(16,9))
    plt.plot(trades_sum, label='Imbalance')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}-{date}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$E_{j,d}(t$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/Ejd_{ticker}_{date}.png')

    return None

# ----------------------------------------------------------------------------


def taq_abs_imbalance_trades_day_plot(ticker, date, trades_num, trades_sum):
    """Plot the abs imbalance and the trades in the same plot.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)

    fig = plt.figure(figsize=(16,9))
    plt.plot(trades_num, label='$N_{j,d}(t)$')
    plt.plot(trades_sum_abs, label='$|E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}-{date}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$N_{j,d}(t)$ or $|E_{j,d}(t)|$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/abs_Ejd_Njd_{ticker}_{date}.png')

    return None

# ----------------------------------------------------------------------------


def taq_difference_trades_abs_imbalance_day_plot(ticker, date, trades_num,
                                                 trades_sum):
    """Plot of the difference between trades and abs imbalance.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)
    # Difference Nj,d(t) - |Ej,d(t)|
    difference_Njd_Ejd_abs = trades_num - trades_sum_abs

    fig = plt.figure(figsize=(16,9))
    plt.plot(difference_Njd_Ejd_abs, label='$N_{j,d}(t) - |E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}-{date}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'Trades', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/diff_Njd_Ejd_abs_{ticker}_{date}'
               + '.png')

    return None

# ----------------------------------------------------------------------------


def taq_pdf_trades_abs_imbalance_day_plot(ticker, date, trades_num,
                                          trades_sum):
    """Plot the distribution of trades and abs imbalance.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)

    fig = plt.figure(figsize=(16,9))
    plt.hist(trades_num, bins='auto', label='$N_{j,d}(t)$')
    plt.hist(trades_sum_abs, bins='auto', label='$|E_{j,d}(t)|$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}-{date}', fontsize=40)
    plt.xlabel(r'Number of trades or Imbalance number', fontsize=35)
    plt.ylabel(r'Counts', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlim((0,20))
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/Ejd_Njd_pdf_{ticker}_{date}.png')

    return None

# ----------------------------------------------------------------------------


def taq_relation_abs_imbalance_trades_plot(ticker, date, trades_num,
                                          trades_sum):
    """Plot the relation Ej,d(t)/Nj,d(t) of trades and abs imbalance.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)
    # Filter the seconds where there was no activity
    condition_num_no_0 = trades_num != 0
    trades_num_no_0 = trades_num[condition_num_no_0]
    trades_sum_abs_no_0 = trades_sum_abs[condition_num_no_0]
    # |Ej,d(t)| / Nj,d(t)
    rel_Ejd_Njd = trades_sum_abs_no_0 / trades_num_no_0

    fig = plt.figure(figsize=(16,9))
    plt.plot(rel_Ejd_Njd)
    plt.title(f'{ticker}-{date}', fontsize=40)
    plt.xlabel(r'Time $[s]$', fontsize=35)
    plt.ylabel(r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/Ejd_over_Njd_{ticker}_{date}'
                + '.png')

    return None

# ----------------------------------------------------------------------------


def taq_pdf_abs_imbalance_over_trades_day_plot(ticker, date, trades_num,
                                               trades_sum):
    """Plot the distribution of the relation between abs imbalance and trades.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param date: string with the date of the data to be extracted
     (i.e. '2008-01-02').
    :param trades_num: array with the number of trades for a day.
    :param trades_sum: array with the values of imbalances for a day.
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    # Magnitude of the imbalance
    trades_sum_abs = np.abs(trades_sum)
    # Filter the seconds where there was no activity
    condition_num_no_0 = trades_num != 0
    trades_num_no_0 = trades_num[condition_num_no_0]
    trades_sum_abs_no_0 = trades_sum_abs[condition_num_no_0]
    # |Ej,d(t)| / Nj,d(t)
    rel_Ejd_Njd = trades_sum_abs_no_0 / trades_num_no_0

    fig = plt.figure(figsize=(16,9))
    plt.hist(rel_Ejd_Njd, bins=100, label=r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$')
    plt.legend(loc='best', fontsize=25)
    plt.title(f'{ticker}_{date}', fontsize=40)
    plt.xlabel(r'$\frac{|E_{j,d}(t)|}{N_{j,d}(t)}$', fontsize=35)
    plt.ylabel(r'Counts', fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(f'../taq_plot/taq_Ejd_Njd/day/Ejd_over_Njd_pdf_{ticker}_{date}'
                + '.png')
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
    date = '2008-01-02'

    for ticker in tickers:

        trades_num, trades_sum = taq_trades_number_imbalance_day_data(ticker, date)

        # Plot Ej,d(t)
        taq_imbalance_day_plot(ticker, date, trades_sum)

        # Info
        taq_Ejd_Njd_general_info_day(ticker, date, trades_num, trades_sum)

        # Plot |Ej,d(t)| with Nj,d(t)
        taq_abs_imbalance_trades_day_plot(ticker, date, trades_num, trades_sum)

        # Plot Nj,d(t) - |Ej,d(t)|
        taq_difference_trades_abs_imbalance_day_plot(ticker, date, trades_num,
                                                    trades_sum)

        # PDF
        taq_pdf_trades_abs_imbalance_day_plot(ticker, date, trades_num, trades_sum)

        # Plot |Ej,d(t)| / Nj,d(t)
        taq_relation_abs_imbalance_trades_plot(ticker, date, trades_num,
                                            trades_sum)

        # PDF
        taq_pdf_abs_imbalance_over_trades_day_plot(ticker, date, trades_num,
                                                trades_sum)

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
