import sys
sys.path.append('..')
import csv
import argparse
import pickle
from imblearn.under_sampling import NearMiss
import numpy as np
from train import train
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # Load file csv
    X_comment = []
    X_label = []
    print("Load file csv...")
    with open('../data/comment_processing.csv', 'r') as input_file:
        reader_file = csv.reader(input_file)
        for row in reader_file:
            X_comment.append(row[0])
            X_label.append(row[1])
    # TF-IDF
    print("Caculate TF-IDF...")
    X_comment = vectorize(X_comment)
    X_label = X_label

    # Handling imbalanced Data - Under sampling
    print("Handling imbalanced Data - Under sampling")
    X_label = np.asarray(X_label)
    X_comment = np.asarray(X_comment)
    nm = NearMiss(random_state=42)
    X_res, Y_res = nm.fit_sample(X_comment, X_label)
    print("comment_process_balanced:", X_res.shape)
    print("score_process_balanced:", Y_res.shape)
    train(X_res,Y_res)