import json
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle
import sys


movie_name = str(sys.argv[1])
movie_path = 'movie_reviews/' + movie_name + '.json'
details_dict = dict()

with open(movie_path, ) as f:
	reviews = json.load(f)

all_reviews = list()
cleaned_reviews = list()

for review in reviews:									#reviews is a list of dictionaries
	for value in review.values():
		for val in value:
			if(val != ' '):								#Checking if content is not null
				all_reviews.append(val.split())

# #Calculating ratings based on the scores given by the user at the site
# with open(movie_path, ) as f:
# 	ratings = json.load(f)

# all_ratings = list()

# for rating in ratings:
# 	for value in rating.values():
# 		value = int(value)
# 		all_ratings.append(value)

# total_sum = 0
# for rating in all_ratings:
# 	total_sum += rating
# #----------------------------------------------------------------------

english_stop_words = stopwords.words('english')
english_stop_words.remove("not")
english_stop_words.remove("no")
for review in all_reviews:
	list1 = list()
	for word in review:
		word = re.sub('[^a-zA-Z]', '', word)			#RE to remove everything that is not a word
		word = word.lower()
		if((word != '') and (word not in english_stop_words)):			#Remove stopwords
			list1.append(word)					#To remove empy word strings

	if(len(list1) != 0):
		cleaned_reviews.append(list1)					#To remove empty lists

#Perform Stemming
def stemming(corpa):
	text = list()
	porter_stemmer = PorterStemmer()
	for word in corpa:
		text.append(porter_stemmer.stem(word))
	return text

stemmed_reviews = list()
for review in cleaned_reviews:
	stemmed_reviews.append(stemming(review))

#Reading positive_words.txt and negative_words.txt
positive_words, negative_words = list(), list()
with open('positive-words.txt', ) as f:
	positive_words = stemming(f.read().split())
	positive_words = set(positive_words)				#Removing repeated words
	positive_words = list(positive_words)				#Converting back to list

with open('negative-words.txt', ) as f:
	negative_words = stemming(f.read().split())
	negative_words = set(negative_words)				#Removing repeated words
	negative_words = list(negative_words)				#Converting back to list

#Labelling the reviews
positive_reviews, negative_reviews, neutral_reviews, flag = 0, 0, 0, 0
most_positive, most_negative = 0, 0
review_index, positive_index, negative_index = -1, 0, 0
for review in stemmed_reviews:
	review_index += 1
	positive_word_count = 0
	negative_word_count = 0

	for word in review:
		if((word == "not") or (word == "no")):
			flag = 1
			continue

		if(flag == 1):
			if(word in positive_words):
				negative_word_count += 1

			elif(word in negative_words):
				positive_word_count += 1

			flag = 0
			continue

		if word in positive_words:
			positive_word_count += 1

		elif word in negative_words:
			negative_word_count += 1

	if(positive_word_count > negative_word_count):
		if((positive_word_count - negative_word_count) > most_positive):
			most_positive = positive_word_count
			positive_index = review_index
		review.append(1)								#Label review as positive
		positive_reviews += 1

	elif(positive_word_count < negative_word_count):
		if((negative_word_count - positive_word_count) > most_negative):
			most_negative = negative_word_count
			negative_index = review_index
		review.append(0)								#Label review as negative
		negative_reviews += 1

	else:
		review.append(2)								#Label review as neutral
		neutral_reviews += 1

formula1 = (positive_reviews + 0.5 * neutral_reviews) / (positive_reviews + negative_reviews)
formula2 = (positive_reviews + 0.5 * neutral_reviews) / (positive_reviews + negative_reviews + 0.5 * neutral_reviews)

# print(stemmed_reviews)
# print("Most Positive Review: ", cleaned_reviews[positive_index])
# print("---------------------------------------------------------")
# print("Most Negative Review: ", cleaned_reviews[negative_index])
# print("Total reviews: ", len(stemmed_reviews), "Positive Reviews: ", positive_reviews, 
# 	"Negative Reviews: ", negative_reviews, "Neutral Reviews: ", neutral_reviews)
# print("Formula 1: ", formula1, "Formula 2: ", formula2)
# print("Rating by user score: ", total_sum / len(ratings))
# for review in stemmed_reviews:
# 	if(review[-1] == 2):
# 		print(review)

details_dict['rating'] = formula2 * 10

most_positive_str = str()
most_negative_str = str()

for pos_str in cleaned_reviews[positive_index]:
	most_positive_str += pos_str + ' '

for neg_str in cleaned_reviews[negative_index]:
	most_negative_str += neg_str + ' '

details_dict['most_positive'] = most_positive_str
details_dict['most_negative'] = most_negative_str

with open('details.pickle', 'ab+') as f:
    pickle.dump(details_dict, f)