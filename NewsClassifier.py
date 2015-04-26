# -*- coding: utf-8 -*-

from nltk.corpus import movie_reviews
import nltk
import random
import json
from pprint import pprint
from nltk import word_tokenize
import os
import codecs

'''
重要！请把workingDirectory修改成Data文件夹所在目录，以"/"结尾。
nltk使用参考：http://www.nltk.org/book/ch06.html
在这个例子里面，documents是一个list
每一个document包含两个fields，
一个是正文: a list of words (只是单词，不是chunk of words)
一个是category：neg或者
'''
TITLE_BONUS = 50

workingDirectory = "/Users/Greyjoy/Documents/Homework/Search_Project/Data/"

tagSet = set([u'tech',u'apple',u'google',u'microsoft',u'mobile',u'business',u'photography',u'home',u'apps',
u'science',u'entertainment',u'culture',u'gaming',u'web',u'movie-reviews',u'transportation',
u'design', u'architecture',u'typography',u'concepts',
u'us-world',u'business',u'politics',u'national-security',u'policy'])
documents = []
wordList = []

for fileName in os.listdir(workingDirectory):
	if "The Verge" not in fileName:
		continue
	filePath = workingDirectory + fileName
	with open(filePath) as data_file: 	
		# data = json.load(data_file)
		input_file  = file(filePath, "r")
		data = json.loads(input_file.read().decode("utf-8-sig"))

		oneOrMoreTagInTagSets = False
		for tag in data["Tags"]:
			if tag in tagSet:
				oneOrMoreTagInTagSets = True

		if oneOrMoreTagInTagSets == False:
			continue

		chunk = " ".join([data["Title"][:-11]] * TITLE_BONUS) + " " + data["Main text"]
		# chunk =  chunk.encode("utf-8")
		tokens = word_tokenize(chunk)
		porter = nltk.PorterStemmer()
		chunkList = [porter.stem(t).lower() for t in tokens]
		wordList += chunkList
		for tag in data["Tags"]:
			if tag not in tagSet:
				continue
			document = []
			document.append(chunkList)
			document.append(tag)
			documents.append(document)

# wordList = []
# for document in documents:
# 	wordList += document[0]

random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in wordList)
word_features = all_words.keys()[:2000]


def document_features(document):
    document_words = set(document) 
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5) 