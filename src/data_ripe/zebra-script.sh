#!/bin/bash
chmod +x zebra-dump-parser-modified.pl
for file in *.Z; do
zcat "$file" | ./zebra-dump-parser-modified.pl >>DUMP 2>>DUMPER
done
