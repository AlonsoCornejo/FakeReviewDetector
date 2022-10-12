from contextlib import closing
import re
import numpy as np
import nltk
from nltk import word_tokenize
from nltk import StanfordTagger
import requests
from bs4 import BeautifulSoup
import string

url = "https://www.newegg.ca/gigabyte-geforce-rtx-3080-ti-gv-n308tgaming-oc-12gd/p/N82E16814932436?Description=3080&cm_re=3080-_-14-932-436-_-Product"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

#Price
prices = doc.find_all(text="$")
parent = prices[0].parent
strong = parent.find("strong")

#Product Title
div_class_tit=doc.find(class_="product-wrap")
title=div_class_tit.find_all('h1')

#Description
div_class_des=doc.find(class_="article")
div_subclass_des=doc.find(class_="a-plus-info")
desc=""

for i in range(7):
    desc=desc+str(div_subclass_des.select('br')[i].previous_sibling)+"||"

#Reviews
comment_list = [div for div in doc.find_all('div', class_="comments-content")]
p_list = [div.find_all('p') for div in comment_list]
all_reviews = [item.text.strip() for p in p_list for item in p]

overall_reviews=[]
i=2
while (i<len(all_reviews)):
    overall_reviews.append(all_reviews[i])
    i=i+3

print(overall_reviews)
