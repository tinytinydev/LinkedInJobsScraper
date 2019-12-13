import flask
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from rake_nltk import Rake

#Accenture URL: https://www.linkedin.com/jobs/view/1567822147/?alternateChannel=topapp

source_path = "https://www.linkedin.com/jobs/view/1613343431/?alternateChannel=jymbii"
page = requests.get(source_path)
page_content = page.content

soup = BeautifulSoup(page_content, 'html.parser')


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


r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

r.extract_keywords_from_text(content)

print(r.get_ranked_phrases()) # To get keyword phrases ranked highest to lowest.


