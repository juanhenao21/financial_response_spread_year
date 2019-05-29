#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sstream>
#include <map>
#include <zlib.h>
#ifdef CHECKSUMS
#include <cryptopp/sha.h>
#endif

#include "tas_format.hpp"


// Convert seconds since midnight to time
std::string sec_to_time(int t)
{
    int h = t / 3600;
    int m = (t - h * 3600) / 60;
    int s =  t - h * 3600 - m * 60;

    char tmp[9];
    sprintf(tmp,"%.2d:%.2d:%.2d", h, m, s );

    return std::string(tmp);
}

int main (int argc, const char * argv[])
{
    std::string filename;

    if ( argc == 2 ) {
        filename = argv[1];
    } else {
        exit(0);
    }

    tas::TASIndexMap index;

    std::string type = read_index(filename.c_str(), index);

    unsigned long num = 0;
    for ( auto& it : index ) {
        num += it.second.size_uncompressed / sizeof(tas::TASLine);
    }

    unsigned long count = 0;
    for ( auto& it : index ) {
        std::vector< tas::TASLine > data = get_data(filename.c_str(), it.first, index);
        for ( auto& d : data ) {

            if ( type == "quotes" ) {
		// From 09h30 (34200 s) to 16h00 (57600)
		if (d.time >= 34200 && d.time <=57600){
             		printf("%.12s %i %i %i %i %i %i %.4s\n", boost::gregorian::to_iso_extended_string(it.first).c_str(), d.time, d.bid, d.ask, d.vol_bid, d.vol_ask, d.mode_or_g127, d.mmid_or_cond );
            	}
	    }
            if ( type == "trades" ) {
	    	if (d.time >= 34200 && d.time <=57600){
             		printf("%.12s %i %i %i %hi %hi %.2s\n", boost::gregorian::to_iso_extended_string(it.first).c_str(), d.time, d.ask, d.vol_ask, d.mode_or_g127, d.corr, d.mmid_or_cond );
            	}
            }

        }

        count += it.second.size_uncompressed / sizeof(tas::TASLine);
        fprintf(stderr,"\rProgress: %3.2f ", 100.0 / num * count );
    }
    fprintf(stderr,"\n");

    return 0;
}
