#!/bin/bash

cd ..

cd ..

cd TAQ_2008/Data

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
