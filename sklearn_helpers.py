from pandas_confusion import ConfusionMatrix
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import FunctionTransformer
import numpy as np
import re

def genericize_mentions(text):
    return re.sub(r'@[\w_-]+', 'thisisanatmention', text)

def get_tweet_length(text):
    return len(text)

def pipelinize(function, active=True):
    def list_comprehend_a_function(list_or_series, active=True):
        if active:
            return [function(i) for i in list_or_series]
        else: # if it's not active, just pass it right back
            return list_or_series
    return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'active':active})

def reshape_a_feature_column(series):
    return np.reshape(np.asarray(series), (len(series), 1))

def pipelinize_feature(function, active=True):
    def list_comprehend_a_function(list_or_series, active=True):
        if active:
            processed = [function(i) for i in list_or_series]
            processed = reshape_a_feature_column(processed)
            return processed
#         This is incredibly stupid and hacky, but we need it to do a grid search.
#         If a feature is deactivated, we're going to just return a column of zeroes.
#         Zeroes shouldn't affect the regression, but other values may.
#         If you really want brownie points, consider pulling out that feature column later in the pipeline.
        else:
            return reshape_a_feature_column(np.zeros(len(list_or_series)))

    return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'active':active})

def display_null_accuracy(y_test):
    value_counts = pd.value_counts(y_test)
    null_accuracy = max(value_counts) / float(len(y_test))
    print 'null accuracy: %s' % '{:.2%}'.format(null_accuracy)
    return null_accuracy

def display_accuracy_score(y_test, y_pred_class):
    score = accuracy_score(y_test, y_pred_class)
    print 'accuracy score: %s' % '{:.2%}'.format(score)
    return score

def display_accuracy_difference(y_test, y_pred_class):
    null_accuracy = display_null_accuracy(y_test)
    accuracy_score = display_accuracy_score(y_test, y_pred_class)
    difference = accuracy_score - null_accuracy
    if difference > 0:
        print 'model is %s more accurate than null accuracy' % '{:.2%}'.format(difference)
    elif difference < 0:
        print 'model is %s less accurate than null accuracy' % '{:.2%}'.format(abs(difference))
    elif difference == 0:
        print 'model is exactly as accurate as null accuracy'
    return null_accuracy, accuracy_score

def train_test_and_evaluate(pipeline, X_train, y_train, X_test, y_test):
    pipeline.fit(X_train, y_train)
    y_pred_class = pipeline.predict(X_test)
    confusion_matrix = ConfusionMatrix(list(y_test), list(y_pred_class))
    display_accuracy_difference(y_test, y_pred_class)
    classification_report = confusion_matrix.classification_report
    print '-' * 75 + '\nConfusion Matrix\n'
    print confusion_matrix
    print '-' * 75 + '\nClassification Report\n'
    print classification_report
      
    return pipeline, confusion_matrix