import sqlite3
import os

# Database file name
DB_FILE = "movies.db"


def init_database():
    """Initialize the database and create the movies table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create movies table with id, title, year, and rating columns
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS movies
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       year
                       INTEGER
                       NOT
                       NULL,
                       rating
                       REAL
                       NOT
                       NULL
                   )
                   ''')

    conn.commit()
    conn.close()


def get_movies():
    """Load all movies from the database and return as a dictionary."""
    init_database()  # Ensure database exists

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Select all movies from the database
    cursor.execute('SELECT title, year, rating FROM movies')
    rows = cursor.fetchall()

    # Convert rows to dictionary format for compatibility with existing code
    movies = {}
    for title, year, rating in rows:
        movies[title] = {"year": year, "rating": rating}

    conn.close()
    return movies


def add_movie_to_storage(title, year, rating):
    """Add a new movie to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Insert new movie into the database
        cursor.execute('''
                       INSERT INTO movies (title, year, rating)
                       VALUES (?, ?, ?)
                       ''', (title, year, rating))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle case where movie already exists
        print(f"Movie '{title}' already exists in the database.")
    finally:
        conn.close()


def delete_movie_from_storage(title):
    """Delete a movie by title from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Delete movie with matching title
    cursor.execute('DELETE FROM movies WHERE title = ?', (title,))
    conn.commit()
    conn.close()


def update_movie_in_storage(title, rating, year):
    """Update movie rating and year in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Update movie information
    cursor.execute('''
                   UPDATE movies
                   SET rating = ?,
                       year   = ?
                   WHERE title = ?
                   ''', (rating, year, title))

    conn.commit()
    conn.close()


# Optional: Migration function to convert from JSON to SQLite
def migrate_from_json():
    """Migrate data from movies.json to SQLite database (one-time use)."""
    import json

    json_file = "movies.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                movies = json.load(f)

            for title, info in movies.items():
                add_movie_to_storage(title, info['year'], info['rating'])

            print(f"Migrated {len(movies)} movies from JSON to SQLite.")
        except Exception as e:
            print(f"Migration error: {e}")
    else:
        print("No movies.json file found to migrate.")