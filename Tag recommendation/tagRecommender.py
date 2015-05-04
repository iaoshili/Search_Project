from keyWordExtraction import RakeKeywordExtractor
from nltk.corpus import wordnet as wn
import sys
#print all the synset element of an element
def lemmalist(word):
    syn_set = []
    for synset in wn.synsets(word):
        for item in synset.lemmas():
            syn_set.append(item.name())
    return syn_set


rake = RakeKeywordExtractor()
keywords = rake.extract("""
Compatibility of systems of linear constraints over the set of natural 
numbers. Criteria of compatibility of a system of linear Diophantine 
equations, strict inequations, and nonstrict inequations are considered. 
Upper bounds for components of a minimal set of solutions and algorithms 
of construction of minimal generating sets of solutions for all types of 
systems are given. These criteria and the corresponding algorithms for 
constructing a minimal supporting set of solutions can be used in solving 
all the considered types of systems and systems of mixed types.
""", incl_scores=True)
tagsInArticles = set()
tagsRecommended = set()
for keyword in keywords:
	tagsInArticles.add(keyword[0])
	similarWords = lemmalist(keyword[0])
	if len(similarWords) != 0:
		for word in similarWords:
			tagsRecommended.add(word)

print "Tags directly recommended from article are: "
for word in tagsInArticles:
	print word

print "*====================*"

print "Tags recommended are: "
for word in tagsRecommended:
	print word