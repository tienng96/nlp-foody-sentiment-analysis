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
import csv
from imblearn.under_sampling import NearMiss
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
    # score_comment = []

    for i, text in enumerate(df['comment']):
        # score_comment.append(text['score'])
        text_processing = prepocess(text)
        temp_text = tokenize(text_processing, stopwords)
        reviews.append(temp_text)
    for i, score in enumerate(df['score']):
        reviews[i] = reviews[i] + ',' + '{}'.format(score)
    #Write file csv
    with open('../data/comment_processing.csv','w') as out_file:
        writer = csv.writer(out_file)
        # writer.writerow(('comment','score'))
        for text in reviews:
            row = [c.strip() for c in text.strip(', ').split(',')]
            writer.writerow(row)
    #Load file csv
    X_comment = []
    X_label = []
    with open('../data/comment_processing.csv','r') as input_file:
        reader_file = csv.reader(input_file)
        for row in reader_file:
            X_comment.append(row[0])
            X_label.append(row[1])
    # TF-IDF
    X_comment = vectorize(X_comment)
    X_label = X_label
    print("Number comment POS:",len(df[df['score'] == 1]))
    print("Number comment NEG:", len(df[df['score'] == 0]))
    # Handling imbalanced Data - Under sampling
    X_label = np.asarray(X_label)
    X_comment = np.asarray(X_comment)
    nm = NearMiss(random_state=42)
    X_res,Y_res = nm.fit_sample(X_comment,X_label)
    print("comment_process_balanced:",X_res.shape)
    print("score_process_balanced:",Y_res.shape)
    train.train(X_res,Y_res)