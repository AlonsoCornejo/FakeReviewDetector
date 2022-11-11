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

class Logistic_reg:
    def __init__(self, name, path):
        
        self.filename = name
        self.mFile=open(path,"r")
        #DEBUG
        
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
    
        #remove line 33 - dont need to train and test split, we will use entire x and y to train single log reg model
        #change line 37 needs to consume the entire x and y matrix
        #our test data is our new review
        #extract LIWC categories from new reviews
        #construct x test matrix from new review, fit that into line 40 (self.y_pred_prob = self.logistic_regression.predict_proba(self.x_test))
        #save result of y pred prob to display on the webpage
            #maybe have a gradient to show the probability using thresholds. 
            #between table of reviews and arrows at bottom, show a histogram of frequencies of key words in the reviews. 
            #place LIWC categories frequencies and send to front end and analyze if they are sentimental, lies, etc. 
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
        
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.x,self.y,test_size=0.25,random_state=0)
        
        self.logistic_regression = LogisticRegression(solver="sag", max_iter=2000)
        
        self.logistic_regression.fit(self.x_train,self.y_train)
        
        self.y_pred = self.logistic_regression.predict(self.x_test)
        self.y_pred_prob = self.logistic_regression.predict_proba(self.x_test)
        
        self.cv_results = cross_validate(self.logistic_regression, self.x, self.y, cv=None)
        
        
        self.y_pred_df = pd.DataFrame(self.y_pred, columns = ['y_pred'], index = X.index.copy())
        self.y_pred_train_df = pd.DataFrame(self.y_pred_train, columns = ['y_pred_train'], index = X[train].index.copy())
        self.y_pred_test_df = pd.DataFrame(self.y_pred_test, columns = ['y_pred_test'], index = X[test].index.copy())
        self.dftraintest = pd.concat([self.y,self.y_pred_df,self.y_pred_train_df,self.y_pred_test_df],axis=1)
    #make a function that returns the results as a file like in comparative.py getfile