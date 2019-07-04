#!/usr/bin/env bash

for i in $(seq 1 8); do
    nice -n 19 python3 ddl.py ../datasets/examples/1_western_zodiac_examples.txt test.txt --complete 1 --prefix prefixes.txt --blacklist blacklist.txt --groupid 1
    grep SCORE test.txt | cut -d' ' -f3- | sort -k 2 > run_$i.txt
    rm test.txt
done

for i in $(set 2 8); do
    if ! cmp -s run_1.txt run_$i.txt; then
        echo "ERROR: SAME QUERY, DIFFERENT ANSWERS IN FILE 1 and $i"
        break
    fi
done

for i in $(seq 1 8); do
    rm run_$i.txt
done