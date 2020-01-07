#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>


std::string time_format(int t) {
    div_t divresult;
    int ms,s,m,h,integer;
    divresult=div(t,1000);
    ms=divresult.rem;
    divresult=div(divresult.quot,60);
    s=divresult.rem;
    divresult=div(divresult.quot,60);
    m=divresult.rem;
    h=divresult.quot;
    std::stringstream ssms;
    std::stringstream sss;
    std::stringstream ssm;
    std::stringstream ssh;
    ssms << ms;
    std::string ms_str=ssms.str();
    sss << s;
    std::string s_str=sss.str();
    ssm << m;
    std::string m_str=ssm.str();
    ssh << h;
    std::string h_str=ssh.str();
    std::string time_format0=h_str+":"+m_str+":"+s_str+":"+ms_str;
    return(time_format0);
}

std::string type_marketoder(std::string s) {
    std::string markettype;
    if(strcmp(s.c_str(),"B")==0)
        markettype="S";
    if(strcmp(s.c_str(),"S")==0)
        markettype="B";
    return (markettype);
}

int sgn(double d) {
    if(d>0)
        return 1;
    else if(d<0)
        return -1;
    else
        return 0;
}

int type2sign(std::string s){
    int tradesign;
    if(strcmp(s.c_str(),"B")==0)
        tradesign=1;
    if(strcmp(s.c_str(),"S")==0)
        tradesign=-1;
    if(strcmp(s.c_str(),"T")==0)
        tradesign=2;
    return (tradesign);
}
