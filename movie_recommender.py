
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

## NOTE: There are 3 types of recommender models

## Popularity - Which is derived by suggesting movies based on how often they 
## are viewed and how long each duration of view is. In doing so, movies that are 
## viewed by more people will be suggested (similar to trending on Youtube or Netflix)

## Content - Which is derived from analyzing the actual content of each movie or text. In the 
## content based recommendation, we would consider recurring elements i.e texts, words, etc and find 
## other movies that have similar elements 

## Collaborative - Which is derived from considering the "taste and preferences" of like minded users
## I.e if user A likes movie 1 and user B also likes movie 1 and user A likes movie 2, user B will be suggested 
## movie 2 as the two users are considered to be similar

## The following algorithm uses the Content based approach! 

################################################################################################################
################################################################################################################

## Creates and prints head of DF for testing CSV

dataFrame = pd.read_csv("movie_dataset.csv");
#print dataFrame.head();
#print dataFrame.columns;

## Selects features to use to analyze when determining similarity 
## Hypothesis: Movies with the same cast, genres, director and keywords will likely be similar to the 
## extent that if an individual likes one they will like another

featuresToUse = ['cast', 'genres', 'director', 'keywords'];

## Cleans data cells as some contain NaN values 

for feature in featuresToUse:
	dataFrame[feature] = dataFrame[feature].fillna(" ")

def all_features(row):
	try: 
		return row['cast'] + " " + row['genres'] + " " + row['director'] + " " + row['keywords']
	except:
		print "Error in row", row

## Adds a combined features column to our data frame 

dataFrame["all_features"] = dataFrame.apply(all_features, axis = 1);
#print dataFrame["all_features"].head();

## Creates a count matrix for vector cosine distance comparisons across movies 

cv = CountVectorizer();
count_matrix = cv.fit_transform(dataFrame["all_features"]);
#print count_matrix.toarray();

similarityScore = cosine_similarity(count_matrix);
#print similarityScore;

################################################################################################################
################################################################################################################

## Testing for the movie Gone Girl

movieToTest = "Gone Girl"

def title_to_index(title):
	return dataFrame[dataFrame.title == title]["index"].values[0];

find_index = title_to_index(movieToTest);

scoredMovies = list(enumerate(similarityScore[find_index]));
sortedMovies = sorted(scoredMovies, key = lambda x:x[1], reverse = True);

def index_to_title(index):
	return dataFrame[dataFrame.index == index]["title"].values[0];

#print sortedMovies

i = 0; 

for movie in sortedMovies:
	print index_to_title(movie[0])
	i = i + 1;
	if i > 10:
		break;
