from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine (set echo=True for debugging)
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
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
                                omdb_rating
                                REAL
                                NOT
                                NULL,
                                user_rating
                                REAL,
                                poster
                                TEXT,
                                date_added
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP,
                                date_updated
                                TIMESTAMP
                            )
                            """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                 SELECT title, year, omdb_rating, user_rating, poster
                 FROM movies
                 ORDER BY title
                 """)
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[3] if row[3] is not None else row[2],  # User rating takes precedence
            "omdb_rating": row[2],
            "user_rating": row[3],
            "poster": row[4]
        }
        for row in movies
    }


def add_movie(title, year, omdb_rating, poster=None):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, omdb_rating, poster) "
                    "VALUES (:title, :year, :omdb_rating, :poster)"
                ),
                {
                    "title": title,
                    "year": year,
                    "omdb_rating": omdb_rating,
                    "poster": poster
                }
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            # Execute DELETE query with parameter binding
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()

            # Check if any row was deleted
            if result.rowcount > 0:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, user_rating):
    """Update a movie's user rating in the database."""
    with engine.connect() as connection:
        try:
            # Execute UPDATE query with parameter binding
            result = connection.execute(
                text("""
                     UPDATE movies
                     SET user_rating  = :user_rating,
                         date_updated = CURRENT_TIMESTAMP
                     WHERE title = :title
                     """),
                {"title": title, "user_rating": user_rating}
            )
            connection.commit()

            # Check if any row was updated
            if result.rowcount > 0:
                print(f"Your personal rating for '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")


def reset_user_rating(title):
    """Remove user rating, reverting to OMDb rating."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("""
                     UPDATE movies
                     SET user_rating  = NULL,
                         date_updated = CURRENT_TIMESTAMP
                     WHERE title = :title
                     """),
                {"title": title}
            )
            connection.commit()

            if result.rowcount > 0:
                print(f"User rating for '{title}' removed.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")


# Wrapper functions for compatibility with the main program
def get_movies():
    """Wrapper for list_movies to maintain compatibility."""
    return list_movies()


def add_movie_to_storage(title, year, rating, poster=None):
    """Wrapper for add_movie to maintain compatibility."""
    add_movie(title, year, rating, poster)


def delete_movie_from_storage(title):
    """Wrapper for delete_movie to maintain compatibility."""
    delete_movie(title)


def update_movie_in_storage(title, rating, year):
    """Wrapper for update_movie to maintain compatibility.
    Note: Now only updates user rating, year parameter is ignored."""
    update_movie(title, rating)