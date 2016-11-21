# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 13:18:15 2016

@author: Greta
"""

from sklearn.svm import SVC
import numpy

def evaluate_cross_validation(clf, X, y, K):
    from sklearn.cross_validation import cross_val_score, KFold
    from scipy.stats import sem
    # create a k-fold cross validation iterator
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print (scores)
    print ("Mean score: {0:.3f} (+/-{1:.3f})".format(numpy.mean(scores), sem(scores)))



def training(data):

    
    svc_1 = SVC(kernel='linear')
    
    
    #we create the target vector of 0 for sad images, 1 for happy, 
    #and 2 for normal images
    zero=[int(i) for i in numpy.zeros(15)]
    one=[int(i) for i in numpy.ones(15)]
    two=[int(i) for i in numpy.repeat(2,15)]
    target=numpy.concatenate((zero,one,two),axis=0)
    
    #we test if the classifier work correctly with CROSS-VALIDATION
    #5 fold cross validation
    from sklearn.cross_validation import train_test_split

    
    
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.20, random_state=0)
    
    from sklearn import neighbors
    n_neighbors =3 
    for weights in ['uniform', 'distance']:
        # we create an instance of Neighbours Classifier and fit the data.
        KNeigh = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
        KNeigh.fit(X_train,y_train)
        print(KNeigh.predict(X_test))
        
    print(y_test)
    #evaluate_cross_validation(KNeigh, X_train, y_train, 10)
    #svc is better!!!
    svc_1.fit(X_train,y_train)
    evaluate_cross_validation(svc_1, X_train, y_train, 10)
    return (svc_1)



