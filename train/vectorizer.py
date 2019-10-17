import sys
sys.path.append('..')
import csv
import argparse
import pickle
from imblearn.under_sampling import NearMiss
import numpy as np
from train import train
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

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
    X_array = vectorizer.transform(reviews)#.toarray()
    print("X_array.shape:",X_array.shape)
    return X_array

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-first', dest='is_first', type=int, help='dump_file_pickle')
    args = parser.parse_args()
    # Load file csv
    # X_comment = []
    # X_label = []
    print("Load file csv...")
    # with open('../data/comment_processing.csv', 'r') as input_file:
    #     reader_file = csv.reader(input_file)
    df = pd.read_csv('../data/comment_processing.csv')
    X_comment = df['comment'].values
    X_label = df['score'].values
    # TF-IDF
    print("Caculate TF-IDF...")
    X_comment = vectorize(X_comment)
    print("Type X_comment:",type(X_comment))
    print("Number comment POS:", len(df[df['score'] == 1]))
    print("Number comment NEG:", len(df[df['score'] == 0]))
    # Handling imbalanced Data - Under sampling
    print("Handling imbalanced Data - Under sampling")
    X_label = np.asarray(X_label)
    # X_comment = np.asarray(X_comment)

    nr = NearMiss()
    X_res, Y_res = nr.fit_sample(X_comment, X_label)
    print("comment_process_balanced:", X_res.shape)
    print("score_process_balanced:", Y_res.shape)

    pickle_out = open("../model/vectorizer_comment.pickle", "wb")
    pickle.dump(X_res, pickle_out)
    pickle_out.close()

    pickle_out = open("../model/vectorizer_score.pickle", "wb")
    pickle.dump(Y_res, pickle_out)
    pickle_out.close()
    # train(X_res,Y_res)