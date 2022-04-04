import json
import re
import numpy as np

class DataSet:
    def __init__(self, name, path):
        self.filename = name
        self.mFile=open(path,"r")

        self.feature_dict = {}
        # https://www.cs.uic.edu/~liub/FBS/comparative-lexicon.pdf
        with open('comparative_dict.json') as json_file:
            self.feature_dict = json.load(json_file)
        json_file.close()

        # precompiles all keys of the dictionary as regex
        self.feature_dict_compiled = [re.compile(i) for i in self.feature_dict]

        # classification list
        # 1 - comparative
        # 0 - NOT comparative
        self.classification = []

    # returns the numpy vector containing all line numbers, and their classifications
    def getClassificationVector(self):
        list = []
        for (n, c) in zip(range(len(self.classification)), self.classification):
            list.append([n, c])
        vec = np.array(list)
        return vec

    # Clean input text
    def cleaning_data(self, text):
        out = text.lower()
        out = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", out) 
        out = re.sub(r" +", " ", out)
        return out
    
    #Execute the couting of the words
    def comparative_feature_extraction(self):
        #Declare and initialzie some storage variables
        num_comp_review = 0
        num_reviews = 0
        output_file = open("Results.txt", "w")
        t_imp = open("toImport.txt", "w")

        # Write headers for output files
        output_file.write("Dataset Analysed: " + self.filename + "\n")
        t_imp.write("Review Number, Review, Is_Comparative?, Comparative Word (If Any)\n")#Header for file to import

        #Iterate through lines of the file
        for x in self.mFile:
            # 0 for false, 1 for true
            is_comparative_review = 0

            # incremement num_reviews each time a new review is acessed
            num_reviews += 1

            # Clean text and remove punctuation 
            clean_text = self.cleaning_data(x)

            #Start writing in the files that will contain the obtained data
            output_file.write("Review " + str(num_reviews) + ":\n")
            output_file.write(clean_text + "\n")
            # find the number of times that each such key appears in text.
            # loop through all elements in the dictionary.
            # if they are found in the cleaned text, increment the dictionary value.
            for (regex, key) in zip(self.feature_dict_compiled, self.feature_dict):
                num_matches = len(re.findall(regex, clean_text))
                self.feature_dict[key] += num_matches
                if num_matches != 0:
                    is_comparative_review = 1

                    # write detected comparable word to the output file
                    output_file.write("Contains Comparable Word: "+key+"\n")
                    # write the word found in the review along with other information regarding the review
                    t_imp.write(str(num_reviews)+","+clean_text+","+str(1)+","+key+"\n")

            self.classification.append(is_comparative_review)
                    
            #Get Number of comparative reviews
            if is_comparative_review:
                num_comp_review += 1
            else:
                #Write that a comparative word was not found in the review
                t_imp.write(str(num_reviews) + "," + clean_text + "," + str(0) + "," + "None" + "\n")
                output_file.write("Does NOT Contain Comparable Words\n")
            #Set false for next review analysis
            is_comparative_review=False

            #Print line delimiting end of review
            output_file.write("**********************************************\n")
        output_file.close()
        t_imp.close()
        return num_comp_review, num_reviews

    #Print Summary of Search
    def get_summary(self):
        
        #Run comparable words identification algorithm
        result = self.comparative_feature_extraction()
        
        #Access obtained Values from identification algorithm
        filename= self.filename
        num_comp_review= result[0]
        num_reviews= result[1]

        #Get Product Name
        _position=filename.find('_')
        product_name=filename[0:_position]+" "+filename[_position+1:-4]

        #Get Sum of All Comparable Words
        sum_compwords=0
        for key in self.feature_dict:
            sum_compwords += self.feature_dict[key]
        
        #Get Precision
        precision=num_comp_review/(num_comp_review+(num_reviews-num_comp_review))

        #Print Basic Information and findings
        print("\n******************************************************")
        print('\033[1m'+'\033[4m'+"General Summary: \n"+'\033[0m')
        print("Product: "+ product_name)
        print("Data file: "+ filename)
        print("Number of Reviews: "+ str(num_reviews))
        print("Number of Comparabale Words: "+ str(sum_compwords))
        print("Number of Reviews containing comparable words: "+ str(num_comp_review))
        print("Average comprable words per Review: "+ str(round(sum_compwords/num_reviews,2)))
        print("Average comprable words per Comparable Review: "+ str(round(sum_compwords/num_comp_review,2)))
        print("Percentage of Comparable reviews from all reviews: " + str(round((num_comp_review/num_reviews)*100,2)))
        print("Precision: " + str(round((precision),2)) + "\n")
        #Print the ocurrences
        print('\033[1m'+'\033[4m'+"All Comparable Word Ocurrances: \n"+'\033[0m')
        for key in self.feature_dict:
            if self.feature_dict[key] != 0:
                print(key + ' -> ' + str(self.feature_dict[key]))
        
        print("******************************************************\n")
    
    # closes the dataset file
    def mFileClose(self):
        if not self.mFile.closed:
            self.mFile.close()
            return
        print("File is already closed")