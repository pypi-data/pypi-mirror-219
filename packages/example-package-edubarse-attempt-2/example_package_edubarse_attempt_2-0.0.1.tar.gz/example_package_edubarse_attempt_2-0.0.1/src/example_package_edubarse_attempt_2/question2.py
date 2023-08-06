#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
from matplotlib import interactive

import json
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.metrics import confusion_matrix
#import plotly
#from OrdinaryLeastSquaresRegression import OrdinaryLeastSquaresRegression

auxiliar_dict = {"classification": [accuracy_score, LinearDiscriminantAnalysis()],
                 "regression":  [mean_squared_error, LinearRegression()],
                 "ordinaryleastsquaresregression":  [mean_squared_error, LinearRegression()]
                }

def generate(problem, n_samples, n_features):       
    """
    Generate a dataset
    """
    if problem == "classification":
        X, y = make_classification(n_samples=n_samples, n_features=n_features, n_classes=2)
        verbosa = "Generate a classification dataset with {} samples, {} features and 2 classes".format(n_samples, n_features) 
        verbosa += "\n\nLearning a Linear Discriminant Analysis, measured with accuracy_score.\n\n"
        
    elif problem == "regression":
        X, y = make_regression(n_samples=n_samples, n_features=n_features, noise=10)
        verbosa = "Generate a regression dataset with {} samples and {} features".format(n_samples, n_features)
        verbosa += "\n\nLearning a Linear Regression, measured with mean_squared_error.\n\n"

    elif problem == "ordinaryleastsquaresregression":  
        X, y = make_regression(n_samples=n_samples, n_features=n_features, noise=10)
        verbosa = "Generate a regression dataset with {} samples and {} features".format(n_samples, n_features)
        verbosa += "\n\nLearning an Ordinary Linear Regression, measured with mean_squared_error.\n\n"
        
    else:
        raise Exception("Unknown problem")
    print(verbosa)
    return X, y, verbosa


def get_metric(problem):
    if problem in list(auxiliar_dict.keys()):
        return 
    else:
        raise Exception("Unknown problem")

def learn(problem, X, y):
    if problem in list(auxiliar_dict.keys()):
        model = auxiliar_dict[problem][1]
    else:
        raise Exception("Unknown problem")
        
    # Train/test splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.33)

    # Model fitting
    model.fit(X_train, y_train)

    # Compute the model error
    y_pred = model.predict(X_test)
    
    
    error = auxiliar_dict[problem][0](y_test, y_pred)
    print("Model error: {:.4f}".format(error))

    if problem == "classification":
        print("Confusion matrix:")
        print(confusion_matrix(y_test, y_pred))

    return model, error

def predicto(model, problem):
    print("Predict on a new dataset of 10 values")
    try:
        coefs = model.coef_.ravel()
    except AttributeError:
        coefs = model.coefs_.ravel()
    X,_,_ = generate(problem, 10, len(coefs))

    return model.predict(X)

def target_statistics(y):
    mean_target = np.mean(y)
    std_target = np.std(y)
    verbosa = "Statistics of the target. Mean = {}, std = {}".format(mean_target, std_target)
    print(verbosa)
    return mean_target, std_target, verbosa

def features_statistics(X):
    mean_features = {"feature_{}".format(k): np.mean(X[:,k]) for k in range(X.shape[1])}
    print("Mean values of the features:")
    print(json.dumps(mean_features, indent=4))

    std_features = {"feature_{}".format(k): np.std(X[:,k]) for k in range(X.shape[1])}
    print("Std values of the features:")
    print(json.dumps(std_features, indent=4))

    return mean_features, std_features

def correlation(X, y):
    corr_coefs = {"feature_{}".format(k): np.corrcoef(X[:,k], y) for k in range(X.shape[1])}
    print_correlations(X, y)
    return corr_coefs

def statistics(X, y):
    mean_target, std_target,_ = target_statistics(y)
    mean_features, std_features = features_statistics(X)

    return {
        "mean_target": mean_target,
        "std_target": std_target,
        "mean_features": mean_features,
        "std_features": std_features,
        "correlations": correlation(X, y)
    }

def print_correlations(X, y):
    dataset = np.concatenate([X, y.reshape(-1,1)], axis=1)
    print("Dataset correlation matrix:")
    print(np.round(np.corrcoef(dataset), 2))

def create_and_train(problem, n_samples, n_features):
    X, y, v = generate(problem, n_samples=n_samples, n_features=n_features)
    stats = statistics(X, y)
    model, error = learn(problem, X, y)
    predictions = predicto(model, problem)

    return stats, error, predictions, v
