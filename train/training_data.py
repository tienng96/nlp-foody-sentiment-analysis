from train import train
import pickle

with open(r"../model/vectorizer_comment.pickle", "rb") as input_file:
    vector_comment = pickle.load(input_file)
with open(r"../model/vectorizer_score.pickle", "rb") as input_file:
    vector_score = pickle.load(input_file)
train(vector_comment,vector_score)