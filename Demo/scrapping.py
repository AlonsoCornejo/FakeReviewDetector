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
        self.product="Ball"
        self.price=25
        self.review="This is the example Review"


    #Extract Title Product
    def extract_name(self):
        page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
        page.content

    #Test
    def getProduct(self):
        product=str(self.product)
        return product

    def getLink(self):
        hipervinculo=str(self.product_link)
        return hipervinculo

    def getPrice(self):
        price=str(self.price)
        return price

    def getReview(self):
        review=str(self.review)
        return review