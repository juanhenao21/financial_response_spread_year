'''
ITCH data plot

Module to plot different ITCH results based on the results of the functions
set in the module itch_data_generator. The module plot the following data

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

- Self response behavior: plot the self response, the self response absolute
  and the zero correlation model for every day for a stock in independent
  plots in one figure.

- Trade sign cross correlator: plot the cross trade sign cross correlator for
  everey day for two stocks in independent pltos in one figure.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import os

import pickle

# -----------------------------------------------------------------------------------------------------------------------


def midpoint_plot(ticker, day):
    """
    Plot the midpoint price data during a open market day. The data is loaded
    from the mipoint price data results. Function to be used in the function
    midpoint_plot_week.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
    """

    # Load data

    print('Processing data for the stock ' + ticker + ' the day ' + day
          + ' March, 2016')

    midpoint = pickle.load(open(
        '../Data/midpoint_data/midpoint_201603{}_{}.pickl'.format(day, ticker),
        'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    # Plotting

    plt.plot(time[::100], midpoint[::100], label=('Day {}'.format(day)))
    plt.legend(loc=0, fontsize=20)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def midpoint_plot_week(ticker, days):
    """
    Plot the midpoint price data during a time period. The data is loaded from
    the mipoint price data results. The time period must be previously knowed
    and set to the function.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
    """

    plt.figure(figsize=(16, 9))

    for day in days:
        midpoint_plot(ticker, day)

    plt.title('{}'.format(ticker), fontsize=40)
    plt.xlabel(r'Time $[hour]$', fontsize=25)
    plt.ylabel(r'Price $ [\$] $', fontsize=25)
    plt.tight_layout()

    if (not os.path.isdir('../Data/midpoint_plot/')):

        os.mkdir('../Data/midpoint_plot/')
        print('Folder to save plot created')

    plt.savefig('../Data/midpoint_plot/midpoint_plot_week_{}.png'
                .format(ticker))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def trade_signs_plot(ticker, day):
    """
    Plot the trade signs data during one minute (11:00 to 11:01) in one day for
    a ticker. The data is loaded from the trade signs data results.
        :param ticker: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
    """
    # Load data

    print('Processing data for the stock ' + ticker + ' the day ' + day
          + ' March, 2016')

    trade_signs = pickle.load(open(
        '../Data/trade_signs_data/trade_signs_most_201603{}_{}.pickl'
        .format(day, ticker), 'rb'))
    time = pickle.load(open('../Data/midpoint_data/time.pickl', 'rb'))

    plt.figure(figsize=(16, 9))

    plt.plot(time[5399964:5457598] / 1000 / 3600,
             trade_signs[5399964:5457598], '-g',
             label='Trade signs using the majority')
    plt.title('Trade signs {}'.format(ticker), fontsize=40)
    plt.xlabel(r'Time $[hour]$', fontsize=25)
    plt.ylabel(r'Buy $(+1)$ or Sell $(-1)$', fontsize=25)
    plt.legend(loc='best', fontsize=20)

    plt.tight_layout()

    if (not os.path.isdir('../Data/trade_signs_plot/')):
        os.mkdir('../Data/trade_signs_plot/')
        print('Folder to save plot created')

    plt.savefig('../Data/trade_signs_plot/trade_signs_201603{}_{}.png'
                .format(day, ticker))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def self_response_plot(ticker, days, t_step):
    """
    Plot the self response during an interval of time (days) in independent
    plots in a figure. The data is loaded from the self response data results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker + ' the day ' + day
              + ' March, 2016')

        plot = pickle.load(open(
            '../Data/self_response_data_{}ms/self_201603{}_{}i_{}ms.pickl'
            .format(t_step, day, ticker, t_step), 'rb'))

        plt.subplot(len(days), 1, i+1)
        plt.semilogx(plot, '-g', label='Stock i {} - Day {}'
                     .format(ticker, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Self response $ R_{ii} (\tau) $')
        plt.legend(loc='best')
        plt.title('Self response - {} - {}ms'.format(ticker, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/self_response_plot_{}ms/'.format(t_step))):
        os.mkdir('../Data/self_response_plot_{}ms/'.format(t_step))
        print('Folder to save plot created')

    plt.savefig('../Data/self_response_plot_{}ms/self_response_{}_{}ms.png'
                .format(t_step, ticker, t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def self_response_abs_plot(ticker, days, t_step):
    """
    Plot the self response absolute during an interval of time (days) in
    independent plots in a figure. The data is loaded from the self response
    data results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker + ' the day ' + day
              + ' March, 2016')

        plot = pickle.load(open(
         '../Data/self_response_abs_data_{}ms/self_abs_201603{}_{}i_{}ms.pickl'
         .format(t_step, day, ticker, t_step), 'rb'))

        plt.subplot(len(days), 1, i+1)
        plt.semilogx(plot, '-g', label='Stock i {} - Day {}'
                     .format(ticker, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Self response $ R_{ii} (\tau) $')
        plt.legend(loc='best')
        plt.title('Self response absolute - {} - {}ms'.format(ticker, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/self_response_abs_plot_{}ms/'
                          .format(t_step))):
        os.mkdir('../Data/self_response_abs_plot_{}ms/'.format(t_step))
        print('Folder to save plot created')

    plt.savefig(
        '../Data/self_response_abs_plot_{}ms/self_response_abs_{}_{}ms.png'
        .format(t_step, ticker, t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def cross_response_plot(ticker_i, ticker_j, days, t_step):
    """
    Plot the cross response during an interval of time (days) in independent
    plots in a figure. The data is loaded from the cross response data results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker_i + ' and the stock '
              + ticker_j + ' the day ' + day + ' March, 2016')

        plot = pickle.load(open(
         '../Data/cross_response_data_{}ms/cross_201603{}_{}i_{}j_{}ms.pickl'
         .format(t_step, day, ticker_i, ticker_j, t_step), 'rb'))

        plt.subplot(len(days), 1, i+1)
        plt.semilogx(plot, '-g', label='Stock i {} - Stock j {} - Day {}'
                     .format(ticker_i, ticker_j, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Cross response $ R_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title('Cross response - ticker i {} ticker j {} - {}ms'
                  .format(ticker_i, ticker_j, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/cross_response_plot_{}ms/'.format(t_step))):
        os.mkdir('../Data/cross_response_plot_{}ms/'.format(t_step))
        print('Folder to save plot created')

    plt.savefig(
        '../Data/cross_response_plot_{}ms/cross_response_{}_{}_{}ms.png'
        .format(t_step, ticker_i, ticker_j, t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def avg_return_avg_trade_prod_plot(ticker_i, ticker_j, days, t_step):
    """
    Plot the average midpoint log return price multiplied by the average trade
    signs during an interval of time (days) in independent plots in a figure.
    The data is loaded from the averaged data results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker_i + ' and the stock '
              + ticker_j + ' the day ' + day + ' March, 2016')

        plot = pickle.load(open(
         '../Data/avg_return_sign_data_{}ms/avg_201603{}_{}i_{}j_{}ms.pickl'
         .format(t_step, day, ticker_i, ticker_j, t_step), 'rb'))

        plt.subplot(len(days), 1, i+1)
        plt.semilogx(plot, '-g', label='Stock i {} - Stock j {} - Day {}'
                     .format(ticker_i, ticker_j, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel("".join((r'$ \left \langle r_{i}\left ( t, \tau \right )'
                   + r'\right \rangle \left \langle \epsilon_{j} \left ( t'
                   + r'\right ) \right \rangle $').split()))
        plt.legend(loc='best')
        plt.title('Average - ticker i {} ticker j {} - {}ms'
                  .format(ticker_i, ticker_j, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/avg_return_sign_plot_{}ms/'
                          .format(t_step))):
        os.mkdir('../Data/avg_return_sign_plot_{}ms/'.format(t_step))
        print('Folder to save plot created')

    plt.savefig(
        '../Data/avg_return_sign_plot_{}ms/avg_response_{}_{}_{}ms.png'
        .format(t_step, ticker_i, ticker_j, t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------


def zero_correlation_plot(ticker, days, t_step):
    """
    Plot the zero correlation model during an interval of time (days) in
    independent plots in a figure. The data is loaded from the zero
    correlation model data results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """
    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for d, day in enumerate(days):

        print('Processing data for the stock ' + ticker + ' the day ' + day
              + ' March, 2016')

        plot = pickle.load(open("".join((
         '../Data/zero_correlation_data_{}ms/zero_correlation_201603{}_{}i'
         + '_rand_{}ms.pickl').split())
         .format(t_step, day, ticker, t_step), 'rb'))

        plt.subplot(5, 1, d+1)
        plt.semilogx(plot, '-g', label='Stock i {} and random trade sign - {}'
                     .format(ticker, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Self response random $ R_{ii} (\tau)_{rand} $')
        plt.title('Zero correlation - ticker i {} - {}ms'
                  .format(ticker, t_step))
        plt.legend(loc='best')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/zero_correlation_plot_{}ms/'
                          .format(t_step))):
        os.mkdir('../Data/zero_correlation_plot_{}ms/'.format(t_step))
        print('Folder to save plot created')

    plt.savefig(
        '../Data/zero_correlation_plot_{}ms/zero_corr_{}_{}ms.png'
        .format(t_step, ticker, t_step))

    return None
# -----------------------------------------------------------------------------------------------------------------------


def cross_response_avg_return_avg_trade_plot(ticker_i, ticker_j, days, t_step):
    """
    Plot the cross response and the avg return and trade  during an interval
    of time (days) in independent plots in a figure to compare the behavior of
    both results. The data is loaded from the cross response data results and
    the average return and average trade sign data results.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker_i + ' and the stock '
              + ticker_j + ' the day ' + day + ' March, 2016')

        cross = pickle.load(open(
         '../Data/cross_response_data_{}ms/cross_201603{}_{}i_{}j_{}ms.pickl'
         .format(t_step, day, ticker_i, ticker_j, t_step), 'rb'))
        avg = pickle.load(open(
         '../Data/avg_return_sign_data_{}ms/avg_201603{}_{}i_{}j_{}ms.pickl'
         .format(t_step, day, ticker_i, ticker_j, t_step), 'rb'))

        plt.subplot(len(days), 2, 2*i+1)
        plt.semilogx(cross, '-g', label='Stock i {} and stock j {} - {}'
                     .format(ticker_i, ticker_j, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Cross response $ R_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title('Cross - {}i - {}j - {}ms'
                  .format(ticker_i, ticker_j, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

        plt.subplot(len(days), 2, 2*i+2)
        plt.semilogx(avg, '-g', label='Stock i {} and stock j {} - {}'
                     .format(ticker_i, ticker_j, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel("".join((r'$ \left \langle r_{i}\left ( t, \tau \right )'
                   + r'\right \rangle \left \langle \epsilon_{j} \left ( t'
                   + r'\right ) \right \rangle $').split()))
        plt.legend(loc='best')
        plt.title('Avg - {}i - {}j - {}ms'
                  .format(ticker_i, ticker_j, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir(
     '../Data/cross_response_avg_return_avg_trade_plot_{}ms/'
     .format(t_step))):
            os.mkdir('../Data/cross_response_avg_return_avg_trade_plot_{}ms/'
                     .format(t_step))
            print('Folder to save plot created')

    plt.savefig("".join((
                '../Data/cross_response_avg_return_avg_trade_plot_{}ms/'
                + 'cross_response_avg_comparison_{}_{}_{}ms.png').split())
                .format(t_step, ticker_i, ticker_j, t_step))

    return None
# -----------------------------------------------------------------------------------------------------------------------


def self_response_self_abs_zero_corr_plot(ticker, days, t_step):
    """
    Plot the self response, self response absolute and zero correlation model
    during an interval of time (days) in independent plots in a figure. The
    data is loaded from the self response data results, the self response
    absolute data results and zero correlation model data results.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """
    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for d, day in enumerate(days):

        print('Processing data for the stock ' + ticker + ' the day ' + day
              + ' March, 2016')

        self_ = pickle.load(open(
         '../Data/self_response_data_{}ms/self_201603{}_{}i_{}ms.pickl'
         .format(t_step, day, ticker, t_step), 'rb'))
        abs_ = pickle.load(open(
         '../Data/self_response_abs_data_{}ms/self_abs_201603{}_{}i_{}ms.pickl'
         .format(t_step, day, ticker, t_step), 'rb'))
        zero = pickle.load(open("".join((
         '../Data/zero_correlation_data_{}ms/zero_correlation_201603{}_{}i'
         + '_rand_{}ms.pickl').split())
         .format(t_step, day, ticker, t_step), 'rb'))

        plt.subplot(len(days), 1, d+1)
        plt.semilogx(self_, '-', label='Self response Stock i {} - {}'
                     .format(ticker, day))
        plt.semilogx(abs_, '-', label='Self response abs Stock i {} - {}'
                     .format(ticker, day))
        plt.semilogx(zero, '-', label='Zero correlation Stock i {} - {}'
                     .format(ticker, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Self response $ R_{ii} (\tau) $')
        plt.legend(loc='best')
        plt.title('Self res - abs - zero - {}i - {}ms'
                  .format(ticker, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/self_res_self_abs_zero_corr_plot_{}ms/'
                          .format(t_step))):
        os.mkdir('../Data/self_res_self_abs_zero_corr_plot_{}ms/'
                 .format(t_step))
        print('Folder to save plot created')

    plt.savefig("".join((
        '../Data/self_res_self_abs_zero_corr_plot_{}ms/self_res_self_abs_'
        + 'zero_corr{}_{}ms.png').split()).format(t_step, ticker, t_step))

    return None
# -----------------------------------------------------------------------------------------------------------------------


def trade_sign_cross_correlator_plot(ticker_i, ticker_j, days, t_step):
    """
    Plot the trade sign cross correlator during an interval of time (days) in
    independent plots in a figure. The data is loaded from the trade sign cross
    correlator data results.
        :param ticker_i: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param days: string with the days to be analized
         (i.e ['07', '08', '09'])
        :param t_step: time step in the data in ms
    """

    plt.figure(figsize=(9, 16))
    plt.subplots_adjust(hspace=0, wspace=0)

    for i, day in enumerate(days):

        print('Processing data for the stock ' + ticker_i + ' and the stock '
              + ticker_j + ' the day ' + day + ' March, 2016')

        plot = pickle.load(open("".join((
         '../Data/trade_sign_cross_correlator_data_{}ms/trade_sign_cross_'
         + 'correlator_201603{}_{}i_{}j_{}ms.pickl').split())
         .format(t_step, day, ticker_i, ticker_j, t_step), 'rb'))

        plt.subplot(len(days), 1, i+1)
        plt.semilogx(plot, '-g', label='Stock i {} - Stock j {} - Day {}'
                     .format(ticker_i, ticker_j, day))
        plt.xlabel(r'Time lag $[\tau]$')
        plt.ylabel(r'Trade sign cross correlator $ \Theta_{ij} (\tau) $')
        plt.legend(loc='best')
        plt.title(
            'Trade sign cross correlator - ticker i {} ticker j {} - {}ms'
            .format(ticker_i, ticker_j, t_step))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(True)
        plt.tight_layout()

    if (not os.path.isdir('../Data/trade_sign_cross_correlator_plot_{}ms/'
                          .format(t_step))):
        os.mkdir('../Data/trade_sign_cross_correlator_plot_{}ms/'
                 .format(t_step))
        print('Folder to save plot created')

    plt.savefig("".join((
        '../Data/trade_sign_cross_correlator_plot_{}ms/trade_sign_cross_'
        + 'correlator__{}_{}_{}ms.png').split())
        .format(t_step, ticker_i, ticker_j, t_step))

    return None

# -----------------------------------------------------------------------------------------------------------------------














