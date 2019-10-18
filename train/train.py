from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import pickle
def train(X_comment, X_label):
    # Train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X_comment, X_label, test_size=0.2, random_state=42)
    # Covert int
    Y_train = Y_train.astype(int)
    # Train SVC
    # clf = svm.SVC(verbose=True, kernel='linear', probability=True, random_state=0, cache_size=2000,
    #               class_weight='balanced')
    clf = LinearSVC(fit_intercept=True, multi_class='crammer_singer', C=0.2175)
    # clf = SVC(kernel='linear', C=0.2175, class_weight=None, verbose=True)
    clf.fit(X_train, Y_train)
    pickle_out = open("../model/model.pickle", "wb")
    pickle.dump(clf, pickle_out)
    pickle_out.close()
    # print(clf.n_support_)
    print("=========VALIDATE_TRAIN===========")
    X_pred = clf.predict(X_train)
    Y_train = Y_train.astype(int)
    precision, recall, fscore, support = score(Y_train, X_pred)
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    print('accuracy = ', accuracy_score(X_pred, Y_train))



    # precision, recall, fscore, support = score(Y_test, Y_pred)
    print("=========VALIDATE_TEST===========")
    Y_pred = clf.predict(X_test)
    Y_test = Y_test.astype(int)
    precision, recall, fscore, support = score(Y_test, Y_pred)
    #Danh gia F1-score:
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    print('accuracy = ', accuracy_score(Y_test, Y_pred))
