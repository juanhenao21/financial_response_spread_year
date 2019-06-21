'''
TAQ data plot

Module to plot different TAQ data results based on the results of the functions
set in the module taq_data_analysis. The module plot the following data

- Midpoint price data: it is possible to plot a day or a group of days in a week
  in the same figure.

- Self response data: it is possible to plot a day, or a group of days in a week
  and the average, a month and the average or the year and the average.

- Cross response data: it is possible to plot a day, or a group of days in a week
  and the average, a month and the average or the year and the average.

- Trade sign self correlator: plot the trade sign self correlator for
  every day for one stock in independent plots in one figure.

- Trade sign cross correlator: plot the trade sign cross correlator for
  every day for two stocks in independent pltos in one figure.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
from matplotlib import pyplot as plt
import os

import pickle

import taq_data_tools

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_plot(ticker, year, months, days):
    """
    Plot the average cross response during a year and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: List of strings of the months to be analized
         (i.e ['07', '08', '09'])
        :param days: List of lists of strings with the days to be analized
         (i.e [['07', '08', '09'], ['01', '02']])
    """

    figure = plt.figure(figsize=(16, 9))

    plot_data_year = np.zeros(__tau__)

    for month in months:

        plot_data_month = np.zeros(__tau__)

        for i, day in enumerate(days[int(month) - 1]):

            function_name = taq_self_response_year_avg_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker, ticker,
                                                          year, month, day)

            try:
                load_day = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq_self_response'
                    + '_data/taq_self_response_data_{1}{2}{3}_{0}.pickle')
                    .split()).format(ticker, year, month, day), 'rb'))

                plot_data_month += load_day

                plt.semilogx(load_day, '-', alpha=0.1)
            except FileNotFoundError:
                pass

        plot_data_month = plot_data_month / len(days[int(month) - 1])

        plt.semilogx(plot_data_month, '-', alpha=0.5,
                     label='Stock i {} - Month {}'
                     .format(ticker, month))

        plot_data_year += plot_data_month

    plot_data_year = plot_data_year / len(months)
    plt.semilogx(plot_data_year, '-', linewidth=5,
                 label='Stock {} - Year {}'
                 .format(ticker, year))

    plt.ylim(0, 2 * 10 ** -4)
    plt.xlim(1, __tau__)
    plt.xlabel(r'Time lag $[\tau]$')
    plt.ylabel(r'Self response $ R_{ij} (\tau) $')
    plt.legend(loc='best')
    plt.title('Self response - ticker {} - Year {}'
              .format(ticker, year))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.grid(True)
    plt.tight_layout()

    # Plotting
    taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker, year,
                                 month)

    return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_plot(ticker_i, ticker_j, year, months, days):
    """
    Plot the average cross response during a month and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: List of strings of the months to be analized
         (i.e ['07', '08', '09'])
        :param days: List of lists of strings with the days to be analized
         (i.e [['07', '08', '09'], ['01', '02']])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(16, 9))

        plot_data_year = np.zeros(__tau__)

        for month in months:

            plot_data_month = np.zeros(__tau__)

            for i, day in enumerate(days[int(month) - 1]):

                function_name = taq_cross_response_year_avg_plot.__name__
                taq_data_tools.taq_function_header_print_plot(function_name,
                                                              ticker_i,
                                                              ticker_j,
                                                              year, month, day)

                try:
                    load_day = pickle.load(open(''.join((
                        '../../taq_data/article_reproduction_data_{2}/taq_cross_response_data/taq_cross'
                        + '_response_data_{2}{3}{4}_{0}i_{1}j.pickle')
                        .split())
                        .format(ticker_i, ticker_j, year, month, day), 'rb'))

                    plot_data_month += load_day

                    plt.semilogx(load_day, '-', alpha=0.1)
                except FileNotFoundError:
                    pass

            plot_data_month = plot_data_month / len(days[int(month) - 1])

            plt.semilogx(plot_data_month, '-', alpha=0.5,
                         label='Stock i {} - Stock j {} - Month {}'
                         .format(ticker_i, ticker_j, month))

            plot_data_year += plot_data_month

        plot_data_year = plot_data_year / len(months)
        plt.semilogx(plot_data_year, '-', linewidth=5,
                     label='Stock i {} - Stock j {} - Year'
                     .format(ticker_i, ticker_j, month))

        plt.ylim(0, 10 ** -4)
        plt.xlim(1, __tau__)
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Cross response $ R_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title('Cross response - ticker i {} ticker j {} - Month {}'
                  .format(ticker_i, ticker_j, month))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                     ticker_j, year, month)

        return None

# ----------------------------------------------------------------------------


def taq_trade_sign_self_correlator_year_avg_plot(ticker, year, months, days):
    """
    Plot the average trade sign self correlator during a year and the dayly self response
    contributions in a figure. The data is loaded from the trade sign self correlator data
    results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: List of strings of the months to be analized
         (i.e ['07', '08', '09'])
        :param days: List of lists of strings with the days to be analized
         (i.e [['07', '08', '09'], ['01', '02']])
    """

    figure = plt.figure(figsize=(16, 9))

    plot_data_year = np.zeros(__tau__)

    for month in months:

        plot_data_month = np.zeros(__tau__)

        for i, day in enumerate(days[int(month) - 1]):

            function_name = taq_trade_sign_self_correlator_year_avg_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker, ticker,
                                                          year, month, day)

            load_day = pickle.load(open(''.join((
                '../taq_data_{1}/taq_trade_sign_self_correlator_data/'
                + 'taq_trade_sign_self_correlator_data_{1}{2}{3}_{0}'
                + '.pickle').split())
                .format(ticker, year, month, day), 'rb'))

            plot_data_month += load_day

            plt.loglog(load_day, '-', alpha=0.1)

        plot_data_month = plot_data_month / len(days[int(month) - 1])

        plt.loglog(plot_data_month, '-', alpha=0.5,
                     label='Stock i {} - Month {}'
                     .format(ticker, month))

        plot_data_year += plot_data_month

    plot_data_year = plot_data_year / len(months)
    plt.loglog(plot_data_year, '-', linewidth=5,
                 label='Stock {} - Year {}'
                 .format(ticker, year))

    plt.ylim(10 ** -6, 1)
    plt.xlabel(r'Time lag $[\tau]$')
    plt.ylabel(r'Trade sign self-correlator $ \Theta_{ij} (\tau) $')
    plt.legend(loc='best')
    plt.title('Trade sign self-correlator - ticker {} -  Year {}'
              .format(ticker, year))
    plt.grid(True)
    plt.tight_layout()

    # Plotting
    taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker, year,
                                 month)

    return None

# ----------------------------------------------------------------------------


def taq_trade_sign_cross_correlator_year_avg_plot(ticker_i, ticker_j, year, months, days):
    """
    Plot the average trade sign cross correlator during a year and the dayly self response
    contributions in a figure. The data is loaded from the trade sign cross correlator data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: List of strings of the months to be analized
         (i.e ['07', '08', '09'])
        :param days: List of lists of strings with the days to be analized
         (i.e [['07', '08', '09'], ['01', '02']])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(16, 9))

        plot_data_year = np.zeros(__tau__)

        for month in months:

            plot_data_month = np.zeros(__tau__)

            for i, day in enumerate(days[int(month) - 1]):

                function_name = taq_trade_sign_cross_correlator_year_avg_plot.__name__
                taq_data_tools.taq_function_header_print_plot(function_name,
                                                              ticker_i,
                                                              ticker_j,
                                                              year, month, day)

                load_day = pickle.load(open(''.join((
                '../taq_data_{2}/taq_trade_sign_cross_correlator_data'
                + '/taq_trade_sign_cross_correlator_data_{2}{3}{4}_{0}i_{1}j'
                + '.pickle').split())
                .format(ticker_i, ticker_j, year, month, day), 'rb'))

                plot_data_month += load_day

                plt.loglog(load_day, '-', alpha=0.1)

            plot_data_month = plot_data_month / len(days[int(month) - 1])

            plt.loglog(plot_data_month, '-', alpha=0.5,
                         label='Stock i {} - Stock j {} - Month {}'
                         .format(ticker_i, ticker_j, month))

            plot_data_year += plot_data_month

        plot_data_year = plot_data_year / len(months)
        plt.loglog(plot_data_year, '-', linewidth=5,
                     label='Stock i {} - Stock j {} - Year {}'
                     .format(ticker_i, ticker_j, year))

        plt.ylim(10 ** -6, 1)
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Trade sign cross correlator $ \Theta_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title('Cross response - ticker i {} ticker j {} - Year {}'
                  .format(ticker_i, ticker_j, year))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                     ticker_j, year, month)

        return None

# ----------------------------------------------------------------------------
