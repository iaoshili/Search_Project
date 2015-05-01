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
# from featx import label_feats_from_corpus, split_label_feats
# from featx import bag_of_words
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from nltk.classify.util import accuracy
from classification import precision_recall_fmeasure
from sklearn import svm
from sklearn.svm import NuSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline
from featx import high_information_words

'''
重要！请把workingDirectory修改成Data文件夹所在目录，以"/"结尾。
nltk使用参考：http://www.nltk.org/book/ch06.html
在这个例子里面，documents是一个list
每一个document包含两个fields，
一个是正文: a list of words (只是单词，不是chunk of words)
一个是category：neg或者
'''
TITLE_BONUS = 50
NUM_FEATUREWORDS = 3000

workingDirectory = "/Users/Greyjoy/Documents/Homework/Search_Project/Data/"

tagSet = set([u'tech',u'apple',u'google',u'microsoft',u'mobile',u'business',u'photography',u'home',u'apps',
u'science',u'entertainment',u'culture',u'gaming',u'web',u'movie-reviews',u'transportation',
u'design', u'architecture',u'typography',u'concepts',
u'us-world',u'business',u'politics',u'national-security',u'policy'])


'''
Input: data in json format. Containing keys: "Title", "Main text", "Tags"
Output: A list of tuple. 
Each tuple is composed of:
1 A list of strings extracted from title and main text.
2 The tag that is currently interested in bi-partitioning.
e.x. If is classifying between "tech" and "non-tech". These two will be the second element of the tuple.
'''
def getCleanStructuredData(data, tag):
	label = ""
	#Deal with text
	stopwordList = stopwords.words('english')
	stopwordList += string.punctuation

	chunk = " ".join([data["Title"][:-11]] * TITLE_BONUS) + " " + data["Main text"]
	tokens = WordPunctTokenizer().tokenize(chunk)
	stemmer = nltk.PorterStemmer()
	tokens = [stemmer.stem(t).lower() for t in tokens]
	tokens = [x for x in tokens if ((x in stopwordList) == False)]

	#Deal with tag
	if tag in data["Tags"]:
		label = tag
	else:
		label = "NotThis"

	cleanedData = []
	cleanedData.append(tokens)
	cleanedData.append(label)
	return cleanedData
		
def extractWordFeatureSet(cleanedDataCollection):
	wordList = []
	for data in cleanedDataCollection:
		text = data[0]
		wordList += text
	#Get a dictionary. Key is a word, value is how many time it occurs in the corpus
	all_words = nltk.FreqDist(w.lower() for w in wordList)
	#Sort the words in the order of their frequency. From high to low.
	sorted_freqWords = sorted(all_words.items(), key=operator.itemgetter(1), reverse = True)
	word_features = []
	for i in xrange(0,NUM_FEATUREWORDS):
		word_features.append(sorted_freqWords[i][0])
	return word_features

def extractBinaryWordFeatureOfADocument(document, word_features):
    document_words = set(document) 
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

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

def train(cleanedDataCollection, word_features, tagToBeTrained, high_info_wordSet):
	random.shuffle(cleanedDataCollection)
	featuresets = [(extractTfIdfFeatureOfADocument(d,word_features, high_info_wordSet), c) for (d,c) in cleanedDataCollection]
	train_set, test_set = featuresets[100:], featuresets[:100]

	# classifier = nltk.NaiveBayesClassifier.train(train_set)
	# print(nltk.classify.accuracy(classifier, test_set))
	# classifier.show_most_informative_features(5) 
	# return classifier

	sk_classifier = SklearnClassifier(svm.NuSVC())
	sk_classifier.train(train_set)
	print "accuracy is: %s" % (accuracy(sk_classifier, test_set))

	precision, recall, fMeasure = precision_recall_fmeasure(sk_classifier,  test_set, tagToBeTrained)

	print "precision is: %s" % (precision)
	print "recall is: %s" % (recall)
	print "F-measure is: %s" % (fMeasure)
	return sk_classifier


cleanedDataCollection = []
corpus = []
tagToBeTrained = "tech"
for fileName in os.listdir(workingDirectory):
	if "The Verge" not in fileName:
		continue
	filePath = workingDirectory + fileName
	with open(filePath) as data_file: 	
		input_file  = file(filePath, "r")
		data = json.loads(input_file.read())
		cleanedData = getCleanStructuredData(data, tagToBeTrained)
		# corpus.append(cleanedData[0])
		cleanedDataCollection.append(cleanedData)

# vectorizer = TfidfVectorizer(min_df=1,tokenizer=lambda doc: doc,lowercase=False)
# X = vectorizer.fit_transform(corpus)
# idf = vectorizer.idf_
# idfDict = dict(zip(vectorizer.get_feature_names(), idf))

currDir = os.getcwd()
f = open(currDir + '/idfDict.pickle', 'rb')
idfDict = pickle.load(f)
print len(idfDict.keys())
f.close()

wordsOfTheLabel = []
wordsWithOutTheLabel = []
for data in cleanedDataCollection:
	if tagToBeTrained == data[1]:
		wordsOfTheLabel += data[0]
	else:
		wordsWithOutTheLabel += data[0]

high_info_wordSet = set(high_information_words([(tagToBeTrained,wordsOfTheLabel), ( "NotThis",wordsWithOutTheLabel)]))
print len(high_info_wordSet)

# word_features = extractBinaryWordFeatureOfADocument(cleanedDataCollection)
classifier = train(cleanedDataCollection,idfDict, tagToBeTrained, high_info_wordSet)



# f = open('/Users/Greyjoy/Downloads/word_features.pickle', 'wb')
# pickle.dump(word_features, f)
# f.close()

# f = open('/Users/Greyjoy/Downloads/my_classifier.pickle', 'wb')
# pickle.dump(classifier, f)
# f.close()

