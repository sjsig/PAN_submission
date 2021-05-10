from transformers import *
import torch

model_name = "xlnet-base-cased"
model_path = './models/en.pt'
data_path = './processed_data/en/data'

state_dict = torch.load(model_path)

model = AutoModelForSequenceClassification.from_pretrained(model_name, state_dict=state_dict)
tokenizer = AutoTokenizer.from_pretrained(model_name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dataset', type=float, default=0)
    parser.add_argument('--output_dir', type=float, default=.3)
    
    args = parser.parse_args()