def menu_option():
    print("Avalaible Product Reviews Data: \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1: Yelp Reviews")
    print("2: DVD Player")
    print("3: Digital Camera")
    print("4: MP3 Player")
    print("5: Coke vs Pepsi")
    print("6: Camera models comaparison")
    print("7: Soccer vs Football")

    option=input("Please select a product review dataset to analyze: ")

    switcher = {
        1: "Yelp_Reviews.txt",
        2: "DVD_Player.txt",
        3: "Digital_Camera.txt",
        4: "MP3_Player.txt",
        5: "Coke_Pepsi.txt",
        6: "Camera_comp.txt",
        7: "Soccer_Football.txt",
    }

    #Return filename based on user input
    return switcher.get(int(option),"nothing")

# Driver
def main():
    #Main Menu and receive user input
    filename=menu_option()
    # running the Stanford POS Tagger from NLTK
    import nltk
    from nltk import word_tokenize
    from nltk import StanfordTagger
    
    # point this path to a utf-8 encoded plain text file in your own file system
    f = "./Data_Per_Product/"+filename

    text_raw = open(f).read()
    text = nltk.word_tokenize(text_raw)
    pos_tagged = nltk.pos_tag(text)
    
    # print the list of tuples: (word,word_class)
    # this is just a test, comment out if you do not want this output
    print(pos_tagged)
    
    # for loop to extract the elements of the tuples in the pos_tagged list
    # print the word and the pos_tag with the underscore as a delimiter
    for word,word_class in pos_tagged:
        print(word + "_" + word_class)
        
       
if __name__ == "__main__":
    main()