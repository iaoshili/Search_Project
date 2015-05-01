# -*- coding: utf-8 -*-

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


def getCleanStructuredData(text):
	#Deal with text
	stopwordList = stopwords.words('english')
	stopwordList += string.punctuation

	tokens = WordPunctTokenizer().tokenize(text)
	stemmer = nltk.PorterStemmer()
	tokens = [stemmer.stem(t).lower() for t in tokens]
	tokens = [x for x in tokens if ((x in stopwordList) == False)]

	cleanedData = tokens
	return cleanedData


def extractFeatureOfADocument(document, word_features):
    document_words = set(document) 
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def classifyDocument(inputFile):
	cleanedData = getCleanStructuredData(inputFile)
	currDir = os.getcwd()
	f = open(currDir + '/my_classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()

	f = open(currDir+'/word_features.pickle', 'rb')
	word_features = pickle.load(f)
	f.close()


	documentFeatures = extractFeatureOfADocument(cleanedData,word_features)
	print classifier.classify(documentFeatures)

classifyDocument("Apple is good. I would exchange my kidney for one apple product.")