/* filter transaction data from the data set of limit order book and calculate the accuracy of trade signs.

Compile Command:
  cd /Users/wangss/Documents/program/C/TradingPhysics/IntradayData
  g++ /Users/wangss/Documents/program/C/program/TradeSignCompare/filter_test_tradesign.cpp -std=c++11 -lboost_date_time -lz -I/usr/local/include -L/usr/local/lib

Run Command:
./a.out 20081007_GS

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

    std::string filename;
    if (argc == 2) {
        filename = argv[1];
    } else {
        exit(0);
    }

    //-----------------------------------Data input-----------------------------------------
    int k=0;
    std::string line;
    vector<string>data;
    vector<int>time;
    vector<string>ticker;
    vector<int>order;
    vector<string>type;
    vector<double>shares;
    vector<double>price;
    ifstream Txt(filename+".csv");
    if(Txt.is_open()) {
        while(std::getline(Txt,line)) {
            data.push_back(line);
            if(k!=0) {
                int comma1 = line.find(',',0);
                time.push_back(atof(line.substr(0,comma1).c_str()));
                int comma2 = line.find(',',comma1 + 1);
                ticker.push_back(line.substr(comma1 + 1,comma2-comma1-1).c_str());
                int comma3 = line.find(',',comma2 + 1);
                order.push_back(atoi(line.substr(comma2 + 1,comma3-comma2-1).c_str()));
                int comma4 = line.find(',',comma3 + 1);
                type.push_back(line.substr(comma3 + 1,comma4-comma3-1).c_str());
                int comma5 = line.find(',',comma4 + 1);
                shares.push_back(atof(line.substr(comma4 + 1,comma5-comma4-1).c_str()));
                int comma6 = line.find(',',comma5 + 1);
                price.push_back(atof(line.substr(comma5 + 1,comma6-comma5-1).c_str())/10000);
            }
            k++;
        }
    } else {
        exit(0);
    }
    //------------------------------------------------------------------------------------------------

    //-----------------------------------Data filter: find transations--------------------------------
    float tradenumber=0;
    float tradenumber_hiddenorder=0;
    float ordernumber_identified=0;
    float ordernumber_identified_2=0;

    vector<int>index_EFT;
    vector<int>ordercode;
    vector<int>shares_currentorder;
    vector<int>time_currentorder;
    vector<double>price_currentorder;
    vector<string>type_currentorder;
    vector<string>type_eachorder;
    vector<int>time_eachorder;
    vector<int>shares_eachorder;
    vector<double>price_eachorder;
    vector<string>type_transaction;
    vector<double>price_transaction;
    vector<int>volume_transaction;

    int pos;
    if(time.size()==ticker.size()&&time.size()==order.size()&&time.size()==type.size()&&time.size()==shares.size()&&time.size()==price.size()) {
        for(int i=0; i<time.size(); i++) {
            if(strcmp(type[i].c_str(),"E")==0||strcmp(type[i].c_str(),"F")==0||strcmp(type[i].c_str(),"T")==0)
                tradenumber++;
            if(strcmp(type[i].c_str(),"T")==0)
                tradenumber_hiddenorder++;
            if(strcmp(type[i].c_str(),"B")==0||strcmp(type[i].c_str(),"S")==0)
                ordernumber_identified++;
            if((strcmp(type[i].c_str(),"B")==0||strcmp(type[i].c_str(),"S")==0)&&time[i]>=34800000&&time[i]<=57000000)
                ordernumber_identified_2++;
        }
        //print filtering information to terminal and file
        printf("Total trade number: %f\n",tradenumber);
        printf("Hidden order number: %f\n",tradenumber_hiddenorder);
        printf("The proportion of hidden order in all executed order is %lf\n", tradenumber_hiddenorder/tradenumber);
        printf("Identified trade number: %f\n",tradenumber-tradenumber_hiddenorder);
        printf("Identified limit order number: %f\n",ordernumber_identified);
        printf("Identified limit order number between 9:40:00:000~15:50:00:000: %f\n",ordernumber_identified_2);



        // find out the order code and shares of current order executed in part (E) or in full (F) or non-displayed (T)
        for(int i=0; i<type.size(); i++) {
            if(strcmp(type[i].c_str(),"E")==0||strcmp(type[i].c_str(),"F")==0||strcmp(type[i].c_str(),"T")==0) {
                index_EFT.push_back(i);
                ordercode.push_back(order[i]);
                shares_currentorder.push_back(shares[i]);
                time_currentorder.push_back(time[i]);
                price_currentorder.push_back(price[i]);
                type_currentorder.push_back(type[i]);
            }
        }

        for(int i=0; i<index_EFT.size(); i++) {
            // find out the information list（time, type, shares, price）with the same order code in chronological order
            if( strcmp(type_currentorder[i].c_str(),"T")!=0) {
                int volume_total;
                for(int j=0; j<order.size(); j++) {
                    if(order[j]==ordercode[i]&& time[j]<=time[index_EFT[i]]) {
                        // only list the information before and of the current order
                        type_eachorder.push_back(type[j]);
                        time_eachorder.push_back(time[j]);
                        shares_eachorder.push_back(shares[j]);
                        price_eachorder.push_back(price[j]);
                    }
                }
                // determine the executed order type and price
                for(int j=0; j<type_eachorder.size(); j++) {
                    if(strcmp(type_eachorder[j].c_str(),"B")==0||strcmp(type_eachorder[j].c_str(),"S")==0) {
                        if(j>0) {
                            printf("Warning: order %d has more than one buy or sell limit order!\n", ordercode[i]);
                        } else {
                            type_transaction.push_back(type_marketoder(type_eachorder[j]));
                            price_transaction.push_back(price_eachorder[j]);
                            volume_total=shares_eachorder[j];
                        }
                    }
                }
                // determine the volume of executed order in full ("F") and in part ("E")
                if(strcmp(type_eachorder[type_eachorder.size()-1].c_str(),"F")==0) {
                    int volume=0;
                    for(int j=1; j<type_eachorder.size()-1; j++) {
                        if(strcmp(type_eachorder[j].c_str(),"E")==0) {
                            volume +=shares_eachorder[j];
                        } else {
                            break;
                        }
                    }
                    volume_transaction.push_back(volume_total-volume);
                } else if(strcmp(type_eachorder[type_eachorder.size()-1].c_str(),"E")==0){
                    volume_transaction.push_back(shares_currentorder[i]);
                }
                type_eachorder.clear();
                time_eachorder.clear();
                shares_eachorder.clear();
                price_eachorder.clear();
            } else if( strcmp(type_currentorder[i].c_str(),"T")==0) {
                type_transaction.push_back(type_currentorder[i]);
                price_transaction.push_back(price_currentorder[i]);
                volume_transaction.push_back(shares_currentorder[i]);
            }

        }
    } else {
        printf("Warning: the sizes of quantities are different.\n");
        printf("time size: %lu\n",time.size());
        printf("ticker size: %lu\n",ticker.size());
        printf("order size: %lu\n",order.size());
        printf("type size: %lu\n",type.size());
        printf("shares size: %lu\n",shares.size());
        printf("price size: %lu\n",price.size());
    }
    //--------------------------------------------------------------------------------------------

    //-------------------------print transaction data----------------------------------------------

    ofstream cout;
    std::string name1 = "./results_tradesign/transactions_"+filename+".txt";
    cout.open(name1.c_str());
    for(int i=0; i<index_EFT.size(); i++) {
        cout <<time_currentorder[i] <<"   "<<time_format(time_currentorder[i])<< "   "<< ordercode[i]<< "   " <<type_transaction[i] << "   " << price_transaction[i]<< "   " << volume_transaction[i]<<endl;
    }
    cout.close();
    //------------------------------------------------------------------------------------------------
    fprintf(stderr, "transaction filter is completed");
    fprintf(stderr, "\n\n");







    //--------------------------------Test accuracy of trade signs------------------------------------

    //--------------------------------1.test trade sign for every transaction---------------------------
    vector<double>sign_t(index_EFT.size(),0);
    vector<double>precios(index_EFT.size(),0);
    vector<double>sign_e;
    sign_t[0]=1;
    double same=0;
    double hidden=0;
    double total=0;
    double accuracy_transaction;
    for(int i=0; i<index_EFT.size(); i++) {
        if(i>0){
            if(price_transaction[i]!=price_transaction[i-1]){
                sign_t[i]=sgn(price_transaction[i]-price_transaction[i-1]);
                precios[i] = price_transaction[i];
            }
            else{
                sign_t[i]=sign_t[i-1];
                precios[i] = price_transaction[i];
            }
        }
        sign_e.push_back(type2sign(type_transaction[i]));
        if(sign_e[i]!=2 && time_currentorder[i]>=34800000 && time_currentorder[i]<=57000000){
            if(sign_t[i]-sign_e[i]==0)
                same++;
            total++;
        }else if(sign_e[i]==2 && time_currentorder[i]>=34800000 && time_currentorder[i]<=57000000){
            hidden++;
        }
    }
    accuracy_transaction=same/total;
    printf("The accuracy of sign for all transactions between 9:40:00~15:50:00 is: %lf\n",accuracy_transaction);
    printf("The number of identified transactions between 9:40:00~15:50:00 is: %lf\n",total);
    printf("The number of matched transactions between 9:40:00~15:50:00 is: %lf\n",same);
    printf("The number of hidden transactions between 9:40:00~15:50:00 is: %lf\n\n",hidden);
    std::string name2 = "./results_tradesign/SignCompare_transactions_"+filename+".txt";
    cout.open(name2.c_str());
    for(int i=0; i<index_EFT.size(); i++) {
        if(sign_e[i]!=2 && time_currentorder[i]>=34800000 && time_currentorder[i]<=57000000){
           cout<<i+1<<"   "<<time_currentorder[i] <<"   "<<time_format(time_currentorder[i])<<"   "<<sign_e[i]<<"   "<<sign_t[i]<<"   "<<precios[i]<<endl;
        }
    }
    cout.close();
    //--------------------------------2.test trade sign for every second--------------------------------
    double same_persecond1=0;
    double same_persecond2=0;
    double total_persecond=0;
    double accuracy_persecond1;
    double accuracy_persecond2;
    double num_sign0_1=0;
    double num_sign0_2=0;
    vector<double>sign_persecond_t1,sign_persecond_t2,sign_persecond_e;
    vector<int>time_second;
    for(int j=0; j<57000000/1000-34800000/1000; j++){
        double sum_sign_t1=0;
        double sum_sign_t2=0;
        double sum_sign_e=0;
        for(int i=0; i<index_EFT.size(); i++) {
            if(sign_e[i]!=2 && time_currentorder[i]/1000>=34800+j && time_currentorder[i]/1000<34801+j){
                sum_sign_t1+=sign_t[i];
                sum_sign_t2+=sign_t[i]*volume_transaction[i];
                sum_sign_e+=sign_e[i];
            }
        }
        sign_persecond_t1.push_back(sgn(sum_sign_t1));
        sign_persecond_t2.push_back(sgn(sum_sign_t2));
        sign_persecond_e.push_back(sgn(sum_sign_e));
        if(sign_persecond_t1[j]==0&&sign_persecond_t2[j]==0&&sign_persecond_e[j]==0){

        }else{
            if(sign_persecond_t1[j]-sign_persecond_e[j]==0)
                same_persecond1++;
            if(sign_persecond_t2[j]-sign_persecond_e[j]==0)
                same_persecond2++;
            total_persecond++;
        }
        if(sign_persecond_t1[j]==0)
            num_sign0_1++;
        if(sign_persecond_t2[j]==0)
            num_sign0_2++;

        time_second.push_back((34800+j)*1000);
    }
    accuracy_persecond1=same_persecond1/total_persecond;
    accuracy_persecond2=same_persecond2/total_persecond;


    printf("Case (1) The trade sign per second between 9:40:00~15:50:00 is defined as the sum of all the signs in this second. The accuracy is: %lf\n",accuracy_persecond1);
    printf("The seconds of identified transactions between 9:40:00~15:50:00 : %lf\n\n",total_persecond);
    printf("The seconds of matched transactions for Eq.(2) between 9:40:00~15:50:00 : %lf\n",same_persecond1);
    printf("Case (2) The trade sign per second between 9:40:00~15:50:00 is defined as the sum of all the signs multiplying trading volumes in this second. The accuracy is: %lf\n",accuracy_persecond2);
    printf("The seconds of matched transactions for Eq.(3) between f9:40:00~15:50:00 : %lf\n",same_persecond2);

    std::string name3 = "./results_tradesign/SignCompare_persecond_"+filename+".txt";
    cout.open(name3.c_str());
    for(int j=0; j<57000000/1000-34800000/1000; j++){
            cout<<time_second[j] <<"   "<<time_format(time_second[j])<<"   "<<sign_persecond_t1[j]<<"   "<<sign_persecond_t2[j]<<"   "<<sign_persecond_e[j]<<endl;
    }
    cout.close();







    //----------------------------------Print information to file---------------------------------------
    std::string name10 = "./results_tradesign/FilterTestInfo_"+filename+".txt";
    cout.open(name10.c_str());
    cout<<"The information for filtering transactions"<<endl;
    cout<<"Total trade number: "<<endl;
    cout<<tradenumber<<endl;
    cout<<"Hidden order number: "<<endl;
    cout<<tradenumber_hiddenorder<<endl;
    cout<<"The proportion of hidden order in all executed order: "<<endl;
    cout<< tradenumber_hiddenorder/tradenumber<<endl;
    cout<<"Identified limit order number: "<<endl;
    cout<<ordernumber_identified<<endl;
    cout<<"Identified limit order number between 9:40:00~15:50:00 : "<<endl;
    cout<<ordernumber_identified_2<<endl;
    cout<<"Identified trade number: "<<endl;
    cout<<tradenumber-tradenumber_hiddenorder<<endl;
    cout<<"The quantities of columns in file 'transactions_"<<filename<<".txt' are: "<<endl;
    cout<<"Time, Time in seconds, Order ID, Type of market order, Trading price, Trading volume."<<endl;
    cout<<"  "<<endl;
    cout<<"The information for sign accuracy of all transactions between 9:40:00~15:50:00"<<endl;
    cout<<"The number of identified transactions is: "<<endl;
    cout<<total<<endl;
    cout<<"The number of matched transactions is: "<<endl;
    cout<<same<<endl;
    cout<<"The number of hidden transactions is: "<<endl;
    cout<<hidden<<endl;
    cout<<"The accuracy of sign for all transactions is: "<<endl;
    cout<<accuracy_transaction<<endl;
    cout<<"The quantities of columns in file 'SignCompare_transactions_"<<filename<<".txt' are: "<<endl;
    cout<<"Number, Milliseconds,Time,Empirial sign, Theoretical sign"<<endl;
    cout<<"  "<<endl;
    cout<<"The information for sign accuracy of every second between 9:40:00~15:50:00"<<endl;
    cout<<"The seconds of identified transactions: "<<endl;
    cout<<total_persecond<<endl;
    cout<<"Case (1) The trade sign per second is defined as the sum of all the signs in this second."<<endl;
    cout<<"The seconds of matched transactions for case (1): "<<endl;
    cout<<same_persecond1<<endl;
    cout<<"The accuracy is: "<<endl;
    cout<<accuracy_persecond1<<endl;
    cout<<"Case (2) The trade sign per second is defined as the sum of all the signs multiplying trading volumes in this second."<<endl;
    cout<<"The seconds of matched transactions for case (2): "<<endl;
    cout<<same_persecond2<<endl;
    cout<<"The accuracy is: "<<endl;
    cout<<accuracy_persecond2<<endl;
    cout<<"The quantities of columns in file 'SignCompare_persecond_"<<filename<<".txt' are: "<<endl;
    cout<<"Seconds, Time, Empirial sign for case (1), Empirial sign for case (2), Theoretical sign for case (1)"<<endl;
    cout<<"  "<<endl;
    cout<<"Number of zero trade sign between 9:40:00~15:50:00"<<endl;
    cout<<"For Case (1)"<<endl;
    cout<<num_sign0_1<<endl;
    cout<<"For Case (2)"<<endl;
    cout<<num_sign0_2<<endl;
    cout.close();

    fprintf(stderr, "completed");
    fprintf(stderr, "\n");
    return 0;
}






