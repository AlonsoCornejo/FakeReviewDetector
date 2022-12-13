import numpy as np
import pandas as pd

def logisticRegression():
    
    #Our fake LIWC dictionary that we will replace later with a real one. Changing this will change everything, making our dictionary and ndarray bigger. Bsed on:
#http://web.stanford.edu/class/linguist197a/Lying%20words%20predicting%20deception.pdf

    global LIWC 
    LIWC = {'Pronoun': ["I", "our", "they", "you're"], 'I':['I', 'my', 'me'],'Self': ['I', 'we', 'me'],'Other': ['she', 'their', 'them'],'Negate': ['no', 'not', 'never'],
            'Article': ['a', 'an', 'the'],'Preps': ['on', 'to', 'from'],'Affect': ['happy', 'ugly', 'bitter'],'Posemo': ['happy', 'pretty', 'good'],
            'Negemo': ['hate', 'worthless', 'enemy'],'Cogmech': ['cause', 'know', 'ought'],'Cause': ['because', 'effect', 'hence'],'Discrep': ['should', 'would', 'could'],
            'Tentat': ['maybe', 'perhaps', 'guess'], 'Certain': ['always', 'never'], 'Senses': ['see', 'touch', 'listen'], 'Social': ['talk', 'us', 'friend'],
            'Space': ['around', 'over', 'up'],'Incl': ['with', 'and', 'include'],'Excl': ['but', 'except', 'without'],'Motion': ['walk', 'move', 'go'],
            'Past': ['walked', 'were', 'had'],'Time': ['hour', 'day', 'oclock'],'Time': ['hour', 'day', 'oclock'],'Present': ['walk', 'is', 'be'],'Future': ['will', 'might', 'shall']}
    
    LIWC_df = pd.DataFrame.from_dict(LIWC)
    
    
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


def analyze_reviews():
    #read and store the whole file to pass into our func later
    f = open("output_review_yelpHotelData_NRYRcleaned.txt","r")
    f_content = f.read()

    #an array that will store each of the \n seperated reviews from the file.
    reviews=[]

    #open the file and seperate each review by the \n char
    with open("/content/gdrive/MyDrive/CSE-CSB_Capstone/Subteam-1/output_review_yelpHotelData_NRYRcleaned.txt","r",newline="\n") as file:
        count = 0
        #for each of the 
        for review in file:
            reviews.append(review.rstrip())
    print("Number of reviews in the file: ",len(reviews))