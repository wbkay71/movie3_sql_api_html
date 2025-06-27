import random
import statistics
from datetime import datetime
from movie_storage import (
    get_movies,
    add_movie_to_storage,
    delete_movie_from_storage,
    update_movie_in_storage
)

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
    """List all movies with their details."""
    clear_screen()
    movies = get_movies()
    if not movies:
        print_colored("No movies found in the database.", COLOR_ERROR)
        return

    print_colored(f"\n\U0001F39E\ufe0f  {len(movies)} movie(s):\n", COLOR_TITLE)
    for title, info in movies.items():
        print(
            f"Movie: \033[1;36m{title}\033[0m, Year: {info['year']}, "
            f"Rating: \033[1;33m{info['rating']:.2f}\033[0m"
        )


def add_movie():
    """Add a new movie after validating user input."""
    clear_screen()
    movies = get_movies()

    while True:
        title = input(f"{COLOR_INPUT}Enter movie name: {COLOR_RESET}").strip()
        if not title:
            print_colored("Title cannot be empty.", COLOR_ERROR)
            continue
        if title in movies:
            print_colored("Movie already exists!", COLOR_ERROR)
        else:
            break

    while True:
        try:
            msg = f"{COLOR_INPUT}Enter release year (1880–{current_year}): {COLOR_RESET}"
            year = int(input(msg))
            if 1880 <= year <= current_year:
                break
            print_colored(f"Please enter a year between 1880 and {current_year}.", COLOR_ERROR)
        except ValueError:
            print_colored("Invalid year. Please enter a valid number.", COLOR_ERROR)

    while True:
        try:
            rating = float(input(f"{COLOR_INPUT}Enter rating (0-10): {COLOR_RESET}"))
            if 0 <= rating <= 10:
                rating = round(rating, 2)
                break
            print_colored("Rating must be between 0 and 10.", COLOR_ERROR)
        except ValueError:
            print_colored("Invalid rating. Enter a number.", COLOR_ERROR)

    add_movie_to_storage(title, year, rating)
    print_colored(f"Added '{title}' ({year}) with rating {rating:.2f}", COLOR_INPUT)


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
    """Update rating and year for a movie, with suggestion-based lookup."""
    clear_screen()
    movies = get_movies()
    title_input = input(f"{COLOR_INPUT}Enter movie to update: {COLOR_RESET}").strip()

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
            prompt = f"{COLOR_INPUT}Enter number to update or 0 to cancel: {COLOR_RESET}"
            choice = int(input(prompt))
            if 1 <= choice <= len(suggestions):
                selected_title = suggestions[choice - 1]
            else:
                print_colored("Update cancelled.", COLOR_MENU)
                return
        except ValueError:
            print_colored("Invalid input. Update cancelled.", COLOR_ERROR)
            return

    while True:
        try:
            rating = float(input(f"{COLOR_INPUT}Enter new rating (0-10): {COLOR_RESET}"))
            if 0 <= rating <= 10:
                rating = round(rating, 2)
                break
            print_colored("Rating must be between 0 and 10.", COLOR_ERROR)
        except ValueError:
            print_colored("Invalid rating. Enter a number.", COLOR_ERROR)

    while True:
        try:
            prompt = (
                f"{COLOR_INPUT}Enter release year (1880–{current_year}): {COLOR_RESET}"
            )
            year = int(input(prompt))
            if 1880 <= year <= current_year:
                break
            print_colored(f"Please enter a year between 1880 and {current_year}.", COLOR_ERROR)
        except ValueError:
            print_colored("Invalid year. Please enter a valid number.", COLOR_ERROR)

    update_movie_in_storage(selected_title, rating, year)
    print_colored(
        f"Updated '{selected_title}' to rating {rating:.2f} and year {year}.",
        COLOR_INPUT
    )


def show_stats():
    """Display statistics about the stored movie ratings."""
    clear_screen()
    movies = get_movies()
    if not movies:
        print_colored("No movies to analyze.", COLOR_ERROR)
        return

    ratings = [info["rating"] for info in movies.values()]
    avg = sum(ratings) / len(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best = [title for title, info in movies.items() if info["rating"] == max_rating]
    worst = [title for title, info in movies.items() if info["rating"] == min_rating]

    print_colored(f"Average rating: {avg:.2f}", COLOR_TITLE)
    print_colored(f"Median rating: {med:.2f}", COLOR_TITLE)
    print_colored(f"Best movie(s): {', '.join(best)} ({max_rating:.2f})", COLOR_TITLE)
    print_colored(f"Worst movie(s): {', '.join(worst)} ({min_rating:.2f})", COLOR_TITLE)


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

        choice = input(f"{COLOR_INPUT}Enter choice (0-9): {COLOR_RESET}")
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
        elif choice == "0":
            print_colored("Exiting program. Goodbye! \U0001F44B", COLOR_INPUT)
            break
        else:
            print_colored(
                "Invalid input. Please enter a number between 0 and 9.",
                COLOR_ERROR
            )


# ---------- Entry Point ----------
if __name__ == "__main__":
    movie_database()
