'''ITCH trade classification comparison

The functions in the module compare the trade classification values of the
section II.C of the `paper <https://arxiv.org/pdf/1603.01580.pdf>`_ with the
results of my implementation.
All the data is already calculated from the TotalView ITCH dataset. This script
gives the statistics of the similarities between the two data.

This script requires the following modules:
    * taq_data_analysis_article_reproduction
    * taq_data_tools_article_reproduction

The module contains the following functions:
    * taq_build_from_scratch - extract data to dayly CSV files.
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product
import multiprocessing as mp
import os
import pandas as pd
import pickle
import subprocess

import taq_data_analysis_article_reproduction
import taq_data_plot_article_reproduction
import taq_data_tools_article_reproduction

__tau__ = 1000

# -----------------------------------------------------------------------------


def taq_build_from_scratch(tickers, year):
    """ Extracts data to dayly CSV files.

    The original data must be decompressed. The function runs a script in
    C++ to decompress and then extract and filter the data for every day of a
    year in CSV files.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Check if there are extracted files from the list of stocks
    for ticker in tickers:
        if(os.path.isfile(
            '../../taq_data/csv_year_data_{1}/{0}_{1}_NASDAQ_quotes.csv'
            .format(ticker, year))
           and os.path.isfile(
               '../../taq_data/csv_year_data_{1}/{0}_{1}_NASDAQ_trades.csv'
               .format(ticker, year))):

            tickers.remove(ticker)

    # Compile and run the C++ script to decompress
    os.chdir('../../taq_data/decompress_original_data_{}/armadillo-3.920.3/'
             .format(year))
    subprocess.call('rm CMakeCache.txt', shell=True)
    subprocess.call('cmake .', shell=True)
    subprocess.call('make', shell=True)
    os.chdir('../')
    abs_path = os.path.abspath('.')
    os.system(
        'g++ main.cpp -std=c++11 -lboost_date_time -lz '
        + '-I {}/armadillo-3.920.3/include -o decompress.out'.format(abs_path))
    os.system('mv decompress.out ../original_year_data_{}/'.format(year))
    os.chdir('../original_year_data_{}'.format(year))

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        print('Extracting quotes')
        pool.starmap(taq_data_tools_article_reproduction.taq_decompress,
                     product(tickers, [year], ['quotes']))
    with mp.Pool(processes=mp.cpu_count()) as pool:
        print('Extracting trades')
        pool.starmap(taq_data_tools_article_reproduction.taq_decompress,
                     product(tickers, [year], ['trades']))

    subprocess.call('rm decompress.out', shell=True)
    subprocess.call('mv *.csv ../csv_year_data_{}/'.format(year), shell=True)

    # Extract dayly data
    with mp.Pool(processes=mp.cpu_count()) as pool:
        print('Extracting dayly data')
        pool.starmap(taq_data_analysis_article_reproduction.taq_data_extract,
                     product(tickers, ['quotes'], [year]))
        pool.starmap(taq_data_analysis_article_reproduction.taq_data_extract,
                     product(tickers, ['trades'], [year]))

    return None

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_article_reproduction.taq_bussiness_days(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Basic functions
        # pool.starmap(taq_data_analysis_article_reproduction.taq_midpoint_time_data,
        #              product(tickers, date_list))
        # pool.starmap(taq_data_analysis_article_reproduction.taq_trade_signs_time_data,
        #              product(tickers, date_list))

        # Especific functions
        pool.starmap(taq_data_analysis_article_reproduction.taq_self_response_year_data,
                     product(tickers, [year]))
        # pool.starmap(taq_data_analysis_article_reproduction.taq_cross_response_year_data,
        #              product(tickers, tickers, [year]))
        # pool.starmap(taq_data_analysis_article_reproduction
        #              .taq_trade_sign_self_correlator_year_data,
        #              product(tickers, [year]))
        # pool.starmap(taq_data_analysis_article_reproduction
        #              .taq_trade_sign_cross_correlator_year_data,
        #              product(tickers, tickers, [year]))

        pool.starmap(taq_data_plot_article_reproduction
                     .taq_self_response_year_avg_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot_article_reproduction
                     .taq_cross_response_year_avg_plot,
                     product(tickers, tickers, [year]))
        pool.starmap(taq_data_plot_article_reproduction
                     .taq_trade_sign_self_correlator_year_avg_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot_article_reproduction
                     .taq_trade_sign_cross_correlator_year_avg_plot,
                     product(tickers, tickers, [year]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    # Tickers and days to analyze
    tickers = ['AAPL']#, 'CVX', 'GS', 'JPM', 'MSFT', 'XOM']
    year = '2008'

    # Basic folders
    # taq_data_tools_article_reproduction.taq_start_folders(year)

    # Run analysis
    # taq_build_from_scratch(tickers, year)
    taq_data_plot_generator(tickers, year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
