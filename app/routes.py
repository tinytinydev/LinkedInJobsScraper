from flask import Blueprint, render_template, abort
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from nltk.corpus import stopwords
from rake_nltk import Rake
from flask import jsonify, request, render_template

routing = Blueprint("Routing",__name__,template_folder='templates')

@routing.route('/')
@routing.route('/index')
def test():
    return render_template('index.html', title='Home')

@routing.route('/api/xtract',methods=['POST'])
def keyword_PAI():
    source_path = request.json.get('url')
    return extract_info(source_path)
    
@routing.route('/view/xtract',methods=['POST'])
def keyword_form():

    data = request.form.to_dict(flat=False)

    source_path = request.form['url']
    print("URL: " + source_path)
    xtracted_info = extract_info(source_path)

    return render_template('xtracted.html', title='Xtracted',keywords= xtracted_info["keywords"],must=xtracted_info["must"],html=xtracted_info["html"])

def extract_info(source_path):
    page = requests.get(source_path)
    page_content = page.content

    soup = BeautifulSoup(page_content, 'html.parser')
    try:
        print(soup.find('title'))
        title = soup.find('title') #Job Posting title

        if type(title) != 'NoneType':
            title = title.get_text()
    except:
        print("title not found")
    company = soup.find("a",{"class":"topcard__org-name-link"}).get_text() #Company Name

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
        
    original_content = content

    original_content = original_content.replace("\n","</br>")

    content = content.lower()
        
    word_arr = content.split(" ")

    extra_stop_words = ['you' , 'it' , 'would']
    word_arr = [word for word in word_arr if word not in stopwords.words('english')]
    word_arr = [word for word in word_arr if word not in extra_stop_words]

    filtered_str = ""

    for word in word_arr:
        filtered_str += word + " "
        

    return {"keywords": get_keywords(filtered_str),"must": get_musthave(filtered_str),"html":original_content} # To get keyword phrases ranked highest to lowest.

def get_keywords(content):
    keywords = []
    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
    for line in content.split("\n"):
        r.extract_keywords_from_text(line)
        keywordsInSentence = r.get_ranked_phrases_with_scores()

        for tup in keywordsInSentence:
            if tup[0] >= 30.0:
                keywords.append(tup[1])

    return keywords # To get keyword phrases ranked highest to lowest.


def get_musthave(content):
    
    must_keywords = ["must", "strong", "required","have","preferred","least"]
    must_content = []
    
    sentences = []
    
    for line in content.split('\n'):
        for sentence in line.split('.'):
            sentences.append(sentence)
    
    
    for sentence in sentences:
        for word in sentence.split(' '):
            if word in must_keywords:
                must_content.append(sentence)

                
    print(str(len(must_content)))
    return must_content
    
