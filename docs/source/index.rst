.. Response function analysis documentation master file, created by
   sphinx-quickstart on Thu Aug 15 12:26:40 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Response function analysis' documentation!
==========================================
In this study, we have analyzed trades and quotes (TAQ) data from the NASDAQ
Stock Market.

In the TAQ data set, there are two data files for each stock. One gives the
list of all successive quotes. Thus, we have the best bid price, best ask
price, available volume and the time stamp accurate to the second. The other
data file is the list of all successive trades, with the traded price, traded
volume and time stamp accurate to the second. Despite the one second accuracy
of the time stamps, in both files more than one quote or trade may be recorded
in the same second.

In order to avoid overnight effects and any artifact due to the opening and
closing of the market, we systematically discarded the first ten and the last
ten minutes of trading in a given day.
Therefore, we only consider trades of the same day from 9:40:00 to 15:50:00
New York local time. We will refer to this interval of time as the "market
time".

The main objective of this work is to analyze the response functions. In
general we define the self- and cross-response functions in a correlated
financial market as

.. math::  R^{scale}_{ij}\left(\tau\right)=\left\langle r^{scale}_{i}\left(t-1,
    \tau\right) \cdot\varepsilon^{scale}_{j} \left(t\right)\right\rangle
    _{scale}

In the following can be seen the documentation of all the code used in the
project.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   01_taq_responses_physical

   02_taq_physical_shift

   03_taq_responses_physical_shift

   04_taq_responses_activity

   05_taq_responses_physical_short_long

   06_taq_responses_trade

   07_taq_trade_shift

   08_taq_responses_trade_shift

   09_taq_statistics

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
