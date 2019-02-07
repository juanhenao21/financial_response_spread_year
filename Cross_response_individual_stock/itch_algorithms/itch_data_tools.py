'''
ITCH data tools

Module with functions that help to make more readable the modules.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# -----------------------------------------------------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os

import pickle

# -----------------------------------------------------------------------------------------------------------------------


def trade_sign_reshape(trade_sign, time_t_step):
    """
    Reshape the trade sign data according to the t_step used. Returns a tuple
    with two arrays. A + 1 (- 1) array when the values of the sum is greater
    (smaller) than zero and an array with the places in the string that are
    not zero.
        :param trade_sign: array with the trade sign data
        :param time_t_step: array with the time adjusted to t_step resolution
    """

    # Reshape the array in group of values of t_step ms and infer the number
    # of rows, then sum all rows.
    trade_sign_j_sec_sum = np.sum(np.reshape(
                                  trade_sign, (len(time_t_step), -1)),
                                  axis=1)

    # Reasign the trade sign, if the value of the array is greater than 0
    # gives a 1 and -1 for the contrary.
    trade_sign_j_sec_avg = 1 * (trade_sign_j_sec_sum > 0)\
        - 1 * (trade_sign_j_sec_sum < 0)
    # Reshape the array in group of values of t_step ms and infer the number
    # rows, then sum the absolute value of all rows. This is used to know
    # where a trade sign is cero.
    trade_sign_j_sec_nr = np.sum(np.reshape(np.absolute(trade_sign),
                                 (len(time_t_step), -1)), axis=1)

    return (trade_sign_j_sec_avg, trade_sign_j_sec_nr)

# -----------------------------------------------------------------------------------------------------------------------


def save_data(function_name, data, ticker_i, ticker_j, day, t_step):
    """
    Save the data generated in itch_data_generator module.
        :param function_name: name of the function that generates the data
        :param data: python data to be saved
        :param ticker_i: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the stock to be analized
         (i.e. 'AAPL')
        :param day: string of the day to be analized (i.e '07')
        :param t_step: time step in the data in ms
    """
    # Saving data

    if (not os.path.isdir('../Data/{}_{}ms/'
                          .format(function_name, t_step))):

        try:

            os.mkdir('../Data/{}_{}ms/'.format(function_name, t_step))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        pickle.dump(data, open(
            '../Data/{}_{}ms/{}_201603{}_{}i_{}j_{}ms.pickl'
            .format(function_name, t_step, function_name, day, ticker_i,
                    ticker_j, t_step), 'wb'))

    else:

        pickle.dump(data, open(
            '../Data/{}_{}ms/{}_201603{}_{}i_{}ms.pickl'
            .format(function_name, t_step, function_name, day, ticker_i,
                    t_step), 'wb'))

    print('Data Saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def save_plot(function_name, figure, ticker_i, ticker_j, t_step):
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

    if (not os.path.isdir('../Plots/{}_{}ms/'
                          .format(function_name, t_step))):

        try:

            os.mkdir('../Plots/{}_{}ms/'.format(function_name, t_step))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    if (ticker_i != ticker_j):

        figure.savefig(
            '../Plots/{}_{}ms/{}_{}i_{}j_{}ms.png'
            .format(function_name, t_step, function_name, ticker_i,
                    ticker_j, t_step))

    else:

        figure.savefig(
            '../Plots/{}_{}ms/{}_{}i_{}ms.png'
            .format(function_name, t_step, function_name, ticker_i, t_step))

    print('Plot saved')
    print()

    return None

# -----------------------------------------------------------------------------------------------------------------------


def main():

    return None


if __name__ == '__main__':
    main()
