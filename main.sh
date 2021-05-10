#!/bin/sh

input_dataset=$1
output_dir=$2
destination_folder=~/PAN_submission
model=xlnet-base-cased
en_dir=./processed_data/en
es_dir=./processed_data/es
task_def=./twitter_task_def.yml

# Process xml files 
echo 'Preprocessing xml files'
# python3 preprocessing.py --data_dir ${input_dataset}

echo 'Prepro'
# python3 mt-dnn/prepro_std.py --model ${model} --root_dir ${en_dir} --task_def ${task_def}

echo 'Predicting'
# python3 mt-dnn/predict.py --task_def ${task_def} --task twitter --score results/en --checkpoint models/en.pt --prep_input processed_data/en/xlnet-base-cased/twitter_test.json
python3 script.py