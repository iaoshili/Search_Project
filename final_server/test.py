from featx import high_information_words, bag_of_words_in_set
from nltk.corpus import movie_reviews
labels = movie_reviews.categories()
labeled_words = [(l, movie_reviews.words(categories=[l])) for l in labels]
print labeled_words[0]
# high_info_words = set(high_information_words(labeled_words))
# print high_info_words