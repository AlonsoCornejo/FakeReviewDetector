#import statements for numpy
import numpy as np

#import statements for sklearn
from sklearn import datasets, linear_model
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import make_scorer, accuracy_score, roc_auc_score, confusion_matrix, auc
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

#import seabord to create an accuracy score and plot
import seaborn as sn

#import pyplot
import matplotlib.pyplot as plt

#import for pandas
import pandas as pd

class LogReg:
    self.liwc_df = pd.read_csv('LIWC-outputOnContentsAndNY_big_cat.csv')