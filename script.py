from transformers import AutoTokenizer, AutoModelForSequenceClassification, XLNetConfig, XLNetModel, AutoConfig
import torch
import json
import os
from mt_dnn.model import MTDNNModel

model_name = "xlnet-base-cased"
model_path = './models/en.pt'
data_path = './processed_data/en/data.json'

with open(data_path) as json_file:
    data = json.load(json_file)

# state_dict = torch.load(init_model, map_location=device)
state_dict=None
config = AutoConfig.from_pretrained(model_name).to_dict()
model = MTDNNModel(config, state_dict=state_dict)
model.load(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.eval()

# model = AutoModelForSequenceClassification.from_pretrained(model_path)
# device = torch.device('cuda', 1)
# state_dict = torch.load(model_path, map_location=device)

# print("trying", os.path.exists(model_path))
# model_state_dict = torch.load(model_path)
# print('Model dict')
# # print(model_state_dict)

# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# model.load_state_dict(model_state_dict["state_dict"])


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