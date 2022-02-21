#/!bin/bash
chmod +x zebra-dump-parser-modified.pl

for file in *.bz2; do
bzip2 -d "$file"
done

for file in updates.*; do
zcat -f < "$file" | ./zebra-dump-parser-modified.pl >>DUMP 2>>DUMPER
done
