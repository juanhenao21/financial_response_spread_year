/* calculate the probabilities of sign persistence across non-trading period for real-time steps

Compile Command:
  cd /Users/wangss/Documents/program/C/TradingPhysics/IntradayData
  g++ /Users/wangss/Documents/program/C/program/TradeSignCompare/signprob.cpp -std=c++11 -lboost_date_time -lz -I/usr/local/include -L/usr/local/lib

Run Command:
./a.out 20081007_GS 20080211_XOM

Plot command:
 cd /Users/wangss/Documents/program/C/results_tradesign
 gnuplot plot.plt
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <map>
#include <zlib.h>
#include <math.h>
#include <algorithm>
#include <vector>

#include "func.hpp"

int main(int argc, const char *argv[])
{
    using namespace std;

    vector<string> filename;
    if(argc>0) {
        for (int i=1; i<argc; i++) {
            filename.push_back(argv[i]);
        }
    } else {
        exit(0);
    }

    //-----------------------------------Data input-----------------------------------------

    vector<vector<string>>data(argc-1);
    vector<vector<int>>time(argc-1);
    vector<vector<string>>ticker(argc-1);
    vector<vector<int>>order(argc-1);
    vector<vector<string>>type(argc-1);
    vector<vector<double>>shares(argc-1);
    vector<vector<double>>price(argc-1);
    
    
    for(int i=0; i<argc-1; i++) {
        int k=0;
        std::string line;
        ifstream Txt(filename[i]+".csv");
        if(Txt.is_open()) {
            while(std::getline(Txt,line)) {
                data[i].push_back(line);
                if(k!=0) {
                    int comma1 = line.find(',',0);
                    time[i].push_back(atof(line.substr(0,comma1).c_str()));
                    int comma2 = line.find(',',comma1 + 1);
                    ticker[i].push_back(line.substr(comma1 + 1,comma2-comma1-1).c_str());
                    int comma3 = line.find(',',comma2 + 1);
                    order[i].push_back(atoi(line.substr(comma2 + 1,comma3-comma2-1).c_str()));
                    int comma4 = line.find(',',comma3 + 1);
                    type[i].push_back(line.substr(comma3 + 1,comma4-comma3-1).c_str());
                    int comma5 = line.find(',',comma4 + 1);
                    shares[i].push_back(atof(line.substr(comma4 + 1,comma5-comma4-1).c_str()));
                    int comma6 = line.find(',',comma5 + 1);
                    price[i].push_back(atof(line.substr(comma5 + 1,comma6-comma5-1).c_str())/10000);
                }
                k++;
            }
        } else {
            exit(0);
        }
    }
    //------------------------------------------------------------------------------------------------

    //-----------------------------------Data filter: find transations--------------------------------


    vector<vector<int>>index_EFT(argc-1);
    vector<vector<int>>ordercode(argc-1);
    vector<vector<int>>shares_currentorder(argc-1);
    vector<vector<int>>time_currentorder(argc-1);
    vector<vector<double>>price_currentorder(argc-1);
    vector<vector<string>>type_currentorder(argc-1);
    vector<vector<string>>type_eachorder(argc-1);
    vector<vector<int>>time_eachorder(argc-1);
    vector<vector<int>>shares_eachorder(argc-1);
    vector<vector<double>>price_eachorder(argc-1);
    vector<vector<string>>type_transaction(argc-1);
    vector<vector<double>>price_transaction(argc-1);
    vector<vector<int>>volume_transaction(argc-1);
    vector<vector<double>>sign_e(argc-1);
    vector<vector<double>>sign_persecond_e(argc-1);
    vector<vector<int>>time_second(argc-1);
    

    for(int k=0; k<argc-1; k++) {
        if(time.size()==ticker.size()&&time.size()==order.size()&&time.size()==type.size()&&time.size()==shares.size()&&time.size()==price.size()) {
            // find out the order code and shares of current order executed in part (E) or in full (F) or non-displayed (T)
            for(int i=0; i<type[k].size(); i++) {
                if(strcmp(type[k][i].c_str(),"E")==0||strcmp(type[k][i].c_str(),"F")==0||strcmp(type[k][i].c_str(),"T")==0) {
                    index_EFT[k].push_back(i);
                    ordercode[k].push_back(order[k][i]);
                    shares_currentorder[k].push_back(shares[k][i]);
                    time_currentorder[k].push_back(time[k][i]);
                    price_currentorder[k].push_back(price[k][i]);
                    type_currentorder[k].push_back(type[k][i]);
                }
            }

            for(int i=0; i<index_EFT[k].size(); i++) {
                // find out the information list（time, type, shares, price）with the same order code in chronological order
                if( strcmp(type_currentorder[k][i].c_str(),"T")!=0) {
                    int volume_total;
                    for(int j=0; j<order[k].size(); j++) {
                        if(order[k][j]==ordercode[k][i]&& time[k][j]<=time[k][index_EFT[k][i]]) {
                            // only list the information before and of the current order
                            type_eachorder[k].push_back(type[k][j]);
                            time_eachorder[k].push_back(time[k][j]);
                            shares_eachorder[k].push_back(shares[k][j]);
                            price_eachorder[k].push_back(price[k][j]);
                        }
                    }
                    // determine the executed order type and price
                    for(int j=0; j<type_eachorder[k].size(); j++) {
                        if(strcmp(type_eachorder[k][j].c_str(),"B")==0||strcmp(type_eachorder[k][j].c_str(),"S")==0) {
                            if(j>0) {
                                printf("Warning: order %d has more than one buy or sell limit order!\n", ordercode[k][i]);
                            } else {
                                type_transaction[k].push_back(type_marketoder(type_eachorder[k][j]));
                                price_transaction[k].push_back(price_eachorder[k][j]);
                                volume_total=shares_eachorder[k][j];
                            }
                        }
                    }
                    // determine the volume of executed order in full ("F") and in part ("E")
                    if(strcmp(type_eachorder[k][type_eachorder[k].size()-1].c_str(),"F")==0) {
                        int volume=0;
                        for(int j=1; j<type_eachorder[k].size()-1; j++) {
                            if(strcmp(type_eachorder[k][j].c_str(),"E")==0) {
                                volume +=shares_eachorder[k][j];
                            } else {
                                break;
                            }
                        }
                        volume_transaction[k].push_back(volume_total-volume);
                    } else if(strcmp(type_eachorder[k][type_eachorder[k].size()-1].c_str(),"E")==0) {
                        volume_transaction[k].push_back(shares_currentorder[k][i]);
                    }
                    type_eachorder[k].clear();
                    time_eachorder[k].clear();
                    shares_eachorder[k].clear();
                    price_eachorder[k].clear();
                } else if( strcmp(type_currentorder[k][i].c_str(),"T")==0) {
                    type_transaction[k].push_back(type_currentorder[k][i]);
                    price_transaction[k].push_back(price_currentorder[k][i]);
                    volume_transaction[k].push_back(shares_currentorder[k][i]);
                }

            }
        } else {
            printf("Warning: the sizes of quantities are different.\n");
            printf("time size: %lu\n",time[k].size());
            printf("ticker size: %lu\n",ticker[k].size());
            printf("order size: %lu\n",order[k].size());
            printf("type size: %lu\n",type[k].size());
            printf("shares size: %lu\n",shares[k].size());
            printf("price size: %lu\n",price[k].size());
        }
        for(int i=0; i<index_EFT[k].size(); i++) {
            sign_e[k].push_back(type2sign(type_transaction[k][i]));
        }
        
        for(int j=0; j<57000000/1000-34800000/1000; j++){   // j is the time in the unit of seconds.
            double sum_sign_e=0;
            for(int i=0; i<index_EFT[k].size(); i++) {
                if(sign_e[k][i]!=2 && time_currentorder[k][i]/1000>=34800+j && time_currentorder[k][i]/1000<34801+j){
                    sum_sign_e+=sign_e[k][i];
                   // printf("%d %lf %d\n",j, sum_sign_e, time_currentorder[k][i]);
                }
                
            }
            if(sum_sign_e!=0){
                sign_persecond_e[k].push_back(sgn(sum_sign_e));
                time_second[k].push_back(34800+j); // in the unit of seconds.
            }
            sum_sign_e=0;
        }
        
        
        
        
        
        fprintf(stderr, "\rProgress: %3.2f%s", 100.0 / (argc-1) * (k+1), "%");
    }
    //--------------------------------------------------------------------------------------------


//----Probabilities of sign persistence across non-trading period of per transaction for same interval time-----

    vector<double>Ns,Nd,Ps,Pd,Lag0;
    double lag0=0;
    double lag1;
    int jj;
    while(jj<1000) { // j is the interval time .
        double ns=0;    // the number of the same sign.
        double nd=0;    // the number of different signs.
        if(jj<20){
            lag0=0.05*jj;
            lag1=0.05*jj+0.05;
            jj++;
        }else if(jj>=20 && jj<200){
            lag0=0.05*jj;
            lag1=0.05*jj+0.5;
            jj=jj+10;
        }else if(jj>=200 && jj<1000){
            lag0=0.05*jj;
            lag1=0.05*jj+5;
            jj=jj+100;
        }
        for(int k=0; k<argc-1; k++) {
            for(int i=0; i<index_EFT[k].size(); i++) {
                if(i>0) {
                    if(sign_e[k][i]!=2 && time_currentorder[k][i]>=34800000 && time_currentorder[k][i]<=57000000){
                        if(sign_e[k][i]==sign_e[k][i-1]&&time_currentorder[k][i]-time_currentorder[k][i-1]-1>lag0*1000 && time_currentorder[k][i]-time_currentorder[k][i-1]-1<=lag1*1000){
                            ns++;
                        }else if(sign_e[k][i]!=sign_e[k][i-1]&&time_currentorder[k][i]-time_currentorder[k][i-1]>lag0*1000 && time_currentorder[k][i]-time_currentorder[k][i-1]<=lag1*1000){
                            nd++;
                        }
                    }
                }
            }
        }
        Ns.push_back(ns);
        Nd.push_back(nd);
        Ps.push_back(ns/(ns+nd));
        Pd.push_back(nd/(ns+nd));
        Lag0.push_back(lag1);
        ns=0;
        nd=0;
    }

    ofstream cout;
    std::string name4 = "/Users/wangss/Documents/program/C/results_tradesign/SignProb.txt";
    cout.open(name4.c_str());
    for(int j=0; j<Ns.size(); j++) {
        cout<<Lag0[j] <<"   "<<Ns[j]<<"   "<<Nd[j]<<"   "<<Ps[j]<<"   "<<Pd[j]<<endl;
    }
    cout.close();
    
    
    
    //----Probabilities of sign persistence across non-trading period for real-time steps of per second--------
    
    vector<double>Ns_persecond,Nd_persecond,Ps_persecond,Pd_persecond,Lag0_persecond;
    for(int j=0; j<100; j++) { // j is the interval time .
        double ns_persecond=0;
        double nd_persecond=0;
        for(int k=0; k<argc-1; k++) {
            for(int i=0; i<sign_persecond_e[k].size(); i++) {
                if(i>0) {
                    if(sign_persecond_e[k][i]==sign_persecond_e[k][i-1]&&time_second[k][i]-time_second[k][i-1]-1>=1*j && time_second[k][i]-time_second[k][i-1]-1<1*j+1){
                            ns_persecond++;
                    }else if(sign_persecond_e[k][i]!=sign_persecond_e[k][i-1]&&time_second[k][i]-time_second[k][i-1]-1>=1*j && time_second[k][i]-time_second[k][i-1]-1<1*j+1){
                            nd_persecond++;
                    }
                }
            }
        }
        Ns_persecond.push_back(ns_persecond);
        Nd_persecond.push_back(nd_persecond);
        Ps_persecond.push_back(ns_persecond/(ns_persecond+nd_persecond));
        Pd_persecond.push_back(nd_persecond/(ns_persecond+nd_persecond));
        Lag0_persecond.push_back(j);
        ns_persecond=0;
        nd_persecond=0;
    }
    
    
    std::string name5 = "/Users/wangss/Documents/program/C/results_tradesign/SignProb_persecond.txt";
    cout.open(name5.c_str());
    for(int j=0; j<100; j++) {
        cout<<Lag0_persecond[j] <<"   "<<Ns_persecond[j]<<"   "<<Nd_persecond[j]<<"   "<<Ps_persecond[j]<<"   "<<Pd_persecond[j]<<endl;
    }
    cout.close();
    
    

    fprintf(stderr, "completed");
    fprintf(stderr, "\n");
    return 0;
}
