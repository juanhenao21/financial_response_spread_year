'''Self- and cross responses figures

Plot the self- and cross responses for the stocks AAPL, CVX, GS, JPM, MSFT,
and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
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
        figure = plt.figure(figsize=(16, 9))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        for ticker_i in tickers:

            # Load data
            self_resp = pickle.load(open(''.join((
                f'../../project/taq_data/responses_event_data_{year}/taq_self'
                + f'_response_year_responses_event_data/taq_self_response'
                + f'_year_responses_event_data_{year}_{ticker_i}.pickle')
                .split()), 'rb'))

            ax1.semilogx(self_resp, linewidth=5, label=f'{ticker_i}')

        ax1.legend(loc='lower left', fontsize=20)
        ax1.set_title('Self-response', fontsize=40)
        ax1.set_xlabel(r'$\tau \, [trades]$', fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau_{trades})$', fontsize=20)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        for sector in sectors:

            # Load data
            cross_resp = pickle.load(open(''.join((
                f'../../project/taq_data/responses_event_data_{year}/taq_cross'
                + f'_response_year_responses_event_data/taq_cross_response'
                + f'_year_responses_event_data_{year}_{sector[0]}i_{sector[1]}'
                + f'j.pickle').split()), 'rb'))

            ax2.semilogx(cross_resp, linewidth=5,
                         label=f'{sector[0]} - {sector[1]}')

        ax2.legend(loc='lower left', fontsize=20)
        ax2.set_title('Cross-response', fontsize=40)
        ax2.set_xlabel(r'$\tau \, [trades]$', fontsize=20)
        ax2.set_ylabel(r'$R_{ij}(\tau_{trades})$', fontsize=20)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.set_xlim(1, 1000)
        # plt.ylim(4 * 10 ** -5, 9 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save Plot
        figure.savefig(f'../plot/01_responses_trade_scale_{year}')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def taq_time_scale_response_year_avg_plot(tickers, sectors, year):
    """Plots the cross-response average for a year.

    :param sectors: list of lists with the strings of the abbreviation of the
     stocks to be analized and the year
     (i.e. [['AAPL', 'MSFT', '2008], ['CVX', 'XOM', '2008]]).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        for ticker_i in tickers:

            # Load data
            self_resp = pickle.load(open(''.join((
                f'../../project/taq_data/article_reproduction_data_{year}/taq'
                + f'_self_response_year_data/taq_self_response_year_data'
                + f'_{year}_{ticker_i}.pickle').split()), 'rb'))

            ax1.semilogx(self_resp, linewidth=5, label=f'{ticker_i}')

        ax1.legend(loc='lower left', fontsize=20)
        ax1.set_title('Self-response', fontsize=40)
        ax1.set_xlabel(r'$\tau \, [seconds]$', fontsize=20)
        ax1.set_ylabel(r'$R_{ii}(\tau_{seconds})$', fontsize=20)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax1.yaxis.offsetText.set_fontsize(15)
        ax1.grid(True)

        for sector in sectors:

            # Load data
            cross_resp = pickle.load(open(''.join((
                f'../../project/taq_data/article_reproduction_data_{year}/taq'
                + f'_cross_response_year_data/taq_cross_response_year_data'
                + f'_{year}_{sector[0]}i_{sector[1]}j.pickle').split()), 'rb'))

            ax2.semilogx(cross_resp, linewidth=5, label='{} - {}'
                         .format(sector[0], sector[1]))

        ax2.legend(loc='lower left', fontsize=20)
        ax2.set_title('Cross-response', fontsize=40)
        ax2.set_xlabel(r'$\tau \, [seconds]$', fontsize=20)
        ax2.set_ylabel(r'$R_{ij}(\tau_{seconds})$', fontsize=20)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.set_xlim(1, 1000)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax2.yaxis.offsetText.set_fontsize(15)
        ax2.grid(True)

        plt.tight_layout()

        # Save plot
        figure.savefig(f'../plot/01_responses_time_scale_{year}')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        return None

# ----------------------------------------------------------------------------


def main():

    tickers = ['AAPL', 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    sectors = [['AAPL', 'MSFT'], ['MSFT', 'AAPL'],
               ['XOM', 'CVX'], ['CVX', 'XOM'],
               ['GS', 'JPM'], ['JPM', 'GS']]
    year = '2008'

    taq_trade_scale_response_year_avg_plot(tickers, sectors, year)
    taq_time_scale_response_year_avg_plot(tickers, sectors, year)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
