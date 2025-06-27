# Test script for SQLAlchemy storage functions
from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie

print("Testing Movie Storage with SQLAlchemy")
print("=" * 40)

# Test adding a movie
print("\n1. Adding 'Inception'...")
add_movie("Inception", 2010, 8.8)

# Test listing movies
print("\n2. Listing all movies:")
movies = list_movies()
# Format output to match expected style (even though it's not valid Python syntax)
if movies:
    # Print in a format similar to the expected output
    for title, info in movies.items():
        print(f"['{title}': {info}]")

# Test updating a movie's rating
print("\n3. Updating 'Inception' rating to 9.0...")
update_movie("Inception", 9.0)
print("After update:")
movies = list_movies()
if movies:
    for title, info in movies.items():
        print(f"['{title}': {info}]")

# Test deleting a movie
print("\n4. Deleting 'Inception'...")
delete_movie("Inception")
print("After deletion:")
movies = list_movies()
if movies:
    for title, info in movies.items():
        print(f"['{title}': {info}]")
else:
    print("[]")  # Empty list

# Test adding a movie again
print("\n1. Adding 'Inception'...")
add_movie("Inception", 2010, 8.8)

print("\n" + "=" * 40)
print("Test completed!")