import re
import json
# import nltk
# tokens = nltk.word_tokenize(inputString)
# print(tokens)

def cleanText(text):
    out = text.lower()
    out = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", out) 
    out = re.sub(r" +", " ", out)
    return out

#Json file to Python Dictionary
feature_dict = {}
with open('comparative_dict.json') as json_file:
    feature_dict = json.load(json_file)
json_file.close()

# precompile regex list to improve performance
feature_dict_compiled = [re.compile(i) for i in feature_dict]

#  open data file to be analyzed
file_name = "./Data_Per_Product/Digital_Camera.txt"
file = open(file_name, "r")

# classification list
# 1 if the line is comparative, 0 if the line is not
classification = []
# loop through file and count occurrences of comparative words/phrases
for x in file:
    is_comparative = 0
    cleaned_line = cleanText(x)
    for (regex, feature) in zip(feature_dict_compiled, feature_dict):
        num_matches = len(re.findall(regex, cleaned_line))
        feature_dict[feature] += num_matches
        if num_matches != 0:
            is_comparative = 1
    classification.append(is_comparative)
file.close()

# print out all non-zero feature occurances
for key in feature_dict:
    if feature_dict[key] != 0:
        print(key + ' -> ' + str(feature_dict[key]))

# print classification of each line in the input file
for i in range(len(classification)):
    print("Line " + str(i) + ": " + str(classification[i]))