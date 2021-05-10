from transformers import *
import torch
import json

model_name = "xlnet-base-cased"
model_path = './models/en.pt'
data_path = './processed_data/en/data.json'

with open(data_path) as json_file:
    data = json.load(json_file)

state_dict = torch.load(model_path)

model = AutoModelForSequenceClassification.from_pretrained(model_name, state_dict=state_dict)
tokenizer = AutoTokenizer.from_pretrained(model_name)

for author in data:
    tweets = author["posts"]
    lang = author["lang"]
    uid = author["author"]
    inputs = tokenizer(tweets, return_tensors="pt", add_special_tokens=False)
    outputs = model(**inputs)
    print(uid)
    print(outputs)



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--input_dataset', type=float, default=0)
#     parser.add_argument('--output_dir', type=float, default=.3)
    
#     args = parser.parse_args()