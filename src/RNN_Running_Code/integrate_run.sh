#!/bin/bash

for f in $(find ./ -name 'save_memory_run.sh'); do 

	#echo "--------------------------------------------------------"
	echo "Current Experiment - " $f

	cd "$(dirname "$f")"
	chmod a+x ./save_memory_run.sh
	./save_memory_run.sh
	cd ..

done
