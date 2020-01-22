TAQ Responses Second
********************

The objective of this part of the code is to reproduce the sections 3.1 and 3.2
of the paper `Cross–response in correlated financial markets:  individual
stocks
<https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.

This analysis is based on the data from NASDAQ stock market of the year 2008,
however, with small changes it could work for different years of the same data
source.
NASDAQ is a purely electronic stock exchange, whose Trades and Quotes (TAQ)
dataset contains the time, price and volume. This information is not only given
for the trades with all successive transactions, but also for the quotes with
all successive best buy and sell limit orders.

To analyze the response across different stocks, we select six companies (Apple
inc., Microsoft Corp., Goldman Sachs Group, JPMorgan Chase, Exxon Mobil Corp.
and Chevron Corp.) from three different economic sectors (information
technology, financials and energy) traded in the NASDAQ stock market in 2008.

The quote data and the trade data of each stock are in two separate files with
a time-stamp accuracy of one second.  However, more than one quote or trade may
be recorded in the same second.

Due to the one-second accuracy of the time-stamps, it is not possible to match
each trade with the directly preceding quote.  Hence, we cannot determine the
trade sign by comparing the traded price and the preceding midpoint. In this
case we need to do a preprocessing of the data to relate the midpoint prices
with the trade signs in trade time scale and in second time scale. Observe that
we will not be discussing the returns, but the midpoint price. This because
both are intrinsically related, as explain before, and it is more intuitive to
understand the changes in midpoint prices than in returns.

All the results obtained with the **TAQ Responses Second** modules are the base
to the other implementations (*escribir la lista de las otras carpetas*).
To run the full code in an easier way, I implemented the function
:py:func:`taq_data_main_responses_second.taq_build_from_scratch`. However,
running the main function :py:func:`taq_data_main_responses_second.main` will
do all the work.

Run from scratch
================

To run the code from the scratch and reproduce the results in section 2.3 and
2.4 of the `paper
<https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_, it is
needed to create three folders:

└── project

....├── taq_data

....│....└── original_year_data_2008

....└── taq_plot

The ``taq_data`` and ``taq_plot`` folder must be inside the ``project`` folder.
The ``original_year_data_2008`` must be inside the ``taq_data`` folder.

Then you need to move the ``.quotes`` and ``.trades`` files of the tickers you
want to analize into the folder ``original_year_data_2008``, and the
``decompress_original_data_2008`` folder to the ``taq_data`` folder.

Finally you need to access to the folder
``market_response_2008/project/taq_responses_second/taq_algorithms/`` and run
the module ``taq_data_main_responses_second.py``. This will obtain and plot the
data for the corresconding stocks.

Make it run, make it right, make it fast, make it small

Modules
=======
The code is divided in four parts:
    * `Tools`_: some functions for repetitive actions.
    * `Analysis`_: code to analyze the data.
    * `Plot`_: code to plot the data.
    * `Main`_: code to run the implementation.

Tools
-----
.. automodule:: taq_data_tools_responses_second
   :members:

Analysis
--------
.. automodule:: taq_data_analysis_responses_second
   :members:

Plot
----
.. automodule:: taq_data_plot_responses_second
   :members:

Main
----
.. automodule:: taq_data_main_responses_second
   :members:
