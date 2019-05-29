The programs are used for decompressing the TAQ data set, which includes
main.cpp
log.hpp
tas_format.cpp


Compile Commands: 
(in mac)
g++ /file directory…/main.cpp -std=c++11 -lboost_date_time -lz -I/usr/local/include -L/usr/local/lib 

(in university computer server)
g++ /file directory…/main.cpp -std=c++11 -lboost_date_time -lz -I/file directory…/armadillo-3.920.3/include


Run Commands:
(in terminal)
./a.out filename.trades
or
./a.out filename.quotes


The header file:
tas_format.hpp ; log.hpp

Library:
boost_date_time ;    armadillo-3.920.3 

 