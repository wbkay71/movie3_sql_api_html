import random
import statistics
from datetime import datetime
from movie_api import get_movie_with_rating, search_movies
from movie_storage_sql import (
    get_movies,
    add_movie_to_storage,
    delete_movie_from_storage,
    update_movie_in_storage
)
import requests
from website_generator import generate_website

# ---------- Constants ----------
current_year = datetime.now().year
COLOR_TITLE = "\033[95m"
COLOR_MENU = "\033[94m"
COLOR_INPUT = "\033[92m"
COLOR_ERROR = "\033[91m"
COLOR_RESET = "\033[0m"


# ---------- Helper Functions ----------
def clear_screen():
    """Print blank lines to simulate clearing the terminal screen."""
    print("\n" * 50)


def print_colored(text, color_code):
    """Print the given text in the specified color."""
    print(f"{color_code}{text}{COLOR_RESET}")


# ---------- Core Functions ----------
def list_movies():
    """List all movies with their OMDb and user ratings."""
    clear_screen()
    movies = get_movies()
    if not movies:
        print_colored("No movies found in the database.", COLOR_ERROR)
        return

    print_colored(f"\n\U0001F39E\ufe0f  {len(movies)} movie(s):\n", COLOR_TITLE)

    # Calculate maximum title length for alignment
    max_title_length = max(len(title) for title in movies.keys()) if movies else 0

    for title, info in movies.items():
        # Format title with padding
        padded_title = title.ljust(max_title_length)

        # Format year
        year_str = f"({info['year']})"

        # Format OMDb rating (always in cyan/blue)
        omdb_rating = f"\033[1;36mOMDb: {info['omdb_rating']:.1f}\033[0m"

        # Check if user has rated the movie
        if info['user_rating'] is not None:
            # Calculate difference for color coding
            diff = abs(info['user_rating'] - info['omdb_rating'])

            # Ampel-System for user rating
            if diff <= 0.5:
                # Green - very close (≤ 0.5 difference)
                user_color = "\033[1;32m"  # Bright green
            elif diff <= 1.5:
                # Yellow - somewhat different (0.5 - 1.5)
                user_color = "\033[1;33m"  # Bright yellow
            elif diff <= 2.5:
                # Orange - quite different (1.5 - 2.5)
                user_color = "\033[38;5;208m"  # Orange (256 color)
            else:
                # Red - very different (> 2.5)
                user_color = "\033[1;31m"  # Bright red

            user_rating = f"{user_color}You: {info['user_rating']:.1f}\033[0m"
            rating_str = f"{omdb_rating} | {user_rating}"
        else:
            rating_str = omdb_rating

        # Print movie entry
        print(
            f"Movie: \033[1;36m{padded_title}\033[0m {year_str:6} - {rating_str}"
        )


def add_movie():
    """Add a new movie by fetching data from OMDb API."""
    clear_screen()
    movies = get_movies()

    # Get movie title from user
    while True:
        title = input(f"{COLOR_INPUT}Enter movie name: {COLOR_RESET}").strip()
        if not title:
            print_colored("Title cannot be empty.", COLOR_ERROR)
            continue
        break

    # Try to fetch movie data from API
    print_colored("Searching for movie data...", COLOR_MENU)

    try:
        # Always search first to show all options
        search_results = search_movies(title)

        if search_results:
            # Show all search results
            print_colored(f"\nFound {len(search_results)} movie(s):", COLOR_MENU)
            for i, movie in enumerate(search_results[:10], 1):  # Show up to 10 results
                print(f"{i}. {movie.get('Title')} ({movie.get('Year')})")

            print("0. Cancel")
            print("99. Search again with different title")

            # Let user select
            try:
                choice = int(input(f"\n{COLOR_INPUT}Select a movie to add: {COLOR_RESET}"))
                if choice == 0:
                    print_colored("Operation cancelled.", COLOR_MENU)
                    return
                elif choice == 99:
                    # Let user try again
                    print_colored("\nTips for better search results:", COLOR_MENU)
                    print("  - Try the complete movie title (e.g., 'The French Connection')")
                    print("  - For sequels, include the number (e.g., 'Godfather 2')")
                    print("  - Check spelling carefully")
                    print("  - Sometimes 'The' at the beginning helps")
                    add_movie()  # Recursive call
                    return
                elif 1 <= choice <= min(10, len(search_results)):
                    selected = search_results[choice - 1]
                    selected_title = selected.get('Title')

                    # Check if movie already exists
                    if selected_title in movies:
                        print_colored(f"\nMovie '{selected_title}' already exists in your database!", COLOR_ERROR)
                        return

                    # Fetch full data for selected movie WITH YEAR
                    selected_year = selected.get('Year')
                    api_data = get_movie_with_rating(selected_title, selected_year)
                    if api_data:
                        # Show movie details before adding
                        print_colored(f"\nAdding: {api_data['title']}", COLOR_TITLE)
                        print(f"Year: {api_data['year']}")
                        print(f"OMDb Rating: {api_data['rating']}/10")
                        if api_data.get('poster'):
                            print(f"Poster: Available")

                        # Add to database
                        add_movie_to_storage(
                            api_data['title'],
                            api_data['year'],
                            api_data['rating'],
                            api_data.get('poster')
                        )
                        print_colored(
                            f"\nSuccessfully added '{api_data['title']}' ({api_data['year']}) "
                            f"with OMDb rating {api_data['rating']:.1f}",
                            COLOR_INPUT
                        )
                        print_colored(
                            "Use 'Update movie' to add your personal rating.",
                            COLOR_MENU
                        )
                        return
                    else:
                        print_colored(
                            "Could not fetch complete data for this movie.",
                            COLOR_ERROR
                        )
                        return
                else:
                    print_colored("Invalid choice.", COLOR_ERROR)
                    return
            except ValueError:
                print_colored("Invalid input. Operation cancelled.", COLOR_ERROR)
                return
        else:
            # No results found
            print_colored(
                f"\nNo movies found for '{title}'.",
                COLOR_ERROR
            )
            print_colored(
                "Tips for better search results:",
                COLOR_MENU
            )
            print("  - Try the complete movie title")
            print("  - For sequels, include the number (e.g., 'Godfather 2')")
            print("  - Check spelling")
            print("  - Try without 'The' at the beginning")

            # Offer to search again
            retry = input(f"\n{COLOR_INPUT}Try another search? (y/n): {COLOR_RESET}").lower()
            if retry == 'y':
                add_movie()  # Recursive call
                return

    except requests.exceptions.ConnectionError:
        print_colored(
            "\nError: No internet connection.",
            COLOR_ERROR
        )
        print_colored(
            "Please check your connection and try again.",
            COLOR_ERROR
        )
    except requests.exceptions.Timeout:
        print_colored(
            "\nError: Request timed out.",
            COLOR_ERROR
        )
        print_colored(
            "Please try again later.",
            COLOR_ERROR
        )
    except Exception as e:
        print_colored(
            f"\nAn unexpected error occurred: {str(e)}",
            COLOR_ERROR
        )
        print_colored(
            "Please try again later.",
            COLOR_ERROR
        )

def delete_movie():
    """Delete a movie from the database, offering fuzzy match suggestions."""
    clear_screen()
    movies = get_movies()
    title_input = input(f"{COLOR_INPUT}Enter movie to delete: {COLOR_RESET}").strip()

    if title_input in movies:
        delete_movie_from_storage(title_input)
        print_colored(f"Deleted '{title_input}'.", COLOR_INPUT)
        return

    suggestions = [
        title for title in movies
        if title_input.lower() in title.lower()
    ]

    if not suggestions:
        print_colored("No matching movie found.", COLOR_ERROR)
        return

    print_colored("Did you mean one of these?", COLOR_MENU)
    for index, suggestion in enumerate(suggestions, start=1):
        print(f"{index}. {suggestion}")

    try:
        choice = int(input(f"{COLOR_INPUT}Enter number to delete or 0 to cancel: {COLOR_RESET}"))
        if 1 <= choice <= len(suggestions):
            selected_title = suggestions[choice - 1]
            delete_movie_from_storage(selected_title)
            print_colored(f"Deleted '{selected_title}'.", COLOR_INPUT)
        else:
            print_colored("No movie deleted.", COLOR_MENU)
    except ValueError:
        print_colored("Invalid input. No movie deleted.", COLOR_ERROR)


def update_movie():
    """Update your personal rating for a movie."""
    clear_screen()
    movies = get_movies()
    title_input = input(f"{COLOR_INPUT}Enter movie to rate: {COLOR_RESET}").strip()

    if title_input in movies:
        selected_title = title_input
    else:
        suggestions = [
            title for title in movies
            if title_input.lower() in title.lower()
        ]

        if not suggestions:
            print_colored("No matching movie found.", COLOR_ERROR)
            return

        print_colored("Did you mean one of these?", COLOR_MENU)
        for index, suggestion in enumerate(suggestions, start=1):
            print(f"{index}. {suggestion}")

        try:
            prompt = f"{COLOR_INPUT}Enter number to rate or 0 to cancel: {COLOR_RESET}"
            choice = int(input(prompt))
            if 1 <= choice <= len(suggestions):
                selected_title = suggestions[choice - 1]
            else:
                print_colored("Rating cancelled.", COLOR_MENU)
                return
        except ValueError:
            print_colored("Invalid input. Rating cancelled.", COLOR_ERROR)
            return

    # Show current movie data
    movie_data = movies[selected_title]
    print_colored(f"\nCurrent data for '{selected_title}':", COLOR_TITLE)
    print(f"Year: {movie_data['year']}")
    print(f"OMDb Rating: {movie_data['omdb_rating']:.1f}/10")
    if movie_data.get('user_rating') is not None:
        print(f"Your Current Rating: {movie_data['user_rating']:.1f}/10")
    else:
        print("Your Current Rating: Not rated yet")

    # Ask what to do
    print_colored("\nWhat would you like to do?", COLOR_MENU)
    print("1. Set/Update your personal rating")
    if movie_data.get('user_rating') is not None:
        print("2. Remove your rating (use OMDb rating only)")
    print("0. Cancel")

    try:
        action = input(f"\n{COLOR_INPUT}Select action: {COLOR_RESET}")

        if action == "1":
            # Set or update rating
            print_colored("\nEnter your personal rating for this movie.", COLOR_MENU)

            while True:
                try:
                    rating = float(input(f"{COLOR_INPUT}Your rating (0-10): {COLOR_RESET}"))
                    if 0 <= rating <= 10:
                        rating = round(rating, 1)
                        break
                    else:
                        print_colored("Rating must be between 0 and 10.", COLOR_ERROR)
                except ValueError:
                    print_colored("Invalid rating. Enter a number.", COLOR_ERROR)

            # Update the rating
            update_movie_in_storage(selected_title, rating, movie_data['year'])

            # Show rating comparison
            diff = rating - movie_data['omdb_rating']
            if diff > 0:
                comparison = f"(+{diff:.1f} higher than OMDb)"
            elif diff < 0:
                comparison = f"({diff:.1f} lower than OMDb)"
            else:
                comparison = "(same as OMDb)"

            print_colored(
                f"\nYour rating for '{selected_title}' is now {rating:.1f}/10 {comparison}",
                COLOR_INPUT
            )

        elif action == "2" and movie_data.get('user_rating') is not None:
            # Remove user rating
            from movie_storage_sql import reset_user_rating
            reset_user_rating(selected_title)
            print_colored(
                f"\nYour rating for '{selected_title}' has been removed.",
                COLOR_INPUT
            )
            print_colored(
                f"The movie now shows the OMDb rating of {movie_data['omdb_rating']:.1f}/10",
                COLOR_MENU
            )

        else:
            print_colored("Operation cancelled.", COLOR_MENU)

    except Exception as e:
        print_colored(f"Error: {str(e)}", COLOR_ERROR)


def show_stats():
    """Display statistics about the stored movie ratings."""
    clear_screen()
    movies = get_movies()
    if not movies:
        print_colored("No movies to analyze.", COLOR_ERROR)
        return

    # Separate OMDb and user ratings
    omdb_ratings = [info["omdb_rating"] for info in movies.values()]
    user_ratings = [info["user_rating"] for info in movies.values() if info["user_rating"] is not None]

    # OMDb Statistics
    print_colored("=== OMDb Ratings Statistics ===", COLOR_TITLE)
    avg_omdb = sum(omdb_ratings) / len(omdb_ratings)
    med_omdb = statistics.median(omdb_ratings)
    max_omdb = max(omdb_ratings)
    min_omdb = min(omdb_ratings)
    best_omdb = [title for title, info in movies.items() if info["omdb_rating"] == max_omdb]
    worst_omdb = [title for title, info in movies.items() if info["omdb_rating"] == min_omdb]

    print(f"Average rating: {avg_omdb:.2f}")
    print(f"Median rating: {med_omdb:.2f}")
    print(f"Best movie(s): {', '.join(best_omdb)} ({max_omdb:.1f})")
    print(f"Worst movie(s): {', '.join(worst_omdb)} ({min_omdb:.1f})")

    # User Statistics (if available)
    if user_ratings:
        print_colored("\n=== Your Personal Ratings Statistics ===", COLOR_TITLE)
        avg_user = sum(user_ratings) / len(user_ratings)
        med_user = statistics.median(user_ratings)
        max_user = max(user_ratings)
        min_user = min(user_ratings)
        best_user = [title for title, info in movies.items()
                     if info["user_rating"] is not None and info["user_rating"] == max_user]
        worst_user = [title for title, info in movies.items()
                      if info["user_rating"] is not None and info["user_rating"] == min_user]

        print(f"Movies you've rated: {len(user_ratings)} out of {len(movies)}")
        print(f"Your average rating: {avg_user:.2f}")
        print(f"Your median rating: {med_user:.2f}")
        print(f"Your favorite(s): {', '.join(best_user)} ({max_user:.1f})")
        print(f"Your least favorite(s): {', '.join(worst_user)} ({min_user:.1f})")

        # Rating difference analysis
        print_colored("\n=== Rating Differences ===", COLOR_TITLE)
        total_diff = 0
        higher_count = 0
        lower_count = 0
        same_count = 0

        for title, info in movies.items():
            if info["user_rating"] is not None:
                diff = info["user_rating"] - info["omdb_rating"]
                total_diff += abs(diff)
                if diff > 0:
                    higher_count += 1
                elif diff < 0:
                    lower_count += 1
                else:
                    same_count += 1

        avg_diff = total_diff / len(user_ratings) if user_ratings else 0
        print(f"Average difference from OMDb: {avg_diff:.2f}")
        print(f"You rated higher than OMDb: {higher_count} movie(s)")
        print(f"You rated lower than OMDb: {lower_count} movie(s)")
        print(f"You agreed with OMDb: {same_count} movie(s)")

        # Biggest differences
        differences = []
        for title, info in movies.items():
            if info["user_rating"] is not None:
                diff = info["user_rating"] - info["omdb_rating"]
                differences.append((title, diff))

        differences.sort(key=lambda x: abs(x[1]), reverse=True)
        if differences:
            print_colored("\nBiggest rating differences:", COLOR_MENU)
            for title, diff in differences[:3]:
                if diff > 0:
                    print(f"  - {title}: +{diff:.1f} (you liked it more)")
                else:
                    print(f"  - {title}: {diff:.1f} (you liked it less)")
    else:
        print_colored("\n[No personal ratings yet - use 'Update movie' to add your ratings]", COLOR_MENU)


def random_movie():
    """Display a randomly selected movie."""
    clear_screen()
    movies = get_movies()
    if not movies:
        print_colored("No movies to choose from.", COLOR_ERROR)
        return

    title = random.choice(list(movies.keys()))
    info = movies[title]
    print_colored(
        f"\n\U0001F3B2 Random pick: {title} ({info['year']}), "
        f"rating {info['rating']:.2f}",
        COLOR_TITLE
    )


def search_movie():
    """Search and display movies matching the input substring."""
    clear_screen()
    query = input(f"{COLOR_INPUT}Enter part of the movie name: {COLOR_RESET}").lower()
    movies = get_movies()
    results = {
        title: info
        for title, info in movies.items()
        if query in title.lower()
    }
    if results:
        print_colored(f"\nSearch results for '{query}':", COLOR_TITLE)
        for title, info in results.items():
            print(
                f"Movie: \033[1;36m{title}\033[0m, Year: {info['year']}, "
                f"Rating: \033[1;33m{info['rating']:.2f}\033[0m"
            )
    else:
        print_colored("No matches found.", COLOR_ERROR)


def sort_movies_by_rating():
    """Sort and display movies by rating in descending order."""
    clear_screen()
    movies = get_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print_colored("Movies sorted by rating:", COLOR_TITLE)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']:.2f}")


def sort_movies_by_year():
    """Sort and display movies by release year in ascending order."""
    clear_screen()
    movies = get_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["year"])
    print_colored("Movies sorted by year:", COLOR_TITLE)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']:.2f}")


# ---------- Main Program ----------
def movie_database():
    """Run the interactive movie database application."""
    print_colored("********** \U0001F3AC My Movies Database \U0001F3AC **********", COLOR_TITLE)
    while True:
        print_colored("\nMenu:", COLOR_MENU)
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Movies sorted by year")
        print("G. Generate website")  # New option!

        choice = input(f"{COLOR_INPUT}Enter choice (0-9 or G): {COLOR_RESET}").strip().upper()

        if choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            sort_movies_by_rating()
        elif choice == "9":
            sort_movies_by_year()
        elif choice == "G":
            generate_website()
            input(f"\n{COLOR_INPUT}Press Enter to continue...{COLOR_RESET}")
        elif choice == "0":
            print_colored("Exiting program. Goodbye! \U0001F44B", COLOR_INPUT)
            break
        else:
            print_colored(
                "Invalid input. Please enter a number between 0-9 or G.",
                COLOR_ERROR
            )

# ---------- Entry Point ----------
if __name__ == "__main__":
    movie_database()
