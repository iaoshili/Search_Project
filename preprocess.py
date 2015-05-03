from nltk.corpus import movie_reviews
import nltk
import random
import json
from pprint import pprint
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import WordPunctTokenizer
import os
import codecs
import operator
import string
import pickle
from collections import defaultdict
import logging

WORKING_DIR = "Data/"
Tags_Set = set()
REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "0123456789=[]\\\"\'")
tagSet = set([u'tech',u'apple',u'google',u'microsoft',u'mobile',u'business',u'photography',u'home',u'apps',
u'science',u'entertainment',u'culture',u'gaming',u'web',u'movie-reviews',u'transportation',
u'design', u'architecture',u'typography',u'concepts',
u'us-world',u'business',u'politics',u'national-security',u'policy'])

def main():
    f = open('yyy_tags.pkl', 'rb')
    all_tags = pickle.load(f)
    f.close()
    docList = []
    fullText = [] 
    classes_tag_dict = defaultdict(list)
    logging.info(len(os.listdir(WORKING_DIR)))
    for fileName in os.listdir(WORKING_DIR):
        if "The Verge" not in fileName:
            continue
        filePath = WORKING_DIR + fileName
        with open(filePath) as data_file:   
            input_file  = file(filePath, "r")
            data = json.loads(input_file.read())
            myTags = set()
            for tag in data['Tags']:
                tag = tag.translate(REMOVE_PUNCT_MAP)
                if len(tag) != 0:
                    temp = tag.split(",")
                for t in temp:
                    myTags.add(t)
            for tag in all_tags:
                if tag in myTags:
                    classes_tag_dict[tag].append(1)
                else:
                    classes_tag_dict[tag].append(0)
            stopwordList = stopwords.words('english')
            stopwordList += string.punctuation
            tokens = WordPunctTokenizer().tokenize(data['Main text'])
            stemmer = nltk.PorterStemmer()
            tokens = [stemmer.stem(t).lower() for t in tokens if t not in stopwordList]
            docList.append(tokens)
            fullText.extend(tokens)
    return docList, fullText, classes_tag_dict
        
def getAllTag():
    for fileName in os.listdir(WORKING_DIR):
        if "The Verge" not in fileName:
            continue
        filePath = WORKING_DIR + fileName
        with open(filePath) as data_file:   
            input_file  = file(filePath, "r")
            data = json.loads(input_file.read())
            tags = data['Tags']
            for tag in tags:
                tag = tag.translate(REMOVE_PUNCT_MAP)
                if len(tag) != 0:
                    temp = tag.split(",")
                for t in temp:
                    Tags_Set.add(t)
    f = open('yyy_tags.pkl', 'wb')
    pickle.dump(Tags_Set, f)
    f.close()

if __name__ == "__main__":
    #main()
    tagSet = list(tagSet)
    tags = {
        'tags' : tagSet
    }
    with open('tags.json', 'w') as outfile:
        json.dump(tags, outfile)

    

