#!/usr/bin/env python
# coding: utf-8

# Lab 7 (Web Scraping from a Blog page)
# 
# Web Scraping using Python
# 
# We use BeautifulSoup package in Python - to perform web scraping, whereby
# we attempt to extract out only certain text content.
# 
# In this lab, we attempt to scrape a local Singaporean influencer's blog content at this site:
# http://www.mongabong.com/2017/08/largest-executive-condo-sol-acres.html
# 
# We are particularly interested in extracting a given blog entry's:
# 1) Title
# 2) Date (of entry)
# 3) Blog content (essay)

# In[29]:



import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


# In[25]:




#Accenture URL: https://www.linkedin.com/jobs/view/1567822147/?alternateChannel=topapp

source_path = "https://www.linkedin.com/jobs/view/1613343431/?alternateChannel=jymbii"
page = requests.get(source_path)
page_content = page.content

print(page_content)


# In[26]:



soup = BeautifulSoup(page_content, 'html.parser')

print (soup.prettify())


# In[55]:


# title
title = soup.find('title').get_text()


content = ""

pr = soup.find("div",{"class":"description__text"})



for child in pr.children:
    
    if child.name == 'ul':
        for grandchild in child:
            content += grandchild.get_text() + '\n'
            
    else:

        content += child.get_text() + '\n'
       
    
word_arr = content.split(" ")
word_arr = [word for word in word_arr if word not in stopwords.words('english')]

filtered_str = ""

for word in word_arr:
    filtered_str += word + " "
    

print(filtered_str)


# In[53]:


from rake_nltk import Rake

r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

r.extract_keywords_from_text(content)

r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.


# In[ ]:





# In[ ]:





# In[ ]:




