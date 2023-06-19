


if [ -d "./res_acc" ]; then
	rm -r res_acc
fi

if [ -d "./res_run" ]; then
	rm -r res_run
fi



mkdir res_acc
mkdir res_run




for f in $(find ./experiment/* -name '*_accuracy.txt'); do 

	cp $f ./res_acc/
	

done

for f in $(find ./experiment/* -name '*_runtime.txt'); do 

	cp $f ./res_run/


done