'''TAQ data main module.

The functions in the module run the complete extraction, analysis and plot of
the TAQ data.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * os
    * pandas
    * pickle
    * taq_data_analysis_avg_responses_physical
    * taq_data_plot_avg_responses_physical
    * taq_data_tools_avg_responses_physical

The module contains the following functions:
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import os
import pandas as pd
import pickle

import taq_data_analysis_avg_responses_physical
import taq_data_plot_avg_responses_physical
import taq_data_tools_avg_responses_physical

# -----------------------------------------------------------------------------


def taq_data_plot_generator(year):
    """Generates all the analysis and plots from the TAQ data.

    :param div: integer of the number of divisions in the tickers (i.e. 5).
    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    tickers = taq_data_analysis_avg_responses_physical \
        .taq_tickers_spread_data(year)

    file = open('stocks.txt', 'w')
    for t_idx, ticker in enumerate(tickers):
        print(f'GROUP {t_idx + 1}')
        file.write(f'GROUP {t_idx + 1}\n')
        print(len(ticker))
        for t in ticker:
            # print(t)
            file.write(f'{t}\n')
        print(f'Number of tickers group {t_idx + 1}: {len(ticker)}')
        file.write(f'Number of tickers group {t_idx + 1}: {len(ticker)}\n')
        file.write('\n')
        print()
    file.close()

    taq_data_analysis_avg_responses_physical \
        .taq_self_response_year_avg_responses_physical_data(tickers, year)

    taq_data_plot_avg_responses_physical \
        .taq_self_response_year_avg_responses_physical_plot(year)

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    year = '2008'

    # Basic folders
    taq_data_tools_avg_responses_physical.taq_start_folders(year)

    # Run analysis
    # Analysis and plot
    taq_data_plot_generator(year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
