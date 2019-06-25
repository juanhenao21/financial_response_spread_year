#!/bin/bash

cd ..

cd ..

cd taq_data/original_year_data_2008/

echo 'Extracting quotes'

for f in *.quotes; do
    echo "Processing $f file"
    ./a.out $f > ${f%%.quotes}_quotes.csv
done

echo 'Extracting trades'

for f in *.trades; do
    echo "Processing $f file"
    ./a.out $f > ${f%%.trades}_trades.csv
done

echo 'Done'
