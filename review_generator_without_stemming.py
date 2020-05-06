import json
import re
from nltk.corpus import stopwords


with open('movie_reviews/all_reviews.json', ) as f:
	reviews = json.load(f)

all_reviews = list()
cleaned_reviews = list()

for review in reviews:									#reviews is a list of dictionaries
	for value in review.values():
		for val in value:
			if(val != ' '):								#Checking if content is not null
				all_reviews.append(val.split())

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

#Reading positive_words.txt and negative_words.txt
positive_words, negative_words = list(), list()
with open('positive-words.txt', ) as f:
	positive_words = f.read().split()

with open('negative-words.txt', ) as f:
	negative_words = f.read().split()

#Labelling the reviews
positive_reviews, negative_reviews, neutral_reviews, flag = 0, 0, 0, 0
for review in cleaned_reviews:
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
		review.append(1)								#Label review as positive
		positive_reviews += 1

	elif(positive_word_count < negative_word_count):
		review.append(0)								#Label review as negative
		negative_reviews += 1

	else:
		review.append(2)								#Label review as neutral
		neutral_reviews += 1

# print(stemmed_reviews)
print("Total reviews: ", len(cleaned_reviews), "Positive Reviews: ", positive_reviews, 
	"Negative Reviews: ", negative_reviews, "Neutral Reviews: ", neutral_reviews)

for review in cleaned_reviews:
	if(review[-1] == 2):
		print(review)