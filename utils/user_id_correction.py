# Abhijeet Padhy

import json
import os
import constants as CONST

init_path = 'X:\\fakenewsnet_dataset\\data_json\\'
# directories = ['gossipcop_fake', 'gossipcop_real', 'politifact_fake', 'politifact_real']

# finding the dataset where we have to modify
directories = []
for dataset in CONST.DATASETS:
    for label in CONST.LABELS:
        directories.append("{}_{}".format(dataset, label))
print(directories)


# creating a new folder to save the modified graph
def dump_data_into_file(directory_loc, data, file_location):
    directory = os.path.dirname(directory_loc + file_location + ".json")
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory_loc + file_location + ".json", "w")
    try:
        user_data = json.dumps(data, indent=4)
        f.write(user_data)
        f.close()
        return "Success"
    except Exception as E:
        print('Some error happend', E)
        f.write('')
        f.close()
        return "Error"


def handle_children_recursive(element, parent_tweet_id, fun_dir, fun_news, retweet_data):
    if len(retweet_data[str(parent_tweet_id)]) == 0 and 'children' in element:
        element.pop('children')
        return
    for cur in retweet_data[str(parent_tweet_id)]:
        if cur['id'] == element['tweet_id']:
            element['user'] = cur['user']['id']
            break
    if 'children' not in element:
        return
    for child in element['children']:
        handle_children_recursive(child, parent_tweet_id, fun_dir, fun_news, retweet_data)


def handle_children(element, fun_dir, fun_news):
    retweet_file = open(init_path + fun_dir + '\\' + fun_news + '\\retweets.json')
    retweet_data = json.load(retweet_file)
    parent_tweet_id = element['tweet_id']
    if len(retweet_data[str(parent_tweet_id)]) == 0 and 'children' in element:
        element.pop('children')
        return

    if 'children' not in element:
        return
    for child in element['children']:
        handle_children_recursive(child, parent_tweet_id, fun_dir, fun_news, retweet_data)


for my_dir in directories:
    print("The dir is " + my_dir)
    list_of_news = os.listdir(init_path + my_dir)
    for news in list_of_news:
        print("The news is" + news)
        json_file_path = init_path + my_dir + '\\' + news + '\\tweets.json'
        network_file_path = 'X:\\fakenewsnet_dataset\\data_network\\' + my_dir + '\\' + news + '.json'
        try:
            json_file = open(json_file_path)
        except:
            print("This file {} is not found!".format(json_file_path))
            continue
        try:
            network_file = open(network_file_path)
        except:
            print("This file {} is not found!".format(network_file_path))
            continue
        print(network_file)

        json_data = json.load(json_file)
        network_data = json.load(network_file)

        for network_tweets in network_data['children']:
            tweet_id = network_tweets['tweet_id']
            # correct_user_id = tweets['user_id']
            for json_tweets in json_data['tweets']:
                if tweet_id == json_tweets['tweet_id']:
                    correct_user_id = json_tweets['user_id']
                    # print("Found tweet" + str(tweet_id))
                    # print("wrong user id: " + str(network_tweets['user']) + " correct user id: " + str(correct_user_id))
                    network_tweets['user'] = correct_user_id
                    break
            handle_children(network_tweets, my_dir, news)
        dump_data_into_file('X:\\fakenewsnet_dataset\\data_network_new\\' + my_dir + '\\', network_data, news)
