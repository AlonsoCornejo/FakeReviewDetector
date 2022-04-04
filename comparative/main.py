import dataSet
import numpy as np
# ComparativeExpressions for a second sub-team

#Print out Main Menu and manage user selection
def menu_option():
    print("Avalaible Product Reviews Data: \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1: Yelp Reviews")
    print("2: DVD Player")
    print("3: Digital Camera")
    print("4: MP3 Player")

    option=input("Please select a product review dataset to analyze: ")

    switcher = {
        1: "Yelp_Reviews.txt",
        2: "DVD_Player.txt",
        3: "Digital_Camera.txt",
        4: "MP3_Player.txt",
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
    # close file after summary calculated
    data.mFileClose()

    vec = data.getClassificationVector()
       
if __name__ == "__main__":
    main()