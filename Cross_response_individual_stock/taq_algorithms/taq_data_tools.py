'''
TAQ data tools

Module with functions that help to make more readable the modules.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# TO DO: Docstrings!

# -----------------------------------------------------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os

import pickle

# -----------------------------------------------------------------------------------------------------------------------


def taq_save_data(function_name, data, ticker_i, ticker_j, year, month, day):
    """
    Save the data generated in taq_data_analysis module.
        :param function_name: name of the function that generates the data
        :param data: python data to be saved
        :param ticker_i: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
        :param month: string of the month to be analized (i.e '07')
        :param day: string of the day to be analized (i.e '07')
    """
    # Saving data

    if (not os.path.isdir('../taq_data_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../taq_data_{1}/{0}/'.
                     format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        pickle.dump(data, open(
            '../taq_data_{3}/{0}/{0}_{3}{4}{5}_{1}i_{2}j.pickle'
            .format(function_name, ticker_i, ticker_j, year, month, day),
            'wb'))

    else:

        pickle.dump(data, open(
            '../taq_data_{2}/{0}/{0}_{2}{3}{4}_{1}.pickle'
            .format(function_name, ticker_i, year, month, day), 'wb'))

    print('Data Saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_save_plot(function_name, figure, ticker_i, ticker_j, year, month):
    """
    Save the plots generated in itch_data_plot module.
        :param function_name: name of the function that generates the data
        :param figure: figure object that is going to be save
        :param ticker_i: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param t_step: time step in the data in ms
    """
    # Saving data

    if (not os.path.isdir('../taq_plot_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../taq_plot_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        figure.savefig(
            '../taq_plot_{3}/{0}/{0}_{3}{4}_{1}i_{2}j.png'
            .format(function_name, ticker_i, ticker_j, year, month))

    else:

        figure.savefig(
            '../taq_plot_{2}/{0}/{0}_{2}{3}_{1}i.png'
            .format(function_name, ticker_i, year, month))

    print('Plot saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_function_header_print_data(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """
    docstring here
        :param function_name:
        :param ticker_i:
        :param ticker_j:
        :param year:
        :param month:
        :param day:
    """

    print('TAQ data')
    print(function_name)

    if (ticker_i != ticker_j):
        print('Processing data for the stock i ' + ticker_i + ' and stock j '
              + ticker_j + ' the ' + year + '.' + month + '.' + day)
    else:
        print('Processing data for the stock ' + ticker_i + ' the ' + year
              + '.' + month + '.' + day)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_function_header_print_plot(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """
    docstring here
        :param function_name:
        :param ticker_i:
        :param ticker_j:
        :param year:
    """

    print('TAQ data')
    print(function_name)

    if (ticker_i != ticker_j):
        print('Processing plot for the stock i ' + ticker_i + ' and stock j '
              + ticker_j + ' the ' + year + '.' + month + '.' + day)
    else:
        print('Processing plot for the stock ' + ticker_i + ' the ' + year
              + '.' + month + '.' + day)

    return None

# -----------------------------------------------------------------------------------------------------------------------


def taq_start_folders(year):
    """
    docstring here
        :param year:
    """
    if (not os.path.isdir('../taq_data_{}/'.format(year))
            and not os.path.isdir('../taq_plot_{}/'.format(year))):

        try:

            os.mkdir('../taq_data_{}/'
                     .format(year))
            print('Folder to save data created')
            os.mkdir('../taq_plot_{}/'
                     .format(year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

# -----------------------------------------------------------------------------------------------------------------------


def get_sec(time_str):
    """
    Convert time format from hh:mm:ss to seconds
        :param time_str: string with the format hh:mm:ss (i. e. '09:40:00')
    """
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# -----------------------------------------------------------------------------------------------------------------------


def months_days_list(folder_path, ticker):
    """
    Generate two lists with the string with the numbers of the months
    (from '01' to '12') and the days of the data to be analyzed.
    """
    days = []
    days_list = []
    months_list = []

    for i in range(1, 32):
        if (i < 10):
            days.append('0' + str(i))
        else:
            days.append(str(i))

    for m in range(1, 13):
        if (m < 10):
            months_list.append('0' + str(m))
        else:
            months_list.append(str(m))

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for month in months_list:
        days_month = []
        for d in days:
            for file in files:
                val_split = file.split('_')
                date = val_split[-1].split('.')[0]
                val = val_split[1] + val_split[2] + date
                if (val == '{}quotes2008{}{}'.format(ticker, month, d)):
                    days_month.append(d)
        days_list += [days_month]

    return(months_list, days_list)

# -----------------------------------------------------------------------------

def main():
    folder_path = '../../TAQ_2008/TAQ_py/'
    a, b = months_days_list(folder_path, 'AAPL')
    print(a)
    print(b)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
