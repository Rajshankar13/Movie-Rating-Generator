import json


with open('movie_reviews/avatar_ratings.json', ) as f:
	ratings = json.load(f)

all_ratings = list()

for rating in ratings:
	for value in rating.values():
		value = int(value)
		all_ratings.append(value)

total_sum = 0
for rating in all_ratings:
	total_sum += rating

print("Total Sum: ", total_sum)
print("Rating: ", total_sum / len(all_ratings))