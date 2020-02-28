.. _taq_responses_activity:

TAQ Responses Activity
**********************

We define the activity self- and cross-response functions in physical
time scale, using the trade signs and the returns in physical time scale.
We add a factor :math:`N_{j,d} \left(t \right)` to check the influence of the
frequency of trades in a second in the response functions.

To run this part of the code is necessary to have the results from the module
:ref:`taq_responses_physical`.

Modules
=======
The code is divided in four parts:
    * `Tools`_: some functions for repetitive actions.
    * `Analysis`_: code to analyze the data.
    * `Plot`_: code to plot the data.
    * `Main`_: code to run the implementation.

Tools
-----
.. automodule:: taq_data_tools_responses_activity
   :members:

Analysis
--------
.. automodule:: taq_data_analysis_responses_activity
   :members:

Plot
----
.. automodule:: taq_data_plot_responses_activity
   :members:

Main
----
.. automodule:: taq_data_main_responses_activity
   :members:
