# 🎬 Movie Database Application

A command-line movie database application that allows users to manage their movie collection with persistent storage using SQLite and SQLAlchemy.

## Features

### Core Functionality (CRUD)
- **Add movies** with title, year, and rating
- **List all movies** in your collection
- **Update movie** ratings and release years
- **Delete movies** from your database
- **Search movies** by partial title match
- **Fuzzy matching** for movie titles with suggestions

### Analytics & Organization
- **Statistics**: View average, median, best, and worst-rated movies
- **Random movie picker**: Get a random movie suggestion
- **Sort by rating**: View movies from highest to lowest rated
- **Sort by year**: View movies chronologically

### Technical Features
- **SQLite database** storage with SQLAlchemy ORM
- **Colorful CLI** interface with ANSI color codes
- **Input validation** for all user inputs
- **Error handling** for database operations
- **SQL injection protection** with parameter binding

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd movie-database
```

2. Install required dependencies:
```bash
pip install sqlalchemy
```

## Project Structure

```
movie-database/
│
├── movie_app.py           # Main application with CLI interface
├── movie_storage_sql.py   # SQLAlchemy database operations
├── test_storage.py        # Test script for database functions
├── movies.db             # SQLite database file (auto-created)
└── README.md             # This file
```

## Usage

### Running the Application

```bash
python movie_app.py
```

### Menu Options

```
********** 🎬 My Movies Database 🎬 **********

Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Movies sorted by year
```

### Example Usage

1. **Adding a movie**:
   - Select option 2
   - Enter movie title: "Inception"
   - Enter release year: 2010
   - Enter rating (0-10): 8.8

2. **Searching for movies**:
   - Select option 7
   - Enter partial title: "inc"
   - Shows all movies containing "inc" (case-insensitive)

3. **Viewing statistics**:
   - Select option 5
   - Displays average rating, median, best and worst movies

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL
)
```

## Testing

Run the test script to verify all database operations:

```bash
python test_storage.py
```

This will test:
- Adding a movie
- Listing all movies
- Updating a movie's rating
- Deleting a movie

## Development

### Debugging SQL Queries

To enable SQL query logging, set `echo=True` in `movie_storage_sql.py`:

```python
engine = create_engine(DB_URL, echo=True)
```

### Migration from JSON

If you have an existing `movies.json` file from a previous version, you can migrate your data using the migration script (if available).

## Future Enhancements

- [ ] API integration for automatic movie information fetching
- [ ] Web interface for better user experience
- [ ] Export/import functionality
- [ ] Multiple user support
- [ ] Movie genres and categories
- [ ] Watch history tracking

## Technologies Used

- **Python 3**: Core programming language
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database engine
- **ANSI Color Codes**: Terminal color formatting

## License

This project is part of a bootcamp assignment and is for educational purposes.

## Author

WBK

## Acknowledgments

- Built as part of the Web Development Bootcamp
- Inspired by the need for a simple movie tracking system