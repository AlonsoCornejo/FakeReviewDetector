import numpy as np
import pandas as pd


def logistic_reg():
    global LIWC
    
    #Our fake LIWC dictionary that we will replace later with a real one. Changing this will change everything, making our dictionary and ndarray bigger. Bsed on:
    #http://web.stanford.edu/class/linguist197a/Lying%20words%20predicting%20deception.pdf
    LIWC = {'Pronoun': ["I", "our", "they", "you're"], 'I':['I', 'my', 'me'],'Self': ['I', 'we', 'me'],'Other': ['she', 'their', 'them'],'Negate': ['no', 'not', 'never'],
                'Article': ['a', 'an', 'the'],'Preps': ['on', 'to', 'from'],'Affect': ['happy', 'ugly', 'bitter'],'Posemo': ['happy', 'pretty', 'good'],
                'Negemo': ['hate', 'worthless', 'enemy'],'Cogmech': ['cause', 'know', 'ought'],'Cause': ['because', 'effect', 'hence'],'Discrep': ['should', 'would', 'could'],
                'Tentat': ['maybe', 'perhaps', 'guess'], 'Certain': ['always', 'never'], 'Senses': ['see', 'touch', 'listen'], 'Social': ['talk', 'us', 'friend'],
                'Space': ['around', 'over', 'up'],'Incl': ['with', 'and', 'include'],'Excl': ['but', 'except', 'without'],'Motion': ['walk', 'move', 'go'],
                'Past': ['walked', 'were', 'had'],'Time': ['hour', 'day', 'oclock'],'Time': ['hour', 'day', 'oclock'],'Present': ['walk', 'is', 'be'],'Future': ['will', 'might', 'shall']}

    old_reviews = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    new_reviews = analyze_reviews("new_reviews_clean.txt")
    
    print(new_reviews)
    #r0 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r1 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r2 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r3 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r4 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r5 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r6 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r7 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r8 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r9 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r10 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r11 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
    #r12 = analyze_reviews("output_review_yelpHotelData_NRYRcleaned.txt")
   
    
#This function takes in a corpus, extracts the words in the categories that are present in the LIWC dictionary from that body of text. Then, it counts the number of occurances 
#of those words, and returns a dictionary with categories as keys and the number of times each category's words occur as values.
def LIWC_feature_extraction(text):
    #create a dictionary that will hold our value
    feature_dict={}

    #for every key in the LIWC, we compare our text to the categories and 
    #then we increment whenever a word from the key/ value appears in our text
    for key in LIWC:
        num_occur = 0
        for i in LIWC[key]:
            num_occur += text.count(i)
        feature_dict[key] = num_occur

    
    return feature_dict   


#for every review of the csv yelp reviews, do the analysis of the reviews, and put the number of each review
#for every review in the csv doc of reviews, take the meat of it and analyze based on our dictionary. 
#Then, we write the results of this to a new csv file, with the broad categories as the column names 




#this treats all old review like one big thing, finding all instances in the whole doc as categories
def analyze_reviews(review_file):
    #read and store the whole file to pass into our func later
    f = open(review_file,"r")
    f_content = f.read()

    #an array that will store each of the \n seperated reviews from the file.
    reviews=[]

    #open the file and seperate each review by the \n char
    with open(review_file,"r") as file:
        count = 0
        #for each of the 
        for review in file:
            reviews.append(review.rstrip())
            
def logistic_new_reviews():
    ## create a matrix using Yifan's exported cvs file regarding the LIWC features. Note that you need to locate the features that are LIWC categories only 
    ## and disregard the remaining ones. 

    ## For each row, find the corresponding feature vector and the class label (1-Yes, 0-No). Then train a logistic regression model:
    ## So, here the columns that are Category labels should be apart of the feature vector and the output is the realOrFake column
    ## Lets do this by reading in the CSV file as a Pandas Dataframe, then converting it to a matrix. 

    #read in the csv file into a dataframe
    old_liwc_df = pd.read_csv ('LIWC-outputOnContentsAndNY_big_cat.csv')

    # create a logistic regression model based on categories, choosing realOrFake to be what we are predicting. 
    # referenced from how it was done on https://datatofish.com/logistic-regression-python/

    # feature vector of categories being used for prediction
    x = old_liwc_df[['Linguistic', 'Drives','Cognition','Affect','Social','Culture','Lifestyle', 'Physical', 'Perception', 'Conversation']]

    # category we are predicting
    y = old_liwc_df['realOrFake']

    # split the data into training data and testing data, with 1/4 being reserved for testings 
    train =  read_csv('train.csv')
    test0 =  read_csv('/reviews/review_0_LIWC.csv')
    test1 =  read_csv('/reviews/review_1_LIWC.csv')
    test2 =  read_csv('/reviews/review_2_LIWC.csv')
    test3 =  read_csv('/reviews/review_3_LIWC.csv')
    test4 =  read_csv('/reviews/review_4_LIWC.csv')
    test5 =  read_csv('/reviews/review_5_LIWC.csv')
    test6 =  read_csv('/reviews/review_6_LIWC.csv')
    test7 =  read_csv('/reviews/review_7_LIWC.csv')
    test8 =  read_csv('/reviews/review_8_LIWC.csv')
    test9 =  read_csv('/reviews/review_9_LIWC.csv')
    test10 = read_csv('/reviews/review_10_LIWC.csv')
    test11 = read_csv('/reviews/review_11_LIWC.csv')
    test12 = read_csv('/reviews/review_12_LIWC.csv')
    # create a new Logistic Regression tool
    logistic_regression = LogisticRegression(solver="sag", max_iter=5000)


    # fit the training data to the model
    logistic_regression.fit(x_train,y_train)

    #predict the realOrFake category based on the logistic regression applied to the testing portion of the data
    y_pred = logistic_regression.predict(x_test)
    y_pred_prob = logistic_regression.predict_proba(x_test)

    #print the accuracy of the model by comparing the testing data against the real predictions
    print('Accuracy: ', accuracy_score(y_test, y_pred))
    print('AUC:', roc_auc_score(y_test, y_pred_prob[:,-1]))

    #predict probability function (how likely the review is fake), allows us to evaluate the AUC curve

    #debug with Prof at another time
    #plug in our model into the cross validation from sklearn
    cv_results = cross_validate(logistic_regression, x, y, cv=None)
    print('Cross validation: ', cv_results)
logistic_reg()

