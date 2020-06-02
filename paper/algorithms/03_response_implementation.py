'''TAQ response implementation.

Plots the figures of the response implementation for the paper.

This script requires the following modules:
    * matplotlib
    * pickle

The module contains the following functions:
    * taq_trade_scale_response_year_avg_plot - plots the average response for a
      year in trade time scale.
    * taq_physical_scale_response_year_avg_plot - plots the average response
      for a year in physical time scale.
    * taq_response_year_avg_comparison_plot - plots the average response for a
      year in trade time scale, physical time scale and the activity response.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import pickle

# ----------------------------------------------------------------------------


def taq_trade_scale_response_year_avg_plot(tickers, sectors, year):
    """Plots the avg self- and cross-response for a year in trade time scale.

    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :param year: string of the year to be analized (i.e. '2008')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 6))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        for ticker_i in tickers:

            # Load data
            self_resp = pickle.load(open(
                f'../../project/taq_data/responses_trade_data_{year}/taq_self'
                + f'_response_year_responses_trade_data/taq_self_response_year'
                + f'_responses_trade_data_{year}_{ticker_i}.pickle', 'rb'))

            ax1.semilogx(self_resp, linewidth=5, label=f'{ticker_i}')

        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax1.set_ylabel(r'$R^{t}_{ii}(\tau)$', fontsize=15)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        for sector in sectors:

            # Load data
            cross_resp = pickle.load(open(''.join((
                f'../../project/taq_data/responses_trade_data_{year}/taq_cross'
                + f'_response_year_responses_trade_data/taq_cross_response'
                + f'_year_responses_trade_data_{year}_{sector[0]}i_{sector[1]}'
                + f'j.pickle').split()), 'rb'))

            ax2.semilogx(cross_resp, linewidth=5,
                         label=f'{sector[0]} - {sector[1]}')

        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax2.set_ylabel(r'$R^{t}_{ij}(\tau)$', fontsize=15)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.set_xlim(1, 1000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(10)
        ax2.grid(True)

        plt.tight_layout()

        # Save Plot
        figure.savefig(f'../plot/03_responses_trade_scale_{year}.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def taq_physical_scale_response_year_avg_plot(tickers, sectors, year):
    """Plots the avg self- and cross-response for a year in physical time
       scale.

    :param tickers: list of strings of the abbreviation of the stocks to be
     analized (i.e. 'AAPL').
    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 6))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        for ticker_i in tickers:

            # Load data
            self_resp = pickle.load(open(
                        f'../../project/taq_data/responses_physical_data'
                        + f'_{year}/taq_self_response_year_responses_physical'
                        + f'_data/taq_self_response_year_responses_physical'
                        + f'_data_{year}_{ticker_i}.pickle', 'rb'))

            ax1.semilogx(self_resp, linewidth=5, label=f'{ticker_i}')

        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax1.set_ylabel(r'$R^{p}_{ii}(\tau)$', fontsize=15)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        for sector in sectors:

            # Load data
            cross_resp = pickle.load(open(
                        f'../../project/taq_data/responses_physical_data'
                        + f'_{year}/taq_cross_response_year_responses'
                        + f'_physical_data/taq_cross_response_year'
                        + f'_responses_physical_data_{year}_{sector[0]}i'
                        + f'_{sector[1]}j.pickle', 'rb'))

            ax2.semilogx(cross_resp, linewidth=5, label='{} - {}'
                         .format(sector[0], sector[1]))

        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax2.set_ylabel(r'$R^{p}_{ij}(\tau)$', fontsize=15)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(10)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig(f'../plot/03_responses_physical_scale_{year}.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def taq_response_year_avg_comparison_plot(ticker_i, ticker_j, year):
    """Plots the comparison of responses for different time scales.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 6))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        # Load data
        self_physical = pickle.load(open(
                        f'../../project/taq_data/responses_physical_data'
                        + f'_{year}/taq_self_response_year_responses_physical'
                        + f'_data/taq_self_response_year_responses_physical'
                        + f'_data_{year}_{ticker_i}.pickle', 'rb'))
        self_trade = pickle.load(open(
                        f'../../project/taq_data/responses_trade_data_{year}/'
                        + f'taq_self_response_year_responses_trade_data/taq'
                        + f'_self_response_year_responses_trade_data_{year}'
                        + f'_{ticker_i}.pickle', 'rb'))
        self_activity = pickle.load(open(
                        f'../../project/taq_data/responses_activity_data'
                        + f'_{year}/taq_self_response_year_responses_activity'
                        + f'_data/taq_self_response_year_responses_activity'
                        + f'_data_{year}_{ticker_i}.pickle', 'rb'))

        ax1.semilogx(self_physical, linewidth=5, label=r'$R_{ii}^{p}(\tau)$')
        ax1.semilogx(self_trade, linewidth=5, label=r'$R_{ii}^{t}(\tau)$')
        ax1.semilogx(self_activity, linewidth=5, label=r'$R_{ii}^{a}(\tau)$')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax1.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax1.set_ylabel(r'$R_{ii}(\tau)$ %s' % (ticker_i), fontsize=15)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(10)
        ax1.grid(True)

        # Load data
        cross_physical = pickle.load(open(
                        f'../../project/taq_data/responses_physical_data'
                        + f'_{year}/taq_cross_response_year_responses'
                        + f'_physical_data/taq_cross_response_year'
                        + f'_responses_physical_data_{year}_{ticker_i}i'
                        + f'_{ticker_j}j.pickle', 'rb'))
        cross_trade = pickle.load(open(
                        f'../../project/taq_data/responses_trade_data'
                        + f'_{year}/taq_cross_response_year_responses'
                        + f'_trade_data/taq_cross_response_year_responses'
                        + f'_trade_data_{year}_{ticker_i}i_{ticker_j}j'
                        + f'.pickle', 'rb'))
        cross_activity = pickle.load(open(
                        f'../../project/taq_data/responses_activity_data'
                        + f'_{year}/taq_cross_response_year_responses'
                        + f'_activity_data/taq_cross_response_year'
                        + f'_responses_activity_data_{year}_{ticker_i}i'
                        + f'_{ticker_j}j.pickle', 'rb'))

        ax2.semilogx(cross_physical, linewidth=5, label=r'$R_{ij}^{p}(\tau)$')
        ax2.semilogx(cross_trade, linewidth=5, label=r'$R_{ij}^{t}(\tau)$')
        ax2.semilogx(cross_activity, linewidth=5, label=r'$R_{ij}^{a}(\tau)$')
        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=15)
        ax2.set_xlabel(r'$\tau \, [s]$', fontsize=15)
        ax2.set_ylabel(r'$R_{ij}(\tau)$ %s - %s' % (ticker_i, ticker_j),
                       fontsize=15)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.set_xlim(1, 1000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(10)
        ax2.grid(True)

        plt.tight_layout()

        # Plotting
        plt.savefig(f'../plot/03_response_comparison_{year}_{ticker_i}i'
                    + f'_{ticker_j}j.png')

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

    ticker_i = 'APA'
    ticker_j = 'RIG'
    tickers = ['GOOG', 'MA', 'GS', 'CME', 'APA', 'RIG']
    sectors = [['GOOG', 'MA'], ['MA', 'GOOG'],
               ['GS', 'CME'], ['CME', 'GS'],
               ['APA', 'RIG'], ['RIG', 'APA']]
    year = '2008'

    taq_trade_scale_response_year_avg_plot(tickers, sectors, year)
    taq_physical_scale_response_year_avg_plot(tickers, sectors, year)
    taq_response_year_avg_comparison_plot(ticker_i, ticker_j, year)

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
