#!/bin/sh

input_dataset=$1
output_dir=$2
destination_folder=~/PAN_submission
model=xlnet-base-cased
en_dir=./processed_data/en
es_dir=./processed_data/es
task_def=./twitter_task_def.yml
results_dir=results

# Process xml files 
echo 'Preprocessing xml files'
python3 preprocessing.py --data_dir ${input_dataset}

echo 'Prepro'
python3 mt-dnn/prepro_std.py --model ${model} --root_dir ${en_dir} --task_def ${task_def}

echo 'Predicting'
python3 mt-dnn/predict.py --task_def ${task_def} --task twitter --score ${results_dir}/en.json --checkpoint models/en.pt --prep_input processed_data/en/xlnet-base-cased/twitter_test.json

echo 'Generating output'
python3 generate_output.py --output_dir ${output_dir} --results_dir ${results_dir}