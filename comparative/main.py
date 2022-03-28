# used to convert the JSON dictionary to a python dictionary object
from contextlib import nullcontext
from itertools import product
import json
from operator import truth
from pickle import FALSE, TRUE
from string import punctuation
from tokenize import Double

# ComparativeExpressions 
# for a second sub-team
def comparative_feature_extraction(file):
    #Declare and initialzie some storage variables
    is_comparative_review=False
    num_comp_review=0
    num_reviews=0

    """
        The keys in 'comparative_dict.json' are from 
        https://www.cs.uic.edu/~liub/FBS/comparative-lexicon.pdf
    """
    #Json file to Python Dictionary
    feature_dict = {}
    with open('comparative_dict.json') as json_file:
        feature_dict = json.load(json_file)
    
    #Iterate through lines of the file
    for x in file:
        #Add Review to the count of all reviews
        num_reviews+=1

        #Clean text and remove punctuation 
        clean_text=cleaning_data(x)

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

#Clean Text and Remove Punctuation Function
def cleaning_data(text):

    clean_text=""
    #Iterate thorough the review text string
    for i in range (0,len(text)):
        if not shouldBe_erased(text[i]):
            clean_text+=text[i]#Build clean review string

    return clean_text

#Function to find Punctuation or symbols that should be deleted
def shouldBe_erased(character):
    #List of Symbols
    symbols=['.',',',':','/','[',']','{','}','(',')'';','+','-','=','*','#','%','$','@','&','!','?','^','~','`','|','_','<','>']

    #Check if character is in the symbol list
    for i in symbols:
        if i==character: 
            return True #Symbol to be deleted is found
    
    return False
    
#Print out Main Menu and manage user selection
def menu_option():
    print("Avalaible Product Reviews Data: \n")
    print("1: MP3 Player\n")
    print("2: DVD Player\n")
    print("3: Digital Camera\n\n")

    option=input("Please select a product review dataset to analyze: ")

    switcher = {
        1: "MP3_Player.txt",
        2: "DVD_Player.txt",
        3: "Digital_Camera.txt",
    }

    #Return filename based on user input
    return switcher.get(int(option),"nothing")

#Print Summary of Search
def get_summary(filename,feature_dict,num_CompRev,num_reviews):
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

# Driver
def main():
    #Main Menu and receive user input
    filename=menu_option()

    #Open File to read
    path="C:/Users/Alonso Cornejo/Documents/Lehigh University/Third Year/Spring Semester/CSB312/Dic Assignment/comparative-analysis/comparative/Data_Per_Product/"+filename
    file=open(path,"r")
    
    #Identify comparable words in reviews and get data on review file
    result = comparative_feature_extraction(file)
    
    #Execute/Print Analysis Summary and ocurrences of comparable words
    get_summary(filename,result[0],result[1],result[2])
    
if __name__ == "__main__":
    main()