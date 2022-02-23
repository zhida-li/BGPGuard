#!/bin/bash
chmod +x zebra-dump-parser-modified.pl
for file in *.Z; do
zcat < "$file" | ./zebra-dump-parser-modified.pl >>DUMP 2>>DUMPER
done

# also can do:
#for file in *.gz; do
#zcat < "$file" | ./zebra-dump-parser-modified.pl >>DUMP 2>>DUMPER
#done
