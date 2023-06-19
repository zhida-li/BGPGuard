#!/bin/bash

chmod +x collect.sh
# Parameters

epoch=30

hidden_size1=80
hidden_size2=32
hidden_size3=16

num_layers=1  # rnn layer

declare -a dir_names=(
	"lstm_2layer_batch5" 
	"lstm_2layer_batch10" 
	"lstm_2layer_batch20" 

	"lstm_3layer_batch5" 
	"lstm_3layer_batch10" 
	"lstm_3layer_batch20" 
	
	"lstm_4layer_batch5" 
	"lstm_4layer_batch10" 
	"lstm_4layer_batch20" 
	
	"gru_2layer_batch5" 
	"gru_2layer_batch10" 
	"gru_2layer_batch20" 
	
	"gru_3layer_batch5" 
	"gru_3layer_batch10" 
	"gru_3layer_batch20" 


	"gru_4layer_batch5" 
	"gru_4layer_batch10" 
	"gru_4layer_batch20" 
	
	)


# Move to target directory

if [ -d "./experiment" ]; then
	rm -r experiment
fi


if [ -d "./tmp" ]; then
	rm -r tmp
fi

if [ -d "./res_acc" ]; then
	rm -r res_acc
fi

if [ -d "./res_run" ]; then
	rm -r res_run
fi



mkdir experiment
cd experiment



# Create folders

for i in "${dir_names[@]}"
do
   mkdir "$i"
done





# Copy python code to corresponding directory

mkdir ../tmp
cp ../code_template/* ../tmp/




## Replace global config macro

for filenames in ../tmp/*; do

	#echo $filenames
	sed -i -e 's/NUM_EPOCHS_HERE/'$epoch'/g' $filenames
	sed -i -e 's/NUM_OF_LAYER_HERE/'$num_layers'/g' $filenames
	
	if [[ $filenames == *"1layer"* ]]; then
		sed -i -e 's/HIDDEN_SIZE_3_HERE/'$hidden_size1'/g' $filenames
	elif [[ $filenames == *"2layer"* ]]; then
		sed -i -e 's/HIDDEN_SIZE_2_HERE/'$hidden_size1'/g' $filenames
		sed -i -e 's/HIDDEN_SIZE_3_HERE/'$hidden_size2'/g' $filenames
	else
		sed -i -e 's/HIDDEN_SIZE_1_HERE/'$hidden_size1'/g' $filenames
		sed -i -e 's/HIDDEN_SIZE_2_HERE/'$hidden_size2'/g' $filenames
		sed -i -e 's/HIDDEN_SIZE_3_HERE/'$hidden_size3'/g' $filenames
	fi


done


## Copy to target location


declare -a code_name_pattern=(
	"lstm_2layer"
	"lstm_3layer"
	"lstm_4layer"

	"gru_2layer"
	"gru_3layer"
	"gru_4layer"

	)





for str_pattern in "${code_name_pattern[@]}"
do
   
	for filenames in *; do

		if [[ $filenames == *$str_pattern* ]]; then

			for code_template_filename in ../tmp/*; do

				if [[ $code_template_filename == *$str_pattern* ]]; then

					cp ../tmp/$code_template_filename $filenames/

				fi
			done
		fi
	done
done




counter=0






for f in $(find ./ -name '*.py'); do 


	#echo $(basename $(dirname $f))
	
	cp ../dataset/train.csv $(basename $(dirname $f))/
	cp ../dataset/test.csv $(basename $(dirname $f))/
			

	python3 $f
	wait
	((counter++))
	
	echo '('$counter' / 18) : '$f 


	rm -r $(basename $(dirname $f));





done





#echo "------------------------------------------------"
#echo "end"

