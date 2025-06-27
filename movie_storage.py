import json
import os

MOVIE_FILE = "movies.json"

def get_movies():
    """Load movies from file or return empty dict."""
    if not os.path.exists(MOVIE_FILE):
        return {}
    with open(MOVIE_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_movies(movies):
    """Write movies dictionary to JSON file."""
    with open(MOVIE_FILE, "w") as file:
        json.dump(movies, file, indent=4)

def add_movie_to_storage(title, year, rating):
    """Add a new movie and save to file."""
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)

def delete_movie_from_storage(title):
    """Delete a movie by title and save updated data."""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)

def update_movie_in_storage(title, rating, year):
    """Update movie rating and year."""
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        movies[title]["year"] = year
        save_movies(movies)