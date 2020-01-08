/**
 * @file
 * Data structures for our in house binary data format (from here on called TAS) for TAQ data.
 *
 * The TAS format is designed with four requierements in mind:
 * 1. Reduce the size of the files needed to store the TAQ data by using compression.
 * 2. Make it easy and fast to retrieve data for a given data by using an index.
 * 3. Every symbol and exchange should have its own file for each year so it's possible to work with a subset of the whole database.
 * 4. Use checksums to find corrupted files.
 *
 * @author Thilo Schmitt
 */

#ifndef tas_tas_format_hpp
#define tas_tas_format_hpp

#include <boost/date_time.hpp>
#include "log.hpp"

#ifdef CHECKSUMS
#include <cryptopp/sha.h>
#endif

namespace tas {

/*!
 * @brief A structure representing the header of TAS trades or quotes file.
 *
 * The file starts with a 10 byte identifier that specifies either a trades file "TAS_TRADES"
 * or a quotes file "TAS_QUOTES".
 */
struct TASHeader {
    char identifier[10];            //!< TAS_TRADES or TAS_QUOTES
    unsigned char version;          //!< File format version number
    unsigned char ex;               //!< Exchange
    char symbol[12];                //!< Ticker symbol for stock
    unsigned char index_sha256[32]; //!< Checksum for index data
    unsigned long index_start;      //!< Start of the index
    unsigned long index_size;       //!> Size of the index
};

/*!
 * @brief A structure representing one index entry.
 *
 * The starting position of the index in a file is known from the TASHeader.
 * The index holds the starting position of all trades or quotes for a given date.
 * In addition it knows how many bytes of data for this date are stored and how large
 * the uncompressed data for this date will be.
 */
struct TASIndex {
    char date[10];                              //!< Date
    unsigned long offset;                       //!< Position of data for this date
    unsigned long size_compressed = 0;          //!< Size of compressed data for this date
    unsigned long size_uncompressed = 0;        //!< Size of uncompressed data for this date
    unsigned char sha256[32];                   //!< Checksum over the data for this date
};

/*!
 * @brief A structure representing one line of trades or quotes data.
 *
 * We use the same format for trade and quote data. As quotes contain more information
 * the data for trades is duplicated. This means that in case of trades file the fields
 * ask and bid both contain the traded price. The fields vol_ask and vol_bid both contain
 * the traded volume.
 *
 */
struct TASLine
{
    int time;               //!< Time in seconds since 00:00
    int bid;                //!< Price or bid
    int ask;                //!< Price or ask
    int vol_bid;            //!< Traded volume or volume at best bid
    int vol_ask;            //!< Traded volume or volume at best ask
    short mode_or_g127;     //!< Mode or rule g127
    short corr;             //!< Correction status of the trade
    char mmid_or_cond[4];   //!< Market maker id or condition
};

typedef std::map< boost::gregorian::date, TASIndex> TASIndexMap;


/*!
 * @brief Read the index from a TAS file.
 *
 *
 * @param Pointer to TASIndexMap object.
 * @return Returns "quotes" or "trades" depending on the given file.
 */
std::string read_index(std::string filename, TASIndexMap &bin_index )
{
    TASHeader head;

    //INFO( "Reading index from file: " << filename )

    std::string type;

    FILE* file = fopen(filename.c_str(), "rb");
    if (file) {
        fseek (file , 0, SEEK_SET);
        if ( fread ( (void *) &head, 1, sizeof(TASHeader), file ) == sizeof(TASHeader) ) {
            if ( strncmp("TAS_QUOTES", head.identifier, 10) != 0 && strncmp("TAS_TRADES", head.identifier, 10) != 0 ) {
                TASERR( "Not a valid TAS file!" );
            }
            if ( head.version != 1 ) {
                TASERR ( "Wrong version!" )
            }

            if ( strncmp("TAS_TRADES", head.identifier, 10) == 0 ) type = "trades";
            if ( strncmp("TAS_QUOTES", head.identifier, 10) == 0 ) type = "quotes";

            TASIndex* idx = (TASIndex*) malloc(head.index_size);
            fseek (file , head.index_start, SEEK_SET);
            if ( fread ( (void *) idx, 1, head.index_size, file ) == head.index_size ) {
#ifdef CHECKSUMS
                if ( !CryptoPP::SHA256().VerifyDigest(head.index_sha256, (unsigned char*) idx, head.index_size) ) {
                    std::cerr << "Checksum error in " << type << " index." << std::endl;
                    //exit(-1);
                }
#endif

                for (int c = 0; c < head.index_size / sizeof(TASIndex); ++c) {

                    //printf("%i %.10s %lu %lu %lu\n", c, idx[c].date, idx[c].offset, idx[c].size_compressed, idx[c].size_uncompressed );

                    boost::gregorian::date date( boost::gregorian::from_string( std::string(idx[c].date, 10) ) );

                    bin_index.insert( std::pair< boost::gregorian::date, TASIndex>(date, idx[c]) );

                }
            }
            free( idx );
        }
        fclose(file);
    } else {
        TASERR( "File " << filename << " does not exist." )
    }

    return type;
}

std::vector<TASLine> get_data( std::string filename, boost::gregorian::date day, TASIndexMap &bin_index )
{
    std::vector<TASLine> data;

    auto it_bin_index = bin_index.find( day );


    if ( it_bin_index != bin_index.end() ) {

        // Alloc memory for the uncompressed intraday data
        TASLine* uncompressed = (TASLine*) malloc(it_bin_index->second.size_uncompressed);

        // Alloc memory for the compressed intraday data
        unsigned char* compressed = (unsigned char*) malloc(it_bin_index->second.size_compressed);

        FILE* file = fopen(filename.c_str(), "rb");
        if ( file != NULL ) {
            fseek(file, it_bin_index->second.offset, SEEK_SET);

            if ( fread ( (unsigned char *) compressed, 1, it_bin_index->second.size_compressed, file ) == it_bin_index->second.size_compressed ) {

                int error = uncompress((unsigned char*) uncompressed, &it_bin_index->second.size_uncompressed, compressed, it_bin_index->second.size_compressed);

                if ( error == 0 ) {
#ifdef CHECKSUMS
                    if ( !CryptoPP::SHA256().VerifyDigest(&it_bin_index->second.sha256[0], (unsigned char*) uncompressed, it_bin_index->second.size_uncompressed) ) {
                        fprintf(stderr, "Checksum error\n");
                        //exit(0);
                    }
#endif
                } else {
                    TASERR( "gzip error: " << error << " in file " << filename )
                }
            }
            fclose(file);
        } else {
            printf("File not found.\n");
        }

        //TODO: Add a filter function

        for ( int i = 0; i < it_bin_index->second.size_uncompressed / sizeof(TASLine); ++i) {
            data.push_back( uncompressed[i] );
        }

        free(uncompressed);
        free(compressed);
    }

    return data;
}

}

#endif
