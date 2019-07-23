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
import pandas as pd

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

    if (not os.path.isdir('../../taq_data/responses_event_trades_minute_data_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../../taq_data/responses_event_trades_minute_data_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        pickle.dump(data, open(''.join((
            '../../taq_data/responses_event_trades_minute_data_{3}/{0}/{0}_{3}{4}{5}'
            + '_{1}i_{2}j.pickle').split())
            .format(function_name, ticker_i, ticker_j, year, month, day),
            'wb'))

    else:

        pickle.dump(data, open(''.join((
            '../../taq_data/responses_event_trades_minute_data_{2}/{0}/{0}_{2}{3}{4}'
            '_{1}.pickle').split())
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

    if (not os.path.isdir('../../taq_plot/responses_event_trades_minute_plot_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../../taq_plot/responses_event_trades_minute_plot_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        figure.savefig(
            '../../taq_plot/responses_event_trades_minute_plot_{3}/{0}/{0}_{3}{4}_{1}i_{2}j.png'
            .format(function_name, ticker_i, ticker_j, year, month))

    else:

        figure.savefig(
            '../../taq_plot/responses_event_trades_minute_plot_{2}/{0}/{0}_{2}{3}_{1}.png'
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

# -----------------------------------------------------------------------------


def taq_bussiness_days(year):
    """
    Generate a list with the dates of the bussiness days in a year
        :param year: string of the year to be analized (i.e '2008')
    """
    init_date = '01/01/{}'.format(year)
    last_date = '12/31/{}'.format(year)

    # Use only the bussiness days
    dt = pd.date_range(start=init_date, end=last_date, freq='B')
    dt_df = dt.to_frame(index=False)
    date_list = dt_df[0].astype(str).tolist()

    return date_list

# -----------------------------------------------------------------------------


def main():
    folder_path = '../../TAQ_2008/TAQ_py/'
    a, b = months_days_list(folder_path, 'AAPL')
    print(a)
    print(b)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
