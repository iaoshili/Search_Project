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


def extractTfIdfFeatureOfADocument(document, idfDict, high_info_wordSet):
	features = {}
	for word in high_info_wordSet:
		features[word] = 0.0
	for word in document:
		if (word in high_info_wordSet) == False:
			continue
		else:
			features[word] += idfDict[word]
	return features

def loadClassifiers():
	classifiers = []
	currDir = os.getcwd()
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for f in files:
		if "classifier.pickle" in f:
			classifyF = open(currDir + '/'+f, 'rb')
			classifier = pickle.load(classifyF)
			classifiers.append(classifier)
			classifyF.close()
	return classifiers

def getTags(classifiers, documentFeatures):
	tags = []
	for classifier in classifiers:
		tag = classifier.classify(documentFeatures)
		if tag != "NotThis":
		 	tags.append(tag)
	return tags

#Input is string.
#Return a list of tags that correspond to this document.
def classifyDocument(inputFile):
	cleanedData = getCleanStructuredData(inputFile)
	currDir = os.getcwd()
	f = open(currDir+'/high_info_wordSet.pickle', 'rb')
	high_info_wordSet = pickle.load(f)
	f.close()

	f = open(currDir+'/idfDict.pickle', 'rb')
	idfDict = pickle.load(f)
	f.close()

	documentFeatures = extractTfIdfFeatureOfADocument(cleanedData,idfDict,high_info_wordSet)

	classifiers = loadClassifiers()
	tags = getTags(classifiers, documentFeatures)
	return tags

#Demo
# print classifyDocument("Apple is good. I would exchange my kidney for one apple product.")