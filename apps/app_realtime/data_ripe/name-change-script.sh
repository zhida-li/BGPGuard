#/!bin/bash
for file in *.gz; do 
	mv "$file" "`basename $file .gz`.Z"
done
