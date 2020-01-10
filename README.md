# Econophysics

### Juan Camilo Henao Londono
Student
Ph . D. Physics - Econophysics

[AG Guhr](http://www.theo.physik.uni-duisburg-essen.de/tp/ags/guhr_dir/index.html)

[Universität Duisburg-Essen](https://www.uni-due.de/)

To run the code from the scratch and reproduce the results in section 2.3 and 2.4 of the [paper](), it is needed to create
three folders:

|
|- project
 | - taq_data
 | |- original_year_data_2008
 | - taq_plot
 
The `taq_data` and `taq_plot` folder must be inside the `project` folder. The `original_year_data_2008` must be inside the
`taq_data` folder.

Then you need to move the `.quotes` and `.trades` files of the tickers you want to analize into the folder
`original_year_data_2008`. Finally you need to move to the folder 
`market_response_2008/project/taq_responses_second/taq_algorithms/` and run the module `taq_data_main_responses_second.py`. 
This will obtain and plot the data for the corresconding stocks. 

## Basic folder

Contains the first approach to the data and the algorithms used in the group. It has not useful information.

## Cross response individual stocks

Contains the information of the first work I made in the group. Here is the code I used to obtain the results. All the planification and issues were reported in this [Trello Board](https://trello.com/b/pJfWRI4u/econophysics-ph-d).
