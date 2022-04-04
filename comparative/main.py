# used to convert the JSON dictionary to a python dictionary object
from contextlib import nullcontext
from itertools import product
import json
from operator import truth
from pickle import FALSE, TRUE
from string import punctuation
import string
string.punctuation
from tokenize import Double
import dataSet
# ComparativeExpressions for a second sub-team

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


# Driver
def main():
    #Main Menu and receive user input
    filename=menu_option()

    #Open File to read
    path="./Data_Per_Product/"+filename

    #Create a dataset Object
    data=dataSet.DataSet(filename,path)

    #Execute Identification of Comparative Words and Analysis
    data.get_summary()
       
if __name__ == "__main__":
    main()