'''Short and long self- and cross responses figures

Plot the short and long self- and cross responses for the stocks AAPL, CVX,
GS, JPM, MSFT, and XOM.
'''

# ----------------------------------------------------------------------------
# Modules
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle

# ----------------------------------------------------------------------------


def taq_self_response_year_avg_responses_time_short_long_plot(ticker, year,
                                                              tau, tau_p):
    """Plots the short and long self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param tau: integer greater than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        figure = plt.figure(figsize=(16, 9))
        ax = figure.add_subplot(111)

        # Load data
        (self_short,
         self_long,
         self_response,
         self_shuffle) = pickle.load(open(''.join((
                                     '../../project/taq_data/responses_time'
                                     + '_short_long_data_{1}/taq_self_response'
                                     + '_year_time_short_long_tau_data_tau'
                                     + '_{2}_tau_p_{3}/taq_self_response_year'
                                     + '_time_short_long_tau_data_tau_{2}_tau'
                                     + '_p_{3}_{1}_{0}.pickle').split())
                                     .format(ticker, year, tau, tau_p), 'rb'))

        # Addition of the short and long response signal
        sum = np.zeros(tau)
        sum[:tau_p + 1] = self_short[:tau_p + 1]
        sum[tau_p + 1:] = self_short[tau_p + 1:] + self_long[tau_p + 1:]

        plt.semilogx(self_short, linewidth=5, label='Short')
        plt.semilogx(self_long, linewidth=5, label='Long')
        plt.semilogx(sum, linewidth=5, label='Sum')
        plt.semilogx(self_response, linewidth=5, label='Self-response')
        plt.semilogx(self_shuffle, linewidth=5, label='Shuffle')
        plt.plot((tau_p, tau_p), (-1000, 1000), '--k', linewidth=5,
                 label=r"$\tau' $ = {}".format(tau_p))

        plt.legend(loc='lower left', fontsize=35)
        # plt.title('Self-response', fontsize=40)
        plt.xlabel(r'$\tau \, [s]$', fontsize=45)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=45)
        plt.xticks(fontsize=35)
        plt.yticks(fontsize=35)
        plt.xlim(1, 1000)
        plt.ylim(-0.2 * 10 ** -4, 1.6 * 10 ** -4)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(35)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Save plot
        figure.savefig('../plot/05_self_short_long_{}.png'.format(ticker))

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_avg_responses_time_short_long_plot(ticker_i,
                                                               ticker_j, year,
                                                               tau, tau_p):
    """Plots the short and long cross-response average for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008')
    :param tau: integer greater than zero (i.e. 50).
    :param tau_p: integer greater than zero and smaller than tau (i.e. 10).
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    if (ticker_i == ticker_j):

        # Self-response
        return None

    else:
        try:
            figure = plt.figure(figsize=(16, 9))
            ax = figure.add_subplot(111)

            # Load data
            (cross_short,
             cross_long,
             cross_response,
             cross_shuffle) = pickle.load(open(''.join((
                                          '../../project/taq_data/responses'
                                          + '_time_short_long_data_{2}/taq'
                                          + '_cross_response_year_time_short'
                                          + '_long_tau_data_tau_{3}_tau_p_{4}'
                                          + '/taq_cross_response_year_time'
                                          + '_short_long_tau_data_tau_{3}_tau'
                                          + '_p_{4}_{2}_{0}i_{1}j.pickle')
                                          .split())
                                          .format(ticker_i, ticker_j, year,
                                                  tau, tau_p), 'rb'))

            # Addition of the short and long response signal
            sum = np.zeros(tau)
            sum[:tau_p + 1] = cross_short[:tau_p + 1]
            sum[tau_p + 1:] = cross_short[tau_p + 1:] + cross_long[tau_p + 1:]

            plt.semilogx(cross_short, linewidth=5, label='Short')
            plt.semilogx(cross_long, linewidth=5, label='Long')
            plt.semilogx(sum, linewidth=5, label='Sum')
            plt.semilogx(cross_response, linewidth=5, label='Cross-response')
            plt.semilogx(cross_shuffle, linewidth=5, label='Shuffle')
            plt.plot((tau_p, tau_p), (-1000, 1000), '--k', linewidth=5,
                     label=r"$\tau' $ = {}".format(tau_p))

            plt.legend(loc='lower left', fontsize=35)
            # plt.title('Cross-response', fontsize=40)
            plt.xlabel(r'$\tau \, [s]$', fontsize=45)
            plt.ylabel(r'$R_{ij}(\tau)$', fontsize=45)
            plt.xticks(fontsize=35)
            plt.yticks(fontsize=35)
            plt.xlim(1, 1000)
            plt.ylim(-8 * 10 ** -5, 9 * 10 ** -5)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax.yaxis.offsetText.set_fontsize(35)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            # Plotting
            figure.savefig('../plot/05_cross_short_long_{}_{}.png'
                           .format(ticker_i, ticker_j))

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def main():

    year = '2008'

    taq_self_response_year_avg_responses_time_short_long_plot('AAPL', year,
                                                              1000, 40)
    taq_cross_response_year_avg_responses_time_short_long_plot('AAPL', 'MSFT',
                                                               year, 1000, 40)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
