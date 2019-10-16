import sys
sys.path.append('..')
import json
import os
import pandas as pd
import numpy as np
import preprocessor
from pyvi import ViTokenizer
from train import train
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
path_json = '../data/raw_data'
comment_score = {'comment':[]}
def process_comment_score(data_comment,comment_score):
    for i,text in enumerate(comment_score['comment']):
        data_comment['comment'].append(text['comment'])
        try:
            data_comment['score'].append(text['score'])
        except:
            data_comment['score'].append(None)
    return data_comment

def processor_score(df):
    for i, ele in enumerate(df['score'].values):
        if (float(ele) >= 6.0):
            df.iloc[i].score = 1
        else:
            df.iloc[i].score = 0
    return df

def  visualization(df):
    numpy_label = df['score'].values
    plt.xlabel("number")
    plt.ylabel("name_class")
    plt.title("su phan bo cua cac class")
    plt.hist(numpy_label, rwidth=1, align="left")
    plt.savefig('demo.png')

def prepocess(text):
    return preprocessor.preprocess(text)

def tokenize(text, stopwords):
    text_segmented = ViTokenizer.tokenize(text).split()
    text_segmented = [elem for elem in text_segmented if elem not in stopwords]
    return ' '.join(text_segmented)

def vectorize(reviews):
    if args.is_first == 1:
        vectorizer = TfidfVectorizer(min_df=5,max_features=50000, sublinear_tf=True)
        vectorizer.fit(reviews)
        pickle_out = open("../model/vectorizer.pickle", "wb")
        pickle.dump(vectorizer, pickle_out)
        pickle_out.close()
    else:
        with open(r"../model/vectorizer.pickle","rb") as input_file:
            vectorizer = pickle.load(input_file)
    X_array = vectorizer.transform(reviews).toarray()
    print("X_array.shape:",X_array.shape)
    return X_array

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-first', dest='is_first', type=int, help='dump_file_pickle')
    args = parser.parse_args()

    for file in os.listdir(path_json):
        path_file = os.path.join(path_json, file)
        if '.json' in file and os.stat(path_file).st_size != 0:
            with open(path_file, 'rb') as input_file:
                data = json.load(input_file)
            comment_score['comment'].extend(data['comment'])
    data_comment = {'comment':[],'score':[]}
    data = process_comment_score(data_comment,comment_score)
    df = pd.DataFrame(data)
    df = df[df.score.isnull() == False].reset_index(drop=True)
    df = processor_score(df)
    print("Number_comment:",len(df['comment'].values))

    with open("./vietnamese-stopwords-dash.txt", encoding="utf8") as input_file:
        x = input_file.readlines()
        removetable = str.maketrans('', '', '\n')
        stopwords = [s.translate(removetable) for s in x]

    reviews = []
    score_comment = []

    for i, text in enumerate(df['comment']):
        #     score_comment.append(text['score'])
        text_processing = prepocess(text)
        reviews.append(tokenize(text_processing, stopwords))
    # TF-IDF
    X_comment = vectorize(reviews)
    X_label = df['score'].values

    train.train(X_comment,X_label)