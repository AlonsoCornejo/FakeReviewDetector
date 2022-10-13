import re
import numpy as np
import nltk
from nltk import word_tokenize
from nltk import StanfordTagger
import requests
from bs4 import BeautifulSoup

class Scrapping:

    #Initialize Object
    def __init__(self,link):

        #Product Characteristics
        self.product_link = link
        self.product=""
        self.description=""
        self.price=0
        self.review=[]
        
    #Setters
    def setLink(self,link):
        self.product_link=link

    def setProduct(self,name):
        self.product=name
    
    def setDescription(self,description):
        self.description=description

    def setPrice(self,amount):
        self.price=amount
    
    def setReview(self,text):
        self.review=text

    #Test Getters
    def getLink(self):
        hipervinculo=str(self.product_link)
        return hipervinculo

    def getProduct(self):
        product=str(self.product)
        return product
    
    def getDescription(self):
        descripcion=str(self.description)
        return descripcion

    def getPrice(self):
        price=str(self.price)
        return price

    def getReview(self):
        review=str(self.review)
        return review
    
    #Scrap Information on web
    def scrap(self,url):
        
        #Access webpage html doc
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")

        #Product Title Scrapping
        div_class=doc.find(class_="product-wrap")
        title=div_class.find_all('h1')
        self.setProduct(title[0].string)

        #Description Scrapping
        div_subclass_des=doc.find(class_="a-plus-info")
        desc=""

        for i in range(7):
            desc=desc+str(div_subclass_des.select('br')[i].previous_sibling)+"||"
        
        self.setDescription(desc)

        #Price Scrapping
        prices = doc.find_all(text="$")
        parent = prices[0].parent
        strong = parent.find("strong")
        self.setPrice(strong.string)

        #Reviews
        comment_list = [div for div in doc.find_all('div', class_="comments-content")]
        p_list = [div.find_all('p') for div in comment_list]
        all_reviews = [item.text.strip() for p in p_list for item in p]

        overall_reviews=[]
        i=2
        while (i<len(all_reviews)):
            overall_reviews.append(all_reviews[i])
            i=i+3

        self.setReview(overall_reviews)

    #Get Reviews on Text File
    def reviews2textFile(self):
        temp = open("temp.txt", "w")

        #Add Reviews
        for i in self.review:
            temp.write(i+'\n')

        temp.close()

        #Erase Blank Lines
        with open("temp.txt", 'r') as tempo, open('input_reviews.txt', 'w') as reviews:
            for line in tempo:
                if line.strip():
                    reviews.write(line)

        

        
        