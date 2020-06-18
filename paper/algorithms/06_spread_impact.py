'''TAQ spread impact figures

Plots the figures of the spread impact self-responses for the paper

This script requires the following modules:
    * matplotlib
    * numpy
    * pickle

The module contains the following functions:
    * taq_self_response_year_avg_responses_physical_plot - plots the spread
      impact responses for a year in physical scale.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# ----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import pickle

# ----------------------------------------------------------------------------

def taq_self_response_year_avg_responses_physical_plot(year):
    """Plots the self-response average for a year.

    :param ticker: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2008').
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    try:
        # Load data
        resp_g1, resp_g2, resp_g3 = pickle.load(open(
            f'../../project/taq_data/avg_responses_physical_data_{year}/taq'
            + f'_self_response_year_avg_responses_physical_data/taq_self'
            + f'_response_year_avg_responses_physical_data_{year}_.pickle',
            'rb'))

        figure = plt.figure(figsize=(16, 9))
        ax = plt.subplot(111)

        plt.semilogx(resp_g1, linewidth=5, label=f'Group 1')
        plt.semilogx(resp_g2, linewidth=5, label=f'Group 2')
        plt.semilogx(resp_g3, linewidth=5, label=f'Group 3')

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3,
                   fontsize=30)
        plt.xlabel(r'$\tau \, [s]$', fontsize=30)
        plt.ylabel(r'$R_{ii}(\tau)$', fontsize=30)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.xlim(1, 1000)
        plt.ylim(19.5 * 10 ** -5, 32.5 * 10 ** -5)
        # plt.ylim(13 * 10 ** -5, 16 * 10 ** -5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(20)
        plt.grid(True)
        plt.tight_layout()

        # Save Plot
        figure.savefig(f'../plot/06_spread_impact_{year}.png')

        return None

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def main():

    year = '2008'

    taq_self_response_year_avg_responses_physical_plot(year)

    return None

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
