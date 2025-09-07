# %%
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ipywidgets import Text, Button, VBox
from IPython.display import display

# %%
#Data Collection 

# %%
movies = pd.read_csv("movies.csv")
movies.head(10)

# %%
#movies.count()
# total number of columns and rows
movies.shape


# %%
# only needed columns 
needed_col = ['genres','keywords','tagline','cast','director']

# %%
# replacing the null values with null string
for i in needed_col: 
    movies[i] = movies[i].fillna('')

# %%
# concatinating the columns
combined_movies = movies['genres']+' '+movies['keywords']+' '+movies['tagline']+' '+movies['cast']+' '+movies['director']

# %%
# converting text to vector
vector = TfidfVectorizer()

# %%
vectored = vector.fit_transform(combined_movies)
print(vectored)

# %%
#Cosine Similarity
simi = cosine_similarity(vectored)
print(simi)

# %%
simi.shape


# %%
#user giving input
#movie_name = input(' Enter your favourite movie name : ')
#print("You typed:", movie_name)

# %%
# Create a text box
movie_box = Text(description="Movie:")

# Create a button
button = Button(description="Submit")

# Function runs when button is clicked
def handle_submit(b):
    print("You entered:", movie_box.value)

button.on_click(handle_submit)

# Display input field + button in notebook
display(VBox([movie_box, button]))

# %%
list_of_all_titles = movies['title'].tolist()
print(list_of_all_titles)

# %%
# close match for the movie name user input
find_match = difflib.get_close_matches(movie_box.value, list_of_all_titles)
print(find_match)


# %%
best_match = find_match[0]
print(best_match)

# %%
#finding the index of the movie
indexofmovie = movies[ movies.title == best_match]['index'].values[0]
print(indexofmovie)

# %%
# getting the similar movies based on the index of the movie
similarity_score = list(enumerate(simi[indexofmovie]))
print(similarity_score)

# %%
#sorting the movies based on similarity score
Sorted_values = sorted(similarity_score, key = lambda x:x[1], reverse=True)
print(Sorted_values)


# %%
#print the name of similar movies based on index
print('Top 5 similar movies to '+ best_match + ' are : \n')
i = 1
for movie in Sorted_values:
    index = movie[0]
    title_from_index = movies[movies.index == index]['title'].values[0]
    if(i< 10):
        print(i, '.', title_from_index)
        i+=1

# %%
# Putting it all together in a function and displaying output in the notebook
movie_box = Text(description="Movie:")
button = Button(description="Submit")
output = Output()   #  this is where all print results go

def handle_submit(b):
    with output:  # capture print statements
        output.clear_output()  # clear previous results
        print("You entered:", movie_box.value)

        list_of_all_titles = movies['title'].tolist()
        find_match = difflib.get_close_matches(movie_box.value, list_of_all_titles)

        if not find_match:
            print("No close matches found. Try typing a valid movie name.")
            return

        best_match = find_match[0]
        indexofmovie = movies[movies.title == best_match]['index'].values[0]

        similarity_score = list(enumerate(simi[indexofmovie]))
        Sorted_values = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        print('Top 5 similar movies to ' + best_match + ' are : \n')
        i = 1
        for movie in Sorted_values:
            index = movie[0]
            title_from_index = movies[movies.index == index]['title'].values[0]
            if i < 6:   # exactly top 5
                print(i, '.', title_from_index)
                i += 1

button.on_click(handle_submit)

# Display everything together
display(VBox([movie_box, button, output]))



