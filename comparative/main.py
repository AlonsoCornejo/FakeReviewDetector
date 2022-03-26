# used to convert the JSON dictionary to a python dictionary object
import json

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

    # TODO clean text and remove punctuation 

    # find the number of times that each such key appears in text.
    # loop through all elements in the dictionary.
    # if they are found in the cleaned text, increment the dictionary value.
    for key in feature_dict:
        if key in text:
            feature_dict[key] += 1

    return feature_dict

# Driver
def main():
    input_str = 'I prefer apple to samsung. I prefer ethereum to bitcoin. I like google the most. Nokia is the best. Lamborghini is on par with Ferrari.'
    feature_dict = comparative_feature_extraction(input_str)
    for key in feature_dict:
        if feature_dict[key] != 0:
            print(key + ' -> ' + str(feature_dict[key]))

if __name__ == "__main__":
    main()