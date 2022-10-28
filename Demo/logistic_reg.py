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
    def large_cat_lin_reg(self):
        self.liwc_df = pd.read_csv('LIWC-outputOnContentsAndNY_big_cat.csv')
        
        self.x = self.liwc_df[['Linguistic', 'Drives','Cognition','Affect','Social','Culture','Lifestyle', 'Physical', 'Perception', 'Conversation']]
        self.y = self.liwc_df['realOrFake']
        
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.x,self.y,test_size=0.25,random_state=0)
        
        self.logistic_regression = LogisticRegression(solver="sag", max_iter=5000)
        
        self.logistic_regression.fit(self.x_train,self.y_train)
        
        self.y_pred = self.logistic_regression.predict(self.x_test)
        self.y_pred_prob = self.logistic_regression.predict_proba(self.x_test)
        
        self.cv_results = cross_validate(self.logistic_regression, self.x, self.y, cv=None)
    
    def large_cat_lin_reg(self):
        self.liwc_df = pd.read_csv('LIWC-outputOnContentsAndNY_big_cat.csv')
        
        self.x = self.liwc_df[['function', 'pronoun','ppron','i','we','you','shehe', 'they', 'ipron', 'det', 
             'article','number','prep','auxverb','adverb','conj', 'negate', 'verb', 'adj',
             'quantity','affiliation','achieve','power','allnone', 'cogproc', 'insight', 'cause',
             'discrep','certitude','differ','memory','tone_pos', 'tone_neg', 'emotion', 'emo_pos',
             'emo_neg','emo_anx','emo_anger','emo_sad','swear', 'socbehav', 'prosocial', 'polite',
             'conflict','moral','comm','socrefs','family', 'friend', 'female', 'male',
             'politic','ethnicity','tech','leisure','home', 'work', 'money', 'relig',
             'health','illness','wellness','mental','substances', 'sexual', 'food', 'death',
             'need','want','acquire','lack','fulfill', 'fatigue', 'reward', 'risk','curiosity', 
             'allure','attention','motion','space', 'visual', 'auditory', 'feeling','time',
             'focuspast','focuspresent','focusfuture','netspeak', 'assent', 'nonflu', 'filler']]
        self.y = self.liwc_df['realOrFake']
        
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(x,y,test_size=0.25,random_state=0)
        
        self.logistic_regression = LogisticRegression(solver="sag", max_iter=2000)
        
        self.logistic_regression.fit(self.x_train,self.y_train)
        
        self.y_pred = self.logistic_regression.predict(self.x_test)
        self.y_pred_prob = self.logistic_regression.predict_proba(self.x_test)
        
        self.cv_results = cross_validate(self.logistic_regression, x, y, cv=None)