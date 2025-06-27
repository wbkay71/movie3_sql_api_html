import os
import requests
import hashlib
from movie_storage_sql import get_movies
from datetime import datetime

# Output directory for the website
OUTPUT_DIR = "website"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
CSS_FILE = "style.css"
HTML_FILE = "index.html"


def create_output_directory():
    """Create the output directories if they don't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"Created directory: {IMAGES_DIR}")


def download_poster(poster_url, movie_title):
    """Download poster image and save locally."""
    if not poster_url or poster_url == 'N/A':
        return None

    try:
        # Create a safe filename from the movie title
        safe_title = "".join(c for c in movie_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length

        # Get file extension from URL
        ext = poster_url.split('.')[-1].split('?')[0]
        if ext not in ['jpg', 'jpeg', 'png', 'gif']:
            ext = 'jpg'

        filename = f"{safe_title}.{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)

        # Check if already downloaded
        if os.path.exists(filepath):
            return f"images/{filename}"

        # Download the image
        print(f"  Downloading poster for {movie_title}...")
        response = requests.get(poster_url, timeout=10)
        response.raise_for_status()

        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"images/{filename}"

    except Exception as e:
        print(f"  Failed to download poster for {movie_title}: {str(e)}")
        return None


def save_css():
    """Save the CSS file to the output directory."""
    css_content = """body {
  background: #F5F5F0;
  color: black;
  font-family: Monaco;
  margin: 0;
  padding: 20px;
}

.list-movies-title {
  padding: 10px 0;
  background: #000000;
  color: #B8860B;
  text-align: center;
  font-size: 16pt;
  margin: -20px -20px 0 -20px;
}

.movie-grid {
  list-style-type: none;
  padding: 0;
  margin: 0;
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 900px) {
  .movie-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 680px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.movie-grid li {
  display: flex;
  justify-content: center;
}

.movie {
  width: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movie-title {
  font-size: 0.85em;
  text-align: center;
  width: 100%;
  margin-top: 8px;
  font-weight: bold;
  line-height: 1.3;
  min-height: 2.6em;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

.movie-main-title {
  font-size: 1em;
  font-weight: bold;
  line-height: 1.2;
}

.movie-subtitle {
  font-size: 0.75em;
  font-weight: normal;
  color: #666;
  line-height: 1.2;
  margin-top: 2px;
}

.movie-year {
  font-size: 0.85em;
  text-align: center;
  width: 100%;
  color: #999;
  margin-top: 8px;
}

.movie-poster {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    width: 160px;
    height: 240px;
    object-fit: cover;
    display: block;
    background: #f0f0f0;
    border: 2px solid #B8860B;
    border-radius: 4px;
}

.movie-poster.no-poster {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ccc;
    color: #666;
    font-size: 0.9em;
    text-align: center;
    padding: 20px;
    box-sizing: border-box;
    font-family: Monaco;
    border: 2px solid #B8860B;
    border-radius: 4px;
}

.movie-rating {
    font-size: 0.8em;
    text-align: center;
    width: 100%;
    color: #333;
    font-weight: bold;
    margin-top: 6px;
}"""

    css_path = os.path.join(OUTPUT_DIR, CSS_FILE)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"Created CSS file: {css_path}")


def generate_movie_html(movie_data, local_poster_path=None):
    """Generate HTML for a single movie."""
    title = movie_data['title']
    year = movie_data['year']
    omdb_rating = movie_data['omdb_rating']
    user_rating = movie_data.get('user_rating')

    # Split title at colon or dash for better display
    title_parts = []
    if ':' in title:
        title_parts = title.split(':', 1)
    elif ' - ' in title:
        title_parts = title.split(' - ', 1)

    # Create title HTML
    if len(title_parts) == 2:
        title_html = f'''
            <div class="movie-title" title="{title}">
                <div>
                    <div class="movie-main-title">{title_parts[0].strip()}</div>
                    <div class="movie-subtitle">{title_parts[1].strip()}</div>
                </div>
            </div>'''
    else:
        title_html = f'<div class="movie-title" title="{title}">{title}</div>'

    # Use local poster if available, otherwise show placeholder
    if local_poster_path:
        poster_html = f'<img src="{local_poster_path}" alt="{title}" class="movie-poster">'
    else:
        poster_html = f'<div class="movie-poster no-poster">No poster<br>available</div>'

    # Create rating HTML
    rating_html = f'<div class="movie-rating">OMDb: {omdb_rating:.1f}'
    if user_rating is not None:
        rating_html += f' | You: {user_rating:.1f}'
    rating_html += '</div>'

    # Create movie HTML (using li for the template)
    movie_html = f"""
        <li>
            <div class="movie">
                {poster_html}
                {title_html}
                <div class="movie-year">{year}</div>
                {rating_html}
            </div>
        </li>"""

    return movie_html


def calculate_statistics(movies):
    """Calculate statistics for the movie collection."""
    if not movies:
        return None

    # Basic counts
    total_movies = len(movies)
    rated_by_user = sum(1 for m in movies.values() if m.get('user_rating') is not None)

    # OMDb statistics
    omdb_ratings = [m['omdb_rating'] for m in movies.values()]
    avg_omdb = sum(omdb_ratings) / len(omdb_ratings)
    highest_omdb = max(movies.items(), key=lambda x: x[1]['omdb_rating'])
    lowest_omdb = min(movies.items(), key=lambda x: x[1]['omdb_rating'])

    # User statistics
    user_ratings = [m['user_rating'] for m in movies.values() if m.get('user_rating') is not None]
    if user_ratings:
        avg_user = sum(user_ratings) / len(user_ratings)
        highest_user = max(
            ((k, v) for k, v in movies.items() if v.get('user_rating') is not None),
            key=lambda x: x[1]['user_rating']
        )
        lowest_user = min(
            ((k, v) for k, v in movies.items() if v.get('user_rating') is not None),
            key=lambda x: x[1]['user_rating']
        )
    else:
        avg_user = None
        highest_user = None
        lowest_user = None

    # Year statistics
    years = [m['year'] for m in movies.values()]
    newest = max(movies.items(), key=lambda x: x[1]['year'])
    oldest = min(movies.items(), key=lambda x: x[1]['year'])

    return {
        'total_movies': total_movies,
        'rated_by_user': rated_by_user,
        'avg_omdb': avg_omdb,
        'avg_user': avg_user,
        'highest_omdb': highest_omdb,
        'lowest_omdb': lowest_omdb,
        'highest_user': highest_user,
        'lowest_user': lowest_user,
        'newest': newest,
        'oldest': oldest
    }


def generate_statistics_html(stats):
    """Generate HTML for the statistics section."""
    if not stats:
        return ""

    html = '<div class="stats-section">'
    html += '<h2>Movie Collection Statistics</h2>'
    html += '<div class="stats-grid">'

    # Total movies
    html += f'''
    <div class="stat-item">
        <div class="stat-value">{stats['total_movies']}</div>
        <div class="stat-label">Total Movies</div>
    </div>'''

    # Movies rated by user
    html += f'''
    <div class="stat-item">
        <div class="stat-value">{stats['rated_by_user']}</div>
        <div class="stat-label">Rated by You</div>
    </div>'''

    # Average OMDb rating
    html += f'''
    <div class="stat-item">
        <div class="stat-value">{stats['avg_omdb']:.1f}</div>
        <div class="stat-label">Avg OMDb Rating</div>
    </div>'''

    # Average user rating
    if stats['avg_user']:
        html += f'''
        <div class="stat-item">
            <div class="stat-value">{stats['avg_user']:.1f}</div>
            <div class="stat-label">Avg Your Rating</div>
        </div>'''

    # Highest rated (OMDb)
    html += f'''
    <div class="stat-item">
        <div class="stat-value">{stats['highest_omdb'][1]['omdb_rating']:.1f}</div>
        <div class="stat-label">Highest OMDb<br>{stats['highest_omdb'][0][:20]}...</div>
    </div>'''

    # Newest movie
    html += f'''
    <div class="stat-item">
        <div class="stat-value">{stats['newest'][1]['year']}</div>
        <div class="stat-label">Newest Movie<br>{stats['newest'][0][:20]}...</div>
    </div>'''

    html += '</div></div>'
    return html


def generate_html(movies):
    """Generate the main HTML file using the provided template."""
    # Sort movies by title
    sorted_movies = sorted(movies.items(), key=lambda x: x[0].lower())

    # Download posters
    print("\nDownloading movie posters...")
    poster_paths = {}
    for title, data in sorted_movies:
        poster_url = data.get('poster')
        if poster_url and poster_url != 'N/A':
            local_path = download_poster(poster_url, title)
            if local_path:
                poster_paths[title] = local_path

    print(f"Downloaded {len(poster_paths)} posters")

    # Generate movie grid HTML
    movie_grid_html = ""
    for title, data in sorted_movies:
        movie_info = {
            'title': title,
            'year': data['year'],
            'omdb_rating': data['omdb_rating'],
            'user_rating': data.get('user_rating'),
            'poster': data.get('poster')
        }
        local_poster = poster_paths.get(title)
        movie_grid_html += generate_movie_html(movie_info, local_poster)

    # Use the provided template
    html_template = """<html>
<head>
    <title>My Movie App</title>
    <link rel="stylesheet" href="style.css"/>
</head>
<body>
<div class="list-movies-title">
    <h1>__TEMPLATE_TITLE__</h1>
</div>
<div>
    <ol class="movie-grid">
        __TEMPLATE_MOVIE_GRID__
    </ol>
</div>
</body>
</html>"""

    # Replace template variables
    html = html_template.replace("__TEMPLATE_TITLE__", f"My Movies ({len(movies)})")
    html = html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    return html


def generate_website():
    """Main function to generate the complete website."""
    print("Generating movie website...")
    print("-" * 40)

    # Create output directory
    create_output_directory()

    # Get movies from database
    movies = get_movies()
    if not movies:
        print("No movies found in database!")
        return

    print(f"Found {len(movies)} movies")

    # Save CSS file
    save_css()

    # Generate and save HTML
    html_content = generate_html(movies)
    html_path = os.path.join(OUTPUT_DIR, HTML_FILE)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created HTML file: {html_path}")

    print("-" * 40)
    print("Website generated successfully!")
    print(f"Open {html_path} in your browser to view.")

    # Try to open in default browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(html_path)}")
        print("Opening in browser...")
    except:
        pass


if __name__ == "__main__":
    generate_website()