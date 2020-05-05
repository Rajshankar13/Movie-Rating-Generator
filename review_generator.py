import json
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


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
for review in all_reviews:
	list1 = list()
	for word in review:
		word = re.sub('[^a-zA-Z]', '', word)			#RE to remove everything that is not a word
		word = word.lower()
		if((word != '') and (word not in english_stop_words)):			#Remove stopwords
			list1.append(word)					#To remove empy word strings

	if(len(list1) != 0):
		cleaned_reviews.append(list1)					#To remove empty lists

def stemming(corpa):
	text = list()
	porter_stemmer = PorterStemmer()
	for word in corpa:
		text.append(porter_stemmer.stem(word))
	return text

stemmed_reviews = list()
for review in cleaned_reviews:
	stemmed_reviews.append(stemming(review))

print(stemmed_reviews)
