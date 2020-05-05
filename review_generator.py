import json
import re


with open('movie_reviews/all_reviews.json', ) as f:
	reviews = json.load(f)

all_reviews = list()
cleaned_reviews = list()

for review in reviews:									#reviews is a list of dictionaries
	for value in review.values():
		for val in value:
			if(val != ' '):								#Checking if content is not null
				all_reviews.append(val.split())

for review in all_reviews:
	list1 = list()
	for word in review:
		word = re.sub('[^a-zA-Z]', '', word)			#RE to remove everything that is not a word
		if(word != ''):
			list1.append(word.lower())					#To remove empy eord strings

	if(len(list1) != 0):
		cleaned_reviews.append(list1)					#To remove empty lists

print(cleaned_reviews)
