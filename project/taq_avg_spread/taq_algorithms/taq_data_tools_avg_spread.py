''' TAQ data tools module.

The functions in the module do small repetitive tasks, that are used along the
whole implementation. These tools improve the way the tasks are standardized
in the modules that use them.

This script requires the following modules:
    * matplotlib
    * os
    * pandas
    * pickle

The module contains the following functions:
    * taq_function_header_print_data - prints info about the function running.
    * taq_initial_message - prints the initial message with basic information.
    * taq_business_days - creates a list of week days for a year.
    * taq_get_tickers_data - gets the available ticker names.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import os
import pandas as pd
import pickle

# -----------------------------------------------------------------------------


def taq_function_header_print_data(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """Prints a header of a function that generates data when it is running.

    :param function_name: name of the function that generates the data.
    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param month: string of the month to be analyzed (i.e '07').
    :param day: string of the day to be analyzed (i.e '07').
    :return: None -- The function prints a message and does not return a
     value.
    """

    print('TAQ data')
    print(function_name)

    # Cross-response data
    if (ticker_i != ticker_j):
        print(f'Processing data for the stock i {ticker_i} and stock j '
              + f'{ticker_j} the {year}.{month}.{day}.')
    # Self-response data
    else:
        print(f'Processing data for the stock {ticker_i} the '
              + f'{year}.{month}.{day}.')

    return None

# -----------------------------------------------------------------------------


def taq_initial_message():
    """Prints the initial message with basic information.

    :return: None -- The function prints a message and does not return a value.
    """

    print()
    print('##############')
    print('Average Spread')
    print('##############')
    print('AG Guhr')
    print('Faculty of Physics')
    print('University of Duisburg-Essen')
    print('Author: Juan Camilo Henao Londono')
    print('More information in:')
    print('* https://juanhenao21.github.io/')
    print('* https://github.com/juanhenao21/financial_response_spread_year')
    print('* https://financial-response-spread-year.readthedocs.io/en/latest/')
    print()

    return None

# -----------------------------------------------------------------------------


def taq_bussiness_days(year):
    """Generates a list with the dates of the bussiness days in a year

    :param year: string of the year to be analyzed (i.e '2008').
    :return: list.
    """

    init_date = f'01/01/{year}'
    last_date = f'12/31/{year}'

    # Use only the bussiness days
    dt = pd.date_range(start=init_date, end=last_date, freq='B')
    dt_df = dt.to_frame(index=False)
    date_list = dt_df[0].astype(str).tolist()

    return date_list

# ----------------------------------------------------------------------------


def taq_get_tickers_data(year):
    """Gets the available ticker names.

    :param year: string of the year to be analyzed (i.e '2016').
    :return: list -- The function returns a list with the name of the tickers.
    """

    # Obtain the absolute path of the current file and split it
    abs_path = os.path.abspath(__file__).split('/')
    # Take the path from the start to the project folder
    root_path = '/'.join(abs_path[:abs_path.index('project') + 1])
    f_path = root_path + f'/taq_data/hdf5_daily_data_{year}'
    files = os.listdir(f_path)

    tickers = []

    # Get the ticker symbols
    for file in files:
        tickers.append(file.split('_')[1])

    tickers = list(set(tickers))

    return tickers

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    pass

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
