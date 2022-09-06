# Abhijeet Padhy

import json
import os
import constants as CONST
import pickle

unique_user_ids = {"DUMMY"}

init_path = 'X:\\fakenewsnet_dataset\\data_network_new\\'
# directories = ['gossipcop_fake', 'gossipcop_real', 'politifact_fake', 'politifact_real']

# finding the dataset where we have to modify
directories = []
for label in CONST.LABELS:
    directories.append("{}_{}".format("gossipcop", label))
print(directories)

def handle_children(element):
    if 'children' not in element:
        return
    for child in element['children']:
        user_id = child['user']
        #print("The child's user is " + str(user_id))
        unique_user_ids.add(user_id)
        handle_children(child)

for my_dir in directories:
    print("The dir is " + my_dir)
    list_of_news = os.listdir(init_path + my_dir)
    print(list_of_news)
    for news in list_of_news:
        #print("The news is " + news)
        json_file_path = init_path + my_dir + '\\' + news
        print(json_file_path)
        try:
            json_file = open(json_file_path)
        except:
            print("This file {} is not found!".format(json_file_path))
            continue
        json_data = json.load(json_file)
        for network_tweets in json_data['children']:
            user_id = network_tweets['user']
            #print("The user is " + str(user_id))
            unique_user_ids.add(user_id)
            #handle_children(network_tweets)

unique_user_ids.remove("DUMMY")
print("The set size is " + str(len(unique_user_ids)))

with open('only_top.pickle', 'wb') as f:
    pickle.dump(unique_user_ids, f)

