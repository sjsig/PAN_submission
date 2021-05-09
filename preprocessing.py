import xml.etree.ElementTree as ET
import emoji as em
import json
import os
import re
from unidecode import unidecode
from transformers import XLNetTokenizer
import random
import argparse
from transformers import pipeline


def parseData(lang="en", remove_emojis=False, convert_emojis=False, lowercase=False, model="XLNet", pct_to_remove=0, args=None):
    truth = open(os.path.join(args.base_dir, f'{args.data_dir}/{lang}/truth.txt'), 'r')
    authors = []
    data = []
    for line in truth.readlines():
        index = line.index(':')
        if(isinstance(index, int)):
            authors.append(line[:index])
    random.shuffle(authors)
    
    index = 0
    for author in authors:
        tree = ET.parse(os.path.join(args.base_dir, f"{args.data_dir}/{lang}/{author}.xml"))
        root = tree.getroot()
        author_data = dict()
        author_data["author"] = author 
        author_data["class"] = int(root.attrib["class"])
        author_data["lang"] = root.attrib["lang"]
        author_data["posts"] = []
        if(index < len(authors)*pct_val):
            author_data["set"] = 'test'
        else:
            author_data["set"] = 'train'
        
        for document in root.find('documents'):
            author_data["posts"].append(processTweet(document.text, lang, remove_emojis, convert_emojis, lowercase))
        
        data.append(author_data)
        index += 1
    
    text_file = open(os.path.join(base_dir, f'raw_data/{lang}/data.json'), "w")
    n = text_file.write(json.dumps(data, indent=4))
    text_file.close()
    
    return data

def processTweet(tweet, lang="en", remove_emojis=False, convert_emojis=False, lowercase=False):
    if(remove_emojis):
        emoji_list = em.emoji_lis(tweet, language=lang)
        for emoji in emoji_list:
            tweet = tweet.replace(emoji["emoji"], '')
    elif(convert_emojis):
        # better way to do this by removing repeats?
        tweet = em.demojize(tweet, language=lang, delimiters=(" ", ""))
    
    return_tweet = ""
    for character in tweet:
        try:
            character.encode("ascii")
            return_tweet += character
        except UnicodeEncodeError:
            # print(unidecode(character))
            if(em.emoji_count(character) == 0): # if it is not an emoji
                return_tweet += unidecode(character)
            else:
                return_tweet += character

    # Other things to try 
    # lower case text **
    # remove stop words 
    # treat character flooding 
    # clean out twitter specirfic elements such as RT, VIA, and FAV reserved words 
    # clean out other non-alphanumeric characters 
    # remove numbers *
    # remove punctuation
    # remove emojis **
    if(lowercase):
        return_tweet = return_tweet.lower()
    return return_tweet 



def parseRawData(lang="en", remove_emojis=False, convert_emojis=False, lowercase=False, model="XLNet", save_directory="processed_data", save_file=False, pct_to_remove=0, args=None):
    data = parseData(lang, remove_emojis, convert_emojis, lowercase, model, pct_to_remove, base_dir, pct_val)
    json_data = json.dumps(data, indent=4)
    
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)
    if not save_file:
        save_file = os.path.join(args.base_dir, f"{save_directory}/{lang}.json")
    
    text_file = open(save_file, "w")
    n = text_file.write(json_data)
    text_file.close()
    return (save_directory, save_file)


def createSet(saveDirectory, parsedFile, model, lang):
    with open(parsedFile) as json_file:
        data = json.load(json_file)
    
    test = []
    for author in data:    
        if(model=="XLNet"):
            total = ""
            for tweet in author["posts"]:
                total += tweet + ". "
    
            total += " <sep> <cls>"
            author["posts"] = total
            test.append(author)  
        elif(model=="BERT"):
            pass
        else:
            raise Exception("Enter either XLNet or BERT as model")

    test_file = f'{save_directory}/{lang}_test.tsv'

    with open(test_file, 'w') as the_file:
        for i in range(len(test)):
            label = ''
            if(test[i]['class']==0):
                label = 'notHate'
            else:
                label = 'hate'
            the_file.write(f"{test[i]['author']}\t{label}\t{test[i]['posts']}\n")
        the_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default="./data")
    parser.add_argument('--base_dir', type=str, default="./")
    args = parser.parse_args()

    lang="en"
    save_directory = "processed_data"
    save_directory = os.path.join(args.base_dir, save_directory)
    save_file = f"{save_directory}/{lang}.json"
    parseRawData(lang=lang, lowercase=True,  remove_emojis=True, save_directory=save_directory, save_file=save_file, args=args) 
    createSet(save_directory, save_file, "XLNet", lang)

    lang="es"
    save_directory = "processed_data"
    save_directory = os.path.join(args.base_dir, save_directory)
    save_file = f"{save_directory}/{lang}.json"
    parseRawData(lang=lang, lowercase=True,  remove_emojis=True, save_directory=save_directory, save_file=save_file, args=args) 
    createSet(save_directory, save_file, "XLNet", lang)
    