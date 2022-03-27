# used to convert the JSON dictionary to a python dictionary object
from contextlib import nullcontext
import json
from operator import truth
from pickle import FALSE, TRUE
from string import punctuation

# ComparativeExpressions 
# for a second sub-team
def comparative_feature_extraction(text):
    # print input text
    print(text + '\n')

    """
        The keys in 'comparative_dict.json' are from 
        https://www.cs.uic.edu/~liub/FBS/comparative-lexicon.pdf
    """
    feature_dict = {}
    with open('comparative_dict.json') as json_file:
        feature_dict = json.load(json_file)


    #Clean text and remove punctuation 
    clean_text=cleaning_data(text)

    # find the number of times that each such key appears in text.
    # loop through all elements in the dictionary.
    # if they are found in the cleaned text, increment the dictionary value.
    for key in feature_dict:
        if key in clean_text:
            feature_dict[key] += 1

    return feature_dict

#Clean Text and Remove Punctuation Function
def cleaning_data(text):
    print("Orginal: "+text + '\n')
    clean_text=""
    #Iterate thorough the review text string
    for i in range (0,len(text)):
        if not shouldBe_erased(text[i]):
            clean_text+=text[i]

    print("New: "+clean_text + '\n')
    return clean_text

#Function to find Punctuation or symbols that should be deleted
def shouldBe_erased(character):
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
    print(option)

    switcher = {
        1: "MP3_Player.txt",
        2: "DVD_Player.txt",
        3: "Digital_Camera.txt",
    }

    return switcher.get(int(option),"nothing")


# Driver
def main():
    #Main Menu and receive user input
    filename=menu_option()
    #Open File to read
    file=open(filename,"r")
  
    input_str = 'I prefer apple to samsung|| I prefer ethereum to bitcoin&& I like google the most** Nokia is the best** Lamborghini is on par with Ferrari.'
    feature_dict = comparative_feature_extraction(input_str)
    for key in feature_dict:
        if feature_dict[key] != 0:
            print(key + ' -> ' + str(feature_dict[key]))

if __name__ == "__main__":
    main()