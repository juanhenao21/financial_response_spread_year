''' TAQ data tools module.

The functions in the module do small repetitive tasks, that are used along the
whole implementation. These tools improve the way the tasks are standardized
in the modules that use them.

This script requires the following modules:
    * matplotlib
    * numpy
    * os
    * pandas
    * pickle

The module contains the following functions:
    * taq_save_data - saves computed data.
    * taq_save_plot - saves figures.
    * taq_function_header_print_data - prints info about the function running.
    * taq_function_header_print_plot - prints info about the plot.
    * taq_start_folders - creates folders to save data and plots.
    * taq_initial_data - takes the initial values for the analysis.
    * taq_business_days - creates a list of week days for a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle

# -----------------------------------------------------------------------------


def taq_save_data(function_name, data, ticker_i, ticker_j, year, month, day):
    """ Saves computed data in pickle files.

    Saves the data generated in the functions of the
    taq_data_analysis_avg_responses_physical module in pickle files.

    :param function_name: name of the function that generates the data.
    :param data: data to be saved. The data can be of different types.
    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param month: string of the month to be analyzed (i.e '07').
    :param day: string of the day to be analyzed (i.e '07').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Saving data

    if (not os.path.isdir(f'../../taq_data/avg_responses_physical_data_{year}/'
                          + f'{function_name}/')):

        try:
            os.mkdir(f'../../taq_data/avg_responses_physical_data_{year}/'
                     + f'{function_name}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    # Cross-response data
    if (ticker_i != ticker_j):

        pickle.dump(data, open(f'../../taq_data/avg_responses_physical_data'
                    + f'_{year}/{function_name}/{function_name}_{year}{month}'
                    + f'{day}_{ticker_i}i_{ticker_j}j.pickle', 'wb'))

    # Self-response data
    else:

        pickle.dump(data, open(f'../../taq_data/avg_responses_physical_data'
                    + f'_{year}/{function_name}/{function_name}_{year}{month}'
                    + f'{day}_{ticker_i}.pickle', 'wb'))

    print('Data Saved')
    print()

    return None

# -----------------------------------------------------------------------------


def taq_save_plot(function_name, figure, ticker_i, ticker_j, year, month):
    """Saves plot in png files.

    Saves the plot generated in the functions of the
    taq_data_plot_avg_responses_physical module in png files.

    :param function_name: name of the function that generates the plot.
    :param figure: figure object that is going to be save.
    :param ticker_i: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :param month: string of the month to be analyzed (i.e '07').
    :return: None -- The function save the plot in a file and does not return
     a value.
    """

    # Saving plot data

    if (not os.path.isdir(f'../../taq_plot/avg_responses_physical_plot_{year}'
                          + f'/{function_name}/')):

        try:
            os.mkdir(f'../../taq_plot/avg_responses_physical_plot_{year}/'
                     + f'{function_name}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    # Cross-response data
    if (ticker_i != ticker_j):

        figure.savefig(f'../../taq_plot/avg_responses_physical_plot_{year}/'
                       + f'{function_name}/{function_name}_{year}{month}'
                       + f'_{ticker_i}i_{ticker_j}j.png')

    # Self-response
    else:

        figure.savefig(f'../../taq_plot/avg_responses_physical_plot_{year}/'
                       + f'{function_name}/{function_name}_{year}{month}'
                       + f'_{ticker_i}.png')

    print('Plot saved')
    print()

    return None

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
              + f'{ticker_j} the {year}.{month}.{day}')
    # Self-response data
    else:
        print(f'Processing data for the stock {ticker_i} the '
              + f'{year}.{month}.{day}')

    return None

# -----------------------------------------------------------------------------


def taq_function_header_print_plot(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """Prints a header of a function that generates a plot when it is running.

    :param function_name: name of the function that generates the plot.
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
        print(f'Processing plot for the stock i {ticker_i} and stock j '
              + f'{ticker_j} the {year}.{month}.{day}')
    # Self-response data
    else:
        print(f'Processing plot for the stock {ticker_i} the '
              + f'{year}.{month}.{day}')

    return None

# -----------------------------------------------------------------------------


def taq_start_folders(year):
    """Creates the initial folders to save the data and plots.

    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function creates folders and does not return a value.
    """

    try:
        os.mkdir(f'../../taq_plot/avg_responses_physical_plot_{year}')
        os.mkdir(f'../../taq_data/avg_responses_physical_data_{year}')

        print('Folder to save data created')
        print()

    except FileExistsError as e:
        print('Folder exists. The folder was not created')
        print(e)
        # raise Exception('Check the folders')

    return None

# -----------------------------------------------------------------------------


def taq_initial_data():
    """Takes the initial values for the analysis

    :return: None -- The function prints the message and does not return a
     value.
    """

    print()
    print('#################################################')
    print('Average Response Functions Physical Time Analysis')
    print('#################################################')
    print('AG Guhr')
    print('Faculty of Physics')
    print('University of Duisburg-Essen')
    print('Author: Juan Camilo Henao Londono')
    print('More information in:')
    print('  * https://juanhenao21.github.io/')
    print('  * https://github.com/juanhenao21/spread_impact_analysis')
    print('  * https://spread-impact-analysis.readthedocs.io/en/latest/')
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
