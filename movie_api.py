import requests
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.environ.get('OMDB_API_KEY')
if not API_KEY:
    raise ValueError("OMDB_API_KEY not found in environment variables. Please check your .env file.")

BASE_URL = "http://www.omdbapi.com/"


def fetch_movie_data(title: str) -> Optional[Dict[str, Any]]:
    """
    Fetch movie data from OMDb API by title.

    Args:
        title (str): The movie title to search for

    Returns:
        Optional[Dict]: Movie data if found, None otherwise
    """
    # Prepare the request parameters
    params = {
        'apikey': API_KEY,
        't': title,  # 't' parameter searches by exact title
        'type': 'movie'  # Only search for movies, not TV series
    }

    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse JSON response
        data = response.json()

        # Check if movie was found
        if data.get('Response') == 'True':
            return data
        else:
            print(f"Movie not found: {data.get('Error', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse API response: {e}")
        return None


def search_movies(search_term: str) -> Optional[list]:
    """
    Search for movies by partial title match.

    Args:
        search_term (str): The search term

    Returns:
        Optional[list]: List of movie results if found, None otherwise
    """
    params = {
        'apikey': API_KEY,
        's': search_term,  # 's' parameter searches by partial title
        'type': 'movie'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get('Response') == 'True':
            return data.get('Search', [])
        else:
            print(f"No movies found: {data.get('Error', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None


def extract_movie_info(api_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant movie information from API response.

    Args:
        api_data (dict): Raw API response data

    Returns:
        dict: Cleaned movie data with year and rating
    """
    # Extract year (remove any extra characters)
    year_str = api_data.get('Year', 'N/A')
    try:
        # Handle cases like "2010-2011" by taking the first year
        year = int(year_str.split('–')[0].split('-')[0])
    except (ValueError, AttributeError):
        year = None

    # Extract IMDb rating
    rating_str = api_data.get('imdbRating', 'N/A')
    try:
        rating = float(rating_str)
    except (ValueError, TypeError):
        rating = None

    # Build the movie info dictionary
    movie_info = {
        'title': api_data.get('Title', 'Unknown'),
        'year': year,
        'rating': rating,
        'director': api_data.get('Director', 'N/A'),
        'actors': api_data.get('Actors', 'N/A'),
        'plot': api_data.get('Plot', 'N/A'),
        'genre': api_data.get('Genre', 'N/A'),
        'runtime': api_data.get('Runtime', 'N/A'),
        'poster': api_data.get('Poster', 'N/A')
    }

    return movie_info


def get_movie_with_rating(title: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get movie data with year and rating.

    Args:
        title (str): Movie title to search for

    Returns:
        Optional[Dict]: Dictionary with title, year, and rating if found
    """
    api_data = fetch_movie_data(title)

    if api_data:
        movie_info = extract_movie_info(api_data)

        # Check if we have the required data
        if movie_info['year'] and movie_info['rating']:
            return {
                'title': movie_info['title'],
                'year': movie_info['year'],
                'rating': movie_info['rating']
            }
        else:
            print(f"Incomplete data for '{title}'")
            return None

    return None


# Test function
if __name__ == "__main__":
    # Test the API with a known movie
    print("Testing OMDb API...")
    print("-" * 50)

    # Test exact title search
    movie_data = fetch_movie_data("Inception")
    if movie_data:
        info = extract_movie_info(movie_data)
        print(f"Found: {info['title']} ({info['year']})")
        print(f"Rating: {info['rating']}/10")
        print(f"Director: {info['director']}")
        print(f"Plot: {info['plot']}")

    print("\n" + "-" * 50)

    # Test search function
    print("\nSearching for 'Matrix'...")
    search_results = search_movies("Matrix")
    if search_results:
        for movie in search_results[:5]:  # Show first 5 results
            print(f"- {movie.get('Title')} ({movie.get('Year')})")