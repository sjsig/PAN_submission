

input_dataset=$1
output_dir=$2
destination_folder='~/PAN_submission'

# Process xml files 
python3 preprocessing.py --data_dir ${input_dataset}

