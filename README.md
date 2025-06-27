# 🎬 Movie Database Application

A command-line movie database application with OMDb API integration, SQLite storage, and static website generation.

## Features

### Core Functionality
- **Add movies** automatically from OMDb API (year, rating, poster)
- **Dual rating system**: OMDb ratings + your personal ratings
- **Smart search** with suggestions for movie titles
- **SQLite database** with SQLAlchemy ORM
- **Static website generation** with movie posters
- **Color-coded CLI** with traffic light system for rating differences

### Movie Management
- List all movies with color-coded ratings
- Update your personal ratings (separate from OMDb)
- Delete movies with fuzzy matching
- Search movies by partial title
- Sort by rating or year
- View statistics (average, median, best/worst)
- Random movie picker

### API Integration
- Automatic movie data fetching from OMDb
- Year-specific movie selection for remakes/sequels
- Poster URL storage and local download
- Handles missing data gracefully

### Website Generation
- Beautiful grid layout with movie posters
- Automatic poster download and caching
- Dark gold (#B8860B) themed design
- Responsive layout (4/3/2 columns)
- Title/subtitle formatting for long names

## Prerequisites

- Python 3.7 or higher
- OMDb API key (free at https://www.omdbapi.com/apikey.aspx)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd movie-database
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API key:
```
OMDB_API_KEY=your_api_key_here
```

## Usage

### Running the Application

```bash
python movie_app.py
```

### Menu Options

```
0. Exit
1. List movies - View all with color-coded ratings
2. Add movie - Search and add from OMDb API  
3. Delete movie - Remove with fuzzy matching
4. Update movie - Add/change your personal rating
5. Stats - View collection statistics
6. Random movie - Get a random suggestion
7. Search movie - Find by partial title
8. Movies sorted by rating
9. Movies sorted by year
G. Generate website - Create static HTML site
```

### Adding Movies

1. Select option 2
2. Enter movie name (partial names work)
3. Choose from search results
4. Movie data is fetched automatically

### Rating System

The app uses a dual rating system:
- **OMDb Rating**: From the API (shown in cyan)
- **Your Rating**: Personal rating (color-coded)

Color coding for your ratings:
- 🟢 **Green**: Very close to OMDb (≤0.5 difference)
- 🟡 **Yellow**: Slightly different (0.5-1.5)
- 🟠 **Orange**: Quite different (1.5-2.5)
- 🔴 **Red**: Very different (>2.5)

### Website Generation

Press 'G' to generate a static website with:
- Movie poster grid
- Local poster storage in `website/images/`
- Black header with dark gold text
- Responsive design

## Project Structure

```
movie-database/
├── movie_app.py          # Main CLI application
├── movie_storage_sql.py  # SQLAlchemy database operations
├── movie_api.py          # OMDb API integration
├── website_generator.py  # Static site generator
├── .env                  # API key (not in git)
├── .env.example          # Template for API setup
├── requirements.txt      # Python dependencies
├── movies.db            # SQLite database
└── website/             # Generated website
    ├── index.html
    ├── style.css
    └── images/          # Downloaded posters
```

## Database Schema

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    omdb_rating REAL NOT NULL,
    user_rating REAL,
    poster TEXT,
    date_added TIMESTAMP,
    date_updated TIMESTAMP
)
```


```

## Troubleshooting

### API Issues
- Ensure your API key is valid in `.env`
- Check internet connection
- API has 1,000 daily request limit

### Database Issues
- Delete `movies.db` to start fresh
- Run migration scripts if upgrading

### Website Issues
- Posters download on first generation
- Check `website/images/` for cached posters

## Technologies Used

- **Python 3**: Core language
- **SQLAlchemy**: Database ORM
- **OMDb API**: Movie data source
- **SQLite**: Local database
- **Requests**: HTTP library
- **Python-dotenv**: Environment management

## License

Educational project for bootcamp purposes.

## Acknowledgments

- OMDb API for movie data
- Built as part of Masterschool curriculum