.. _taq_responses_physical_short_long:

TAQ Responses Time Short Long
*****************************

We use a time lag :math:`\tau` in the returns to see the gains or loses in a
future time. However, the strength of the return in the time lag should not be
equal along its length. Then, we divide the full range time lag :math:`\tau` in
an immediate time lag and in a late time lag.

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
.. automodule:: taq_data_tools_responses_physical_short_long
   :members:

Analysis
--------
.. automodule:: taq_data_analysis_responses_physical_short_long
   :members:

Plot
----
.. automodule:: taq_data_plot_responses_physical_short_long
   :members:

Main
----
.. automodule:: taq_data_main_responses_physical_short_long
   :members:
