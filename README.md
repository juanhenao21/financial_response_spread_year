# Market response 2008

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://market-response-year.readthedocs.io/en/latest/)

In this repository, I analyze the market response for NASDAQ TAQ data for the
year 2008, however, it is possible to analyze data from other years with the
corresponding data.

I reproduce in the first part the sections 3.1 and 3.2 of the paper
[Cross-response in correlated financial markets: individual stocks](https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf)
to obtain the midpoint price, trade signs, self-response, cross-response, trade
sign self-correlator and trade sign cross-correlator values for different
stocks.

With these values, I analyze different characteristics of the responses (To be
done).

You can find [here](https://market-response-year.readthedocs.io/en/latest/)
a detailed documentation of the code.

## Getting Started

The main code is implemented in `Python`. As we use a particular data format,
it is necessary to extract the data from this format. To do that, is used a
`C++` module, however, all this process is automated with `Python`.

If you are interested in test the code, you can write us asking for some data
files examples, so we can share the files with you.

### Prerequisites

For `Python`, all the packages needed to run the analysis are in the


For the `C++` module compilation I used the `g++` compiler. It is necessary to
install the `-lboost_date_time` and the `armadillo-3.920.3` module (only for
Research group Guhr members).

## Running the code

The first step is clone the repository

```bash
$ git clone https://github.com/juanhenao21/market_response_year.git
```

To install all the `Pyton` packages needed I recommend to create a virtual
environment and install them from the `requirements.txt` file. To install the
packages from terminal, you can use

```bash
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### TAQ Responses Second

#### For the members of the research group Guhr

To run the code from the scratch and reproduce the results in section 2.3 and
2.4 of the
[paper](https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf),
you need to move (cd) to the folder
`market_response_year/project/taq_responses_second/taq_algorithms/` and run the
module `taq_data_main_responses_second.py`. In Linux, using the terminal the
command looks like

```bash
$ python3 taq_data_main_responses_second.py
```

The program will ask you which tickers will be used during the analysis and the
year of the analysis. After that, the program will ask you to move the
`.quotes` and `.trades` files of the tickers you want to analize into the
folder `market_response_year/project/taq_data/original_year_data_2008`, and the `decompress_original_data_2008`
folder to the `market_response_year/project/taq_data` folder.
After you move the folder to the location, the program will obtain and plot
the data for the corresponding stocks.

#### For the users with the year CSV data files

If you have the CSV data files, go to the
`market_response_year/project/taq_responses_second/taq_algorithms/taq_data_main_responses_second.py`
file and comment the line in the `main` function

```Python
# taq_build_from_scratch(tickers, year)
```

Then you need to run the module. In Linux, using the terminal, the command look
like

```bash
$ python3 taq_data_main_responses_second.py
```

The program will ask you to move the `CSV` files of the tickers you want to
analize into the folder `csv_year_data_2008`.
After you move the files to the corresponding place, the program will obtain
and plot the data for the stocks.

## Expected results

Explain what these tests test and why

```
Give an example
```

## Authors

* **Juan Camilo Henao Londono** - *Initial work* - [Website](https://juanhenao21.github.io)

## Acknowledgments

* DAAD Research Grants - Doctoral Programmes in Germany
* Research Group Guhr
