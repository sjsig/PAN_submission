

input_dataset=$1
output_dir=$2
destination_folder='~/PAN_submission'

# Unzip input data
unzip ${input_dataset} -d ${destination_folder}

# Process xml files 
python preprocessing.py --data_dir ${destination_folder}

