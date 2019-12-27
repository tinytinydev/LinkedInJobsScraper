import flask
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from rake_nltk import Rake

#Accenture URL: https://www.linkedin.com/jobs/view/1567822147/?alternateChannel=topapp

source_path = "https://www.linkedin.com/jobs/view/1612246883/?alternateChannel=byview"
page = requests.get(source_path)
page_content = page.content

soup = BeautifulSoup(page_content, 'html.parser')


title = soup.find('title').get_text()
content = ""
pr = soup.find("div",{"class":"description__text"})

for child in pr.children:
    
    if child.name == 'ul':
        for grandchild in child:
                try:
                    content += grandchild.get_text() + '\n'
                except:
                    content += grandchild + '\n'
            
    else:
        try:
            content += child.get_text() + '\n'
        except:
            content += child + '\n'
       
    
word_arr = content.split(" ")
word_arr = [word for word in word_arr if word not in stopwords.words('english')]

filtered_str = ""

for word in word_arr:
    filtered_str += word + " "
    

additional_stop = ["finding", "looking","he","she"]
r = Rake(stopwords=additional_stop) # Uses stopwords for english from NLTK, and all puntuation characters.

#r.extract_keywords_from_text(content)

for line in filtered_str.split("\n"):
    r.extract_keywords_from_text(line)
    ranked_phrases = r.get_ranked_phrases_with_scores()

    for tup in ranked_phrases:
        if tup[0] >= 4.0:
            print(tup[1])
    
