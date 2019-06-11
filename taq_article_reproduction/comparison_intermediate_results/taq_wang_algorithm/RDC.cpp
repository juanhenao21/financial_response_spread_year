/**
 Function: to calculate price response, diffusion function and sign correlation for each stock pair.

 Definition of trade signs:
 trade sign of n-th trade in time t: e_{n,t}=sign(p_{n,t}-p_{n-1,t});
 trade sign in time t: e_{t}=sum(e_{n,t});
 if there is no trade in time t, then e_{t}=0;

 Compile Command:
    cd  /directory of your file/data file
    g++ /directory of your file/RDC.cpp -std=c++11 -lboost_date_time -lz -I/usr/local/include -L/usr/local/lib

 Run Command: ./a.out XXX YYY (e.g. ./a.out AAPL MSFT)

 @author Shanshan Wang (shanshan.wang@uni-due.de)

 -.-.-

 This file was modified to make clear the computing process and to compare results of small parts of the code.

 Compile Command:

    g++ RDC.cpp -std=c++11 -lboost_date_time -lz -Iarmadillo-3.920.3/include -o cross.out

 Run Command

    ./cross.out XXX YYY (eg. ./cross.out AAPL MSFT)

 @modified Juan Henao (juan.henao-londono@stud.uni-due.de)
**/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sstream>
#include <map>
#include <zlib.h>
#include <math.h>
#include <algorithm>
#include <armadillo>
#ifdef CHECKSUMS
#include <cryptopp/sha.h>
#endif

#include "tas_format.hpp"


int sgn(double d) {
    if(d>0) {
        return 1;
    } else if(d<0) {
        return -1;
    } else {
        return 0;
    }
}

arma::mat vec2mat(std::vector<double> v) {
    using namespace arma;
    mat m(v.size(),1);
    for(int i=0; i<v.size();i++)
        m(i,0)=v[i];
    return m;
}

arma::vec vec2matvec(std::vector<double> v) {
    using namespace arma;
    vec m(v.size());
    for(int i=0; i<v.size();i++)
        m(i)=v[i];
    return m;
}


int main(int argc, const char *argv[])
{
    using namespace std;
    using namespace arma;

    std::string filename1;
    std::string filename2;
    if (argc == 3) {
        filename1 = argv[1];
        filename2 = argv[2];
    } else {
        exit(0);
    }

    std::string filename1_trades = "../../../taq_data/original_year_data_2008/" + filename1 + "_2008_NASDAQ.trades";
    std::string filename1_quotes = "../../../taq_data/original_year_data_2008/" + filename1 + "_2008_NASDAQ.quotes";
    std::string filename2_trades = "../../../taq_data/original_year_data_2008/" + filename2 + "_2008_NASDAQ.trades";
    std::string filename2_quotes = "../../../taq_data/original_year_data_2008/" + filename2 + "_2008_NASDAQ.quotes";

    tas::TASIndexMap index1_trades;
    tas::TASIndexMap index1_quotes;
    tas::TASIndexMap index2_trades;
    tas::TASIndexMap index2_quotes;

    std::string type1_trades = read_index(filename1_trades.c_str(), index1_trades);
    std::string type1_quotes = read_index(filename1_quotes.c_str(), index1_quotes);
    std::string type2_trades = read_index(filename2_trades.c_str(), index2_trades);
    std::string type2_quotes = read_index(filename2_quotes.c_str(), index2_quotes);


    // deal with data--------------------------------------------------------------------------------


    //(1.t)discard the first ten and last ten minutes of trading in a given day
    ofstream cout;

    std::vector<vector<double> >Date1_t, Price1_t, Volume1_t, E1;

    // Name of the folder and the file with the data of all the transactions for one day. I took the
    // first day in the data (2008-01-02) to simplify the analysis. However the code can be modified
    // to analyze other days.
    std::string nameP = "/scratch/jchenaol/econophysics/taq_data/article_reproduction_data_2008/wang/" + filename1 + "trade_signs_transactions.txt";
    cout.open(nameP.c_str());

    int count_juan = 0;
    int pos = 1; // Day of the year to be analyzed (in this case first transaction in the data)

    for (auto it1_t = index1_trades.begin(); it1_t != index1_trades.end(); it1_t++) {

        if (index1_quotes.find(it1_t->first) != index1_quotes.end() && index2_trades.find(it1_t->first) != index2_trades.end() && index2_quotes.find(it1_t->first) != index2_quotes.end()) {

            double price1_0, e1_n;
            double e1_n0=1;
            std::vector<double>day1_t(22200, 0), price1_t(22200, 0), volume1_t(22200, 0),e1(22200, 0),sum_e1(22200, 0);
            std::vector< tas::TASLine > data1_trades = get_data(filename1_trades.c_str(), it1_t->first, index1_trades);

            for (auto & d1_trades : data1_trades) {

                if (d1_trades.time <= 34800) {
                    price1_0=d1_trades.ask;
                }

                if (d1_trades.time >= 34801 && d1_trades.time <= 57000) {
                    day1_t[d1_trades.time-34801] = d1_trades.time;
                    //price1_t[d1_trades.time-34801] = d1_trades.ask;
                    price1_t[d1_trades.time-34801] = d1_trades.bid;

                    e1_n=sgn(d1_trades.ask-price1_0);
                    if(d1_trades.ask-price1_0==0) {
                        e1_n=e1_n0;
                    }

                    sum_e1[d1_trades.time-34801] +=e1_n;
                    price1_0=d1_trades.ask;
                    e1_n0=e1_n;

                    e1[d1_trades.time-34801]=sgn(sum_e1[d1_trades.time-34801]);
                    volume1_t[d1_trades.time-34801] += d1_trades.vol_ask;

                    count_juan += 1;

                    if (Date1_t.size() == pos - 1) // round - 1
                    {
                        cout << boost::gregorian::to_iso_extended_string(it1_t->first).c_str() << "   " << d1_trades.time << "   " << d1_trades.bid << "   " << e1_n << "   " << endl;
                    }
                }
            }

            cout.close();

            Date1_t.push_back(day1_t);
            Price1_t.push_back(price1_t);
            Volume1_t.push_back(volume1_t);
            E1.push_back(e1);

            count_juan = 0;

            if (Date1_t.size() == pos)
            {
                // Trade signs all trading day
                std::string name1t = "/scratch/jchenaol/econophysics/taq_data/article_reproduction_data_2008/wang/" + filename1 + "trade_signs_seconds.txt";
                cout.open(name1t.c_str());

                for (int i = 0; i < day1_t.size(); i++){
                    cout << i << "   " << Date1_t[pos - 1][i] <<"   "<< Price1_t[pos - 1][i] <<"   "<< E1[pos - 1][i] << endl;
                }

                cout.close();
            }

            day1_t.clear();
            price1_t.clear();
            volume1_t.clear();
            e1.clear();
            sum_e1.clear();
        }
    }

    //(1.q)discard the first ten and last ten minutes of trading in a given day

    std::vector<vector<double> >Date1_q, Mid1_q, Spread1_q;

    std::string nameM = "/scratch/jchenaol/econophysics/taq_data/article_reproduction_data_2008/wang/" + filename1 + "midpoint_transactions.txt";
    cout.open(nameM.c_str());


    for (auto it1_q = index1_quotes.begin(); it1_q != index1_quotes.end() ; it1_q++) {

        if (index1_trades.find(it1_q->first) != index1_trades.end() && index2_trades.find(it1_q->first) != index2_trades.end() && index2_quotes.find(it1_q->first) != index2_quotes.end()) {

            std::vector<double>day1_q(22200, 0), mid1_q(22200, 0), spread1_q(22200,0);
            std::vector<double> mid1_q2;
            std::vector< tas::TASLine > data1_quotes = get_data(filename1_quotes.c_str(), it1_q->first, index1_quotes);
            for (auto & d1_quotes : data1_quotes) {
                if (d1_quotes.time >= 34800 && d1_quotes.time <= 56999) {
                    day1_q[d1_quotes.time-34800] = d1_quotes.time;
                    mid1_q[d1_quotes.time-34800] = (d1_quotes.ask + d1_quotes.bid) / 2;
                    spread1_q[d1_quotes.time-34800] = (d1_quotes.ask -d1_quotes.bid) ;

                    if (Date1_q.size() == pos - 1) // round - 1
                    {
                        cout << boost::gregorian::to_iso_extended_string(it1_q->first).c_str() << "   " << d1_quotes.time << "   " << d1_quotes.bid << "   " << d1_quotes.ask << "   " <<(d1_quotes.ask + d1_quotes.bid) / 2 << "   " << d1_quotes.ask - d1_quotes.bid << endl;
                    }
                }
            }

            for (int i = 0; i < 22200; i++) {
                if (i != 0 && mid1_q[i] == 0) {
                    day1_q[i] = day1_q[i-1] + 1;
                    mid1_q[i] = mid1_q[i-1];
                    spread1_q[i] = spread1_q[i-1];
                }
            }
            for (int i = 22200; i >= 0; i--) {
                if (mid1_q[i] == 0) {
                    day1_q[i] = day1_q[i+1] - 1;
                    mid1_q[i] = mid1_q[i+1];
                    spread1_q[i] = spread1_q[i+1];
                }
            }

            Date1_q.push_back(day1_q);
            Mid1_q.push_back(mid1_q);
            Spread1_q.push_back(spread1_q);

            day1_q.clear();
            mid1_q.clear();
            spread1_q.clear();
        }
    }

    cout.close();

    // Print midpoint

    std::string name1q = "/scratch/jchenaol/econophysics/taq_data/article_reproduction_data_2008/wang/" + filename1 + "midpoint_seconds.txt";

    cout.open(name1q.c_str());

    for (int i=0; i < Mid1_q[1].size(); i++){

            cout << i <<"   "<< Date1_q[pos - 1][i] <<"   "<< Mid1_q[pos - 1][i] << endl;
    }

    cout.close();

    //(2.t)discard the first ten and last ten minutes of trading in a given day


    std::vector<vector<double> >Date2_t, Price2_t, Volume2_t, E2;
    for (auto it2_t = index2_trades.begin(); it2_t != index2_trades.end(); it2_t++) {

        if (index2_quotes.find(it2_t->first) != index2_quotes.end() && index1_trades.find(it2_t->first) != index1_trades.end() && index1_quotes.find(it2_t->first) != index1_quotes.end()) {

            double price2_0,e2_n;
            double e2_n0=1;
            std::vector<double>day2_t(22200, 0), price2_t(22200, 0), volume2_t(22200, 0), e2(22200,0), sum_e2(22200,0);
            std::vector< tas::TASLine > data2_trades = get_data(filename2_trades.c_str(), it2_t->first, index2_trades);
            for (auto & d2_trades : data2_trades) {
                if (d2_trades.time <= 34800) {
                    price2_0=d2_trades.ask;
                }

                if (d2_trades.time >= 34801 && d2_trades.time <= 57000) {
                    day2_t[d2_trades.time-34801] = d2_trades.time;
                    price2_t[d2_trades.time-34801] = d2_trades.ask;

                    e2_n=sgn(d2_trades.ask-price2_0);
                    if(d2_trades.ask-price2_0==0) {
                        e2_n=e2_n0;
                    }

                    sum_e2[d2_trades.time-34801] +=e2_n ;
                    price2_0=d2_trades.ask;
                    e2_n0=e2_n;

                    e2[d2_trades.time-34801]=sgn(sum_e2[d2_trades.time-34801]);

                    volume2_t[d2_trades.time-34801] += d2_trades.vol_ask ;
                }
            }

            Date2_t.push_back(day2_t);
            Price2_t.push_back(price2_t);
            Volume2_t.push_back(volume2_t);
            E2.push_back(e2);

            day2_t.clear();
            price2_t.clear();
            volume2_t.clear();
            e2.clear();
            sum_e2.clear();
        }
    }

    //(2.q)discard the first ten and last ten minutes of trading in a given day

    std::vector<vector<double> >Date2_q, Mid2_q, Spread2_q;
    for (auto it2_q = index2_quotes.begin(); it2_q != index2_quotes.end() ; it2_q++) {
        if (index2_trades.find(it2_q->first) != index2_trades.end() && index1_trades.find(it2_q->first) != index1_trades.end() && index1_quotes.find(it2_q->first) != index1_quotes.end()) {

            std::vector<double>day2_q(22200, 0), mid2_q(22200, 0), spread2_q(22200,0);
            std::vector<double> mid2_q2;
            std::vector< tas::TASLine > data2_quotes = get_data(filename2_quotes.c_str(), it2_q->first, index2_quotes);
            for (auto & d2_quotes : data2_quotes) {
                if (d2_quotes.time >= 34800 && d2_quotes.time <= 56999) {
                    day2_q[d2_quotes.time-34800] = d2_quotes.time;
                    mid2_q[d2_quotes.time-34800] = (d2_quotes.ask + d2_quotes.bid) / 2;
                    spread2_q[d2_quotes.time-34800] = (d2_quotes.ask - d2_quotes.bid) ;
                }
            }
            for (int i = 0; i < 22200; i++) {
                if (i != 0 && mid2_q[i] == 0) {
                    day2_q[i] = day2_q[i-1] + 1;
                    mid2_q[i] = mid2_q[i-1];
                    spread2_q[i] = spread2_q[i-1];
                }
            }
            for (int i = 22200; i >= 0; i--) {
                if (mid2_q[i] == 0) {
                    day2_q[i] = day2_q[i+1] - 1;
                    mid2_q[i] = mid2_q[i+1];
                    spread2_q[i] = spread2_q[i+1];
                }
            }

            Date2_q.push_back(day2_q);
            Mid2_q.push_back(mid2_q);
            Spread2_q.push_back(spread2_q);

            day2_q.clear();
            mid2_q.clear();
            spread2_q.clear();

        }
    }

    //caculate the response function, sign correlation------------------------------------------------

    int L=1000;
    unsigned long num = 0;
    double Rm, Cor;
    double R = 0;
    double C0 = 0;

    std::string name = "/scratch/jchenaol/econophysics/taq_data/article_reproduction_data_2008/wang/" + filename1 + "_" + filename2 + "_2008_RDC_L=1000.txt";

    cout.open(name.c_str());

    for (int l= 0; l<= L; l++) {
        for (int  i = 0; i < Date1_q.size(); i++) {
            for (int j = 0; j+l < 22200; j++) {
                if(E2[i][j]!=0) {
                    if(abs((Mid1_q[i][j+l] - Mid1_q[i][j])/Mid1_q[i][j])>1 || abs((Mid2_q[i][j+l] - Mid2_q[i][j])/Mid2_q[i][j])>1)
                        break;
                    R += (Mid1_q[i][j+l] - Mid1_q[i][j])/Mid1_q[i][j]* E2[i][j];
                    C0 += E1[i][j+l]* E2[i][j];

                    num++;
                }
            }
        }

        Rm = R / num;
        Cor = C0 / num;

        cout << l << "   " << fixed << setprecision(10) << Rm<<"   "<< Cor << "   " << num << endl;

        R = 0;
        C0 = 0;
        num=0;

        fprintf(stderr, "\rProgress: %3.2f%s", 100.0 / L * l, "%");
    }
    cout.close();

    fprintf(stderr, "completed");
    fprintf(stderr, "\n");

    return 0;
}
