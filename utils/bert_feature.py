import pickle
import scipy.sparse as sp
import numpy as np
from transformers import BertTokenizer, BertModel
import json
from preprocess import preprocess_text

def read_timeline_tweets(folder_name, id):
    file_name = f'{id}.json'
    with open(folder_name + '/' + file_name) as f:
        data = json.load(f)
        user_tweet = '. '.join(preprocess_text(timeline['text']) for timeline in data)
        # print(user_tweet)
    return user_tweet

if __name__ == '__main__':
    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    model = BertModel.from_pretrained('bert-base-cased')
    sparse_matrix = []
    not_valid = 0
    with open('only_top.pickle', 'rb') as f:
        unique_user_id = pickle.load(f)
        print('Generating embedding ...')
        for id in unique_user_id:
            try:
                sentence = read_timeline_tweets('../user_timeline_tweets', id)
                encoding = tokenizer(sentence, add_special_tokens=True, return_tensors='pt', truncation=True, padding='do_not_pad')['input_ids']
                output = model(encoding)
                output = output.pooler_output.detach().numpy().flatten()
                sparse_matrix.append(output)
            except:
                not_valid += 1

    sparse_matrix = sp.csc_matrix(np.asarray(sparse_matrix))
    sp.save_npz('bert_feature.npz', sparse_matrix)
    print(f'{not_valid} files were not found')