'''TAQ short and long self- and cross-responses figures

Plots the figures of the short and long self- and cross-responses for the paper

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle

The module contains the following functions:
    * taq_responses_physical_short_long_year_plot - plots the short and long
      response for a year in physical physical scale.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import pickle

# ----------------------------------------------------------------------------


def taq_responses_physical_short_long_year_plot(ticker_i, ticker_j, year, tau,
                                                tau_p):
    """Plots the short and long response for a year.

    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL')
    :param year: string of the year to be analized (i.e '2008').
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
            figure = plt.figure(figsize=(16, 6))
            ax1 = plt.subplot(1, 2, 1)
            ax2 = plt.subplot(1, 2, 2)

            # Load data self-response
            (self_short,
            self_long,
            self_response,
            self_shuffle) = pickle.load(open(
                f'../../project/taq_data/responses_physical_short_long_data'
                + f'_{year}/taq_self_response_year_responses_physical_short'
                + f'_long_data_tau_{tau}_tau_p_{tau_p}/taq_self_response_year'
                + f'_responses_physical_short_long_data_tau_{tau}_tau'
                + f'_p_{tau_p}_{year}_{ticker_i}.pickle', 'rb'))

            # Addition of the short and long response signal
            sum = np.zeros(tau)
            sum[:tau_p + 1] = self_short[:tau_p + 1]
            sum[tau_p + 1:] = self_short[tau_p + 1:] + self_long[tau_p + 1:]

            ax1.semilogx(self_short, linewidth=5, label='Short')
            ax1.semilogx(self_long, linewidth=5, label='Long')
            ax1.semilogx(sum, linewidth=5, label='Sum')
            ax1.semilogx(self_response, linewidth=5, label='Self-response')
            ax1.semilogx(self_shuffle, linewidth=5, label='Shuffle')
            ax1.plot((tau_p, tau_p), (-1000, 1000), '--k', linewidth=5,
                     label=r"$\tau' $ = {}".format(tau_p))

            ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                       fontsize=15)
            ax1.set_xlabel(r'$\tau \, [s]$', fontsize=15)
            ax1.set_ylabel(r'$R^{sl,p}_{ii}(\tau)$', fontsize=15)
            ax1.tick_params(axis='x', labelsize=10)
            ax1.tick_params(axis='y', labelsize=10)
            ax1.set_xlim(1, 1000)
            ax1.set_ylim(-0.4 * 10 ** -4, 2.5 * 10 ** -4)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax1.yaxis.offsetText.set_fontsize(10)
            ax1.grid(True)

            # Load data cross-response
            (cross_short,
             cross_long,
             cross_response,
             cross_shuffle) = pickle.load(open(
                 f'../../project/taq_data/responses_physical_short_long_data'
                 + f'_{year}/taq_cross_response_year_responses_physical_short'
                 + f'_long_data_tau_{tau}_tau_p_{tau_p}/taq_cross_response'
                 + f'_year_responses_physical_short_long_data_tau_{tau}_tau'
                 + f'_p_{tau_p}_{year}_{ticker_i}i_{ticker_j}j.pickle', 'rb'))

            # Addition of the short and long response signal
            sum = np.zeros(tau)
            sum[:tau_p + 1] = cross_short[:tau_p + 1]
            sum[tau_p + 1:] = cross_short[tau_p + 1:] + cross_long[tau_p + 1:]

            ax2.semilogx(cross_short, linewidth=5, label='Short')
            ax2.semilogx(cross_long, linewidth=5, label='Long')
            ax2.semilogx(sum, linewidth=5, label='Sum')
            ax2.semilogx(cross_response, linewidth=5, label='Cross-response')
            ax2.semilogx(cross_shuffle, linewidth=5, label='Shuffle')
            ax2.plot((tau_p, tau_p), (-1000, 1000), '--k', linewidth=5,
                     label=r"$\tau' $ = {}".format(tau_p))

            ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                       fontsize=15)
            ax2.set_xlabel(r'$\tau \, [s]$', fontsize=15)
            ax2.set_ylabel(r'$R^{sl,p}_{ij}(\tau)$', fontsize=15)
            ax2.tick_params(axis='x', labelsize=10)
            ax2.tick_params(axis='y', labelsize=10)
            ax2.set_xlim(1, 1000)
            ax2.set_ylim(-1 * 10 ** -5, 1 * 10 ** -4)
            ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax2.yaxis.offsetText.set_fontsize(10)
            ax2.grid(True)

            plt.tight_layout()

            # Save plot
            figure.savefig(f'../plot/05_short_long_{ticker_i}_{ticker_j}.png')

            return None

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def main():

    year = '2008'

    taq_responses_physical_short_long_year_plot('GOOG', 'MA', year, 1000, 40)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
