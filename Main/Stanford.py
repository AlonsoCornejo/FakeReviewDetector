#Function to check if the review contains word_class proper of comparative sentences
def find_comparativeTypes(word_class):
    #Comparative words word_classes
    comp_words=["JJR","JJS","RBR","RBS"]
    
    #Iterate
    for x in comp_words:
        if x==word_class:
            return 1
    
    return 0

# Driver
def main():
    #Main Menu and receive user input
    #filename=menu_option()
    #Running the Stanford POS Tagger from NLTK
    import nltk
    from nltk import word_tokenize
    from nltk import StanfordTagger
    
    
    text_tok = nltk.word_tokenize("Shoes are the best and greatest.")
 
    # Print(text_tok)
    pos_tagged = nltk.pos_tag(text_tok)
    
    # Print the list of tuples: (word,word_class)
    print(pos_tagged)
    
    #
    #For loop to check if there is a word class proper of comparative words
    for word,word_class in pos_tagged:
        if(find_comparativeTypes(word_class)):
            print(str(1))
            break

       
if __name__ == "__main__":
    main()