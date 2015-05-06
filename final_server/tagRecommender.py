from keyWordExtraction import RakeKeywordExtractor
from nltk.corpus import wordnet as wn
import sys
import codecs
#print all the synset element of an element
def lemmalist(word):
    syn_set = []
    for synset in wn.synsets(word):
        for item in synset.lemmas():
            syn_set.append(item.name())
    return syn_set


f = codecs.open("raw_tags", encoding='utf-8')
lines = f.read()
f.close()
lines = lines.split("\n")
tags = []
for line in lines:
	rawTag = line.split()[:-2]
	tag = " ".join(rawTag)
	tags.append(tag.lower())


def YuanyiYangBigHandsomeGuy(text):
	rake = RakeKeywordExtractor()
	keywords = rake.extract(text, incl_scores=True)
	tagsInArticles = set()
	tagsRecommended = set()
	for keyword in keywords:
		tagsInArticles.add(keyword[0])
		similarWords = lemmalist(keyword[0])
		if len(similarWords) != 0:
			for word in similarWords:
				tagsRecommended.add(word)

	finalTagsRecommend = []

	for tag in tagsInArticles:
		if tag.lower() in tags:
			finalTagsRecommend.append(tag)

	for tag in tagsRecommended:
		if tag.lower() in tags:
			finalTagsRecommend.append(tag)

	return finalTagsRecommend

#Demo
# print YuanyiYangBigHandsomeGuy("Apple is a good product.")
