'''
TAQ data plot

Module to plot different TAQ results based on the results of the functions
set in the module taq_data_analysis. The module plot the following data

- Midpoint price data: plot the midpoint price for every day for a stock in
  one figure.

- Trade signs data: plot the trade signs in a minute of the open market
  (11:00 to 11:01).

- Self response data: plot the self response function for every day for a
  stock in individual plots in one figure.

- Cross response data: plot the cross response function for every day for
  two stock in individual plots in one figure.

- Average return average trade sign return data: plot the product between the
  averaged midpoint log retun and the trade signs for every day for two stocks
  in individual plots in one figure.

- Zero correlation model data: plot the zero correlation model for every day
  for a stock in individual plots in one figure.

- Cross response - average return/sign: plot the cross response function and
  the product of the averaged midpoint log return by the trade signs for every
  day for two stocks in independent figures to compare both results.

- Difference: plot the difference between cross response and average for every
  day for two stocks in individual plots in one figure.

- Self response behavior: plot the self response, the self response absolute
  and the zero correlation model for every day for a stock in independent
  plots in one figure.

- Trade sign cross correlator: plot the trade sign cross correlator for
  every day for two stocks in independent pltos in one figure.

- Trade sign self correlator: plot the trade sign self correlator for
  every day for one stock in independent plots in one figure.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

import numpy as np
from matplotlib import pyplot as plt
import os

import pickle

import taq_data_tools

__tau__ = 1000

# -----------------------------------------------------------------------------------------------------------------------


def taq_midpoint_plot(ticker, year, month, day):
    """
    Plot the midpoint price data during a open market day. The data is loaded
    from the mipoint price data results. Function to be used in the function
    midpoint_plot_week.
        :param ticker: String of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: String of the year to be analized (i.e '2008')
        :param month: String of the month to be analized (i.e '07')
        :param day: String of the day to be analized (i.e '07')
    """

    function_name = taq_midpoint_plot.__name__
    taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                  ticker, year, month, day)
    # Load data

    midpoint = pickle.load(open(''.join((
                                '../taq_data_{1}/taq_midpoint_data/taq_'
                                + 'midpoint_data_midpoint_{1}{2}{3}_{0}.pickl'
                                ).split())
                                .format(ticker, year, month, day), 'rb'))
    time = pickle.load(open(''.join((
                            '../taq_data_{}/taq_midpoint_data/taq_midpoint_'
                            + 'data_time.pickl').split()).format(year), 'rb'))

    # Plotting

    plt.plot(time / 3600, midpoint, label=('Day {}'.format(day)))
    plt.legend(loc=0, fontsize=20)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_midpoint_plot_week(ticker, year, month, days):
    """
    Plot the midpoint price data during a time period. The data is loaded from
    the mipoint price data results. The time period must be previously knowed
    and set to the function.
        :param ticker: String of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: String of the year to be analized (i.e '2008')
        :param month: String of the month to be analized (i.e '07')
        :param days: String with the days to be analized
         (i.e ['07', '08', '09'])
    """

    figure = plt.figure(figsize=(16, 9))

    for day in days:
        taq_midpoint_plot(ticker, year, month, day)

    plt.title('{}'.format(ticker), fontsize=40)
    plt.xlabel(r'Time $[hour]$', fontsize=25)
    plt.ylabel(r'Price $ [\$] $', fontsize=25)
    plt.tight_layout()
    plt.grid(True)

    # Plotting

    function_name = taq_midpoint_plot_week.__name__
    taq_data_tools.taq_save_plot(function_name, figure, ticker, ticker, year,
                                 month)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_ask_bid_midpoint_spread_plot(ticker, year, month, day):
    """
    Plot the ask, bid, midpoint price and spread data during a open market
    day. The data is loaded from the mipoint price data results.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """

    function_name = taq_ask_bid_midpoint_spread_plot.__name__
    taq_data_tools.taq_function_header_print_plot(function_name, ticker,
                                                  ticker, year, month, day)

    # Load data

    ask = pickle.load(open(''.join((
                           '../taq_data_{1}/taq_midpoint_data/taq_midpoint_'
                           + 'data_ask_{1}{2}{3}_{0}.pickle').split())
                           .format(ticker, year, month, day), 'rb'))
    bid = pickle.load(open(''.join((
                           '../taq_data_{1}/taq_midpoint_data/taq_midpoint_'
                           + 'data_bid_{1}{2}{3}_{0}.pickle').split())
                           .format(ticker, year, month, day), 'rb'))
    midpoint = pickle.load(open(''.join((
                                '../taq_data_{1}/taq_midpoint_data/taq_'
                                + 'midpoint_data_midpoint_{1}{2}{3}_{0}.pickle'
                                ).split())
                                .format(ticker, year, month, day), 'rb'))
    spread = pickle.load(open(''.join((
                              '../taq_data_{1}/taq_midpoint_data/taq_midpoint'
                              + '_data_spread_{1}{2}{3}_{0}.pickle').split())
                              .format(ticker, year, month, day), 'rb'))
    time = pickle.load(open(''.join((
                            '../taq_data_{}/taq_midpoint_data/taq_midpoint_'
                            + 'data_time.pickle').split()).format(year), 'rb'))

    figure = plt.figure(figsize=(16, 9))
    figure.suptitle('{} - {}.{}.{}'.format(ticker, year, month, day),
                    fontsize=16)
    figure.tight_layout()
    figure.subplots_adjust(top=0.95, wspace=0.3)

    plt.subplot(4, 2, 1)
    plt.plot(time / 3600, midpoint, label='Midpoint')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(4, 2, 2)
    plt.plot(time / 3600, spread, label='Spread')
    plt.xlabel('Time')
    plt.ylabel('Spread')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(4, 2, 3)
    plt.plot(time / 3600, bid, label='Bid quotes')
    plt.plot(time / 3600, ask, label='Ask quotes')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(4, 2, 4)
    plt.scatter(time / 3600, ask, marker='.', s=5, label='Ask trades')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.grid(True)

    # Saving data

    if (not os.path.isdir('../taq_plot_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../taq_plot_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    figure.savefig(
            '../taq_plot_{2}/{0}/{0}_{2}{3}_{1}i.png'
            .format(function_name, ticker, year, month))

    print('Plot saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_cross_response_plot(ticker_i, ticker_j, year, month, days):
    """
    Plot the cross response during an interval of time (days) in independent
    plots in a figure. The data is loaded from the cross response data results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(9, 16))
        plt.subplots_adjust(hspace=0, wspace=0)

        for i, day in enumerate(days):

            function_name = taq_cross_response_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            plot = pickle.load(open(''.join((
                '../taq_data_{2}/taq_cross_response_data/taq_cross'
                + '_response_data_{2}{3}{4}_{0}i_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, month, day), 'rb'))

            plt.subplot(len(days), 1, i+1)
            plt.semilogx(plot, '-g', label='Stock i {} - Stock j {} - Day {}'
                         .format(ticker_i, ticker_j, day))
            plt.xlabel(r'Time lag $[\tau]$')
            plt.ylabel(r'Cross response $ R_{ij} (\tau) $')
            plt.legend(loc='best')
            plt.title('Cross response - ticker i {} ticker j {}'
                      .format(ticker_i, ticker_j))
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.grid(True)
            plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                     ticker_j, year, month)

        return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_cross_response_week_avg_plot(ticker_i, ticker_j, year, month, days):
    """
    Plot the average cross response during a week and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param days: List of strings with the days to be analized
         (i.e ['07', '08', '09'])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(16, 9))

        plot_data = np.zeros(__tau__)

        for i, day in enumerate(days):

            function_name = taq_cross_response_week_avg_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            load_day = pickle.load(open(''.join((
                '../taq_data_{2}/taq_cross_response_data/taq_cross'
                + '_response_data_{2}{3}{4}_{0}i_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, month, day), 'rb'))

            plot_data += load_day

            plt.semilogx(load_day, '-', alpha=0.4,
                         label='Stock i {} - Stock j {} - Day {}'
                         .format(ticker_i, ticker_j, day))

        plot_data = plot_data / len(days)

        plt.semilogx(plot_data, '-g', linewidth=5,
                     label='Stock i {} - Stock j {} - Week Average'
                     .format(ticker_i, ticker_j))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Cross response $ R_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title('Cross response - ticker i {} ticker j {} - {}.{}-{}'
                  .format(ticker_i, ticker_j, month, days[0], days[-1]))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        # Plotting
        taq_data_tools.taq_save_plot(function_name, figure, ticker_i,
                                     ticker_j, year, month)

        return None
# -----------------------------------------------------------------------------------------------------------------------


def taq_cross_response_month_avg_plot(ticker_i, ticker_j, year, month, days):
    """
    Plot the average cross response during a month and the dayly cross-response
    contributions in a figure. The data is loaded from the cross response data
    results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2008')
        :param month: string of the month to be analized (i.e '07')
        :param days: List of strings with the days to be analized
         (i.e ['07', '08', '09'])
    """

    if (ticker_i == ticker_j):

        return None

    else:

        figure = plt.figure(figsize=(16, 9))

        plot_data = np.zeros(__tau__)

        for i, day in enumerate(days):

            function_name = taq_cross_response_month_avg_plot.__name__
            taq_data_tools.taq_function_header_print_plot(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            load_day = pickle.load(open(''.join((
                '../taq_data_{2}/taq_cross_response_data/taq_cross'
                + '_response_data_{2}{3}{4}_{0}i_{1}j.pickle').split())
                .format(ticker_i, ticker_j, year, month, day), 'rb'))

            plot_data += load_day

            plt.semilogx(load_day, '-', alpha=0.4)

        plot_data = plot_data / len(days)

        plt.semilogx(plot_data, '-g', linewidth=5,
                     label='Stock i {} - Stock j {} - Month Average'
                     .format(ticker_i, ticker_j))
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

# -----------------------------------------------------------------------------------------------------------------------


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

                function_name = taq_cross_response_month_avg_plot.__name__
                taq_data_tools.taq_function_header_print_plot(function_name,
                                                              ticker_i, ticker_j,
                                                              year, month, day)

                load_day = pickle.load(open(''.join((
                    '../taq_data_{2}/taq_cross_response_data/taq_cross'
                    + '_response_data_{2}{3}{4}_{0}i_{1}j.pickle').split())
                    .format(ticker_i, ticker_j, year, month, day), 'rb'))

                plot_data_month += load_day

                plt.semilogx(load_day, '-', alpha=0.1)

            plot_data_month = plot_data_month / len(days[int(month) - 1])

            plt.semilogx(plot_data_month, '-', alpha=0.5,
                         label='Stock i {} - Stock j {} - Month {}'
                         .format(ticker_i, ticker_j, month))

            plot_data_year += plot_data_month

        plot_data_year = plot_data_year / len(months)
        plt.semilogx(plot_data_year, '-', linewidth=5,
                         label='Stock i {} - Stock j {} - Year'
                         .format(ticker_i, ticker_j, month))

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
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
