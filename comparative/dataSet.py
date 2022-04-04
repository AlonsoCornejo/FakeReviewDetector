from asyncio.windows_events import NULL
from contextlib import nullcontext
from fileinput import filename
from io import StringIO
from itertools import product
import json
from operator import truth
from pickle import FALSE, TRUE
from string import punctuation
from tokenize import Double
from unicodedata import name
import string
string.punctuation


class DataSet:

    def __init__(self,name,path):
        self.filename = name
        self.mFile=open(path,"r")


    #Clean Text and Remove Punctuation Function
    def cleaning_data(self,text,punct_list):
        #Using the string library
        for punc in punct_list:
            if punc in text:
                text = text.replace(punc, ' ')
        return text.strip()
    
    #Execute the couting of the words
    def comparative_feature_extraction(self):
        #Declare and initialzie some storage variables
        is_comparative_review=False
        num_comp_review=0
        num_reviews=0
        regular_punct = list(string.punctuation)

        """
            The keys in 'comparative_dict.json' are from 
            https://www.cs.uic.edu/~liub/FBS/comparative-lexicon.pdf
        """
        #Json file to Python Dictionary
        feature_dict = {}
        with open('comparative_dict.json') as json_file:
            feature_dict = json.load(json_file)
        
        #Iterate through lines of the file
        for x in self.mFile:
            #Add Review to the count of all reviews
            num_reviews+=1

            #Clean text and remove punctuation 
            clean_text=self.cleaning_data(x,regular_punct)

            # find the number of times that each such key appears in text.
            # loop through all elements in the dictionary.
            # if they are found in the cleaned text, increment the dictionary value.
            for key in feature_dict:
                if key in clean_text:
                    feature_dict[key] += 1
                    is_comparative_review=True
            
            #Get Number of comparative reviews
            if is_comparative_review:
                num_comp_review+=1
            
            #Set false for next review analysis
            is_comparative_review=False

        return feature_dict,num_comp_review,num_reviews

    #Print Summary of Search
    def get_summary(self):
        
        #Run comparable words identification algorithm
        result = self.comparative_feature_extraction()
        
        #Access obtained Values from identification algorithm
        filename= self.filename
        feature_dict= result[0]
        num_CompRev= result[1]
        num_reviews= result[2]

        #Get Product Name
        _position=filename.find('_')
        product_name=filename[0:_position]+" "+filename[_position+1:-4]

        #Get Sum of All Comparable Words
        sum_compwords=0
        for key in feature_dict:
            sum_compwords+=feature_dict[key]
        
        #Print Basic Information and findings
        print("\n************************************************************************************")
        print('\033[1m'+'\033[4m'+"General Summary: \n"+'\033[0m')
        print("Product: "+ product_name + "\n")
        print("E-Commerce Platform: Amazon \n")
        print("Data file: "+ filename + "\n")
        print("Number of Reviews: "+ str(num_reviews) + "\n")
        print("Number of Comparabale Words: "+ str(sum_compwords) + "\n")
        print("Number of Reviews containing comparable words: "+ str(num_CompRev) + "\n")
        print("Average comprable words per Review: "+ str(round(sum_compwords/num_reviews,2)) + "\n")
        print("Average comprable words per Comparable Review: "+ str(round(sum_compwords/num_CompRev,2)) + "\n")
        print("Percentage of Comparable reviews from all reviews: " + str(round((num_CompRev/num_reviews)*100,2)) + "%\n")
        
        #Print the ocurrences
        print('\033[1m'+'\033[4m'+"All Comparable Word Ocurrances: \n"+'\033[0m')
        for key in feature_dict:
            if feature_dict[key] != 0:
                print(key + ' -> ' + str(feature_dict[key]))
        
        print("***********************************************************************************\n")



