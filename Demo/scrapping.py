import numpy as np
import nltk
from nltk import word_tokenize
from nltk import StanfordTagger
import requests
from bs4 import BeautifulSoup

class Scrapping:

    #Initialize Object
    def __init__(self):

        #Product Characteristics
        self.product_link = ""
        self.name="Kevin"
        self.price=0


    #Extract Title Product
    def extract_name(self):
        page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
        page.content

    #Test
    def getName(self):
        user=str(self.name)
        return user