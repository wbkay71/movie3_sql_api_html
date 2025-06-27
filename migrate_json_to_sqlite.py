import json
import sqlite3
import os


def migrate_json_to_sqlite():
    """
    This script migrates your movie data from movies.json to movies.db
    Run this ONCE to transfer all your existing data!
    """

    # Check if JSON file exists
    if not os.path.exists("movies.json"):
        print("❌ No movies.json file found!")
        print("Make sure movies.json is in the same directory as this script.")
        return

    # Read the JSON file
    print("📖 Reading movies.json...")
    try:
        with open("movies.json", "r") as file:
            movies_data = json.load(file)
        print(f"✓ Found {len(movies_data)} movies in JSON file")
    except json.JSONDecodeError:
        print("❌ Error: movies.json is not valid JSON!")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Connect to SQLite database
    print("\n🗄️ Connecting to SQLite database...")
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Create the movies table if it doesn't exist
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
    print("✓ Database table ready")

    # Migrate each movie
    print("\n🔄 Migrating movies...")
    success_count = 0
    error_count = 0

    for title, info in movies_data.items():
        try:
            cursor.execute('''
                           INSERT INTO movies (title, year, rating)
                           VALUES (?, ?, ?)
                           ''', (title, info['year'], info['rating']))
            success_count += 1
            print(f"  ✓ Added: {title}")
        except sqlite3.IntegrityError:
            print(f"  ⚠️ Skipped: {title} (already exists)")
            error_count += 1
        except Exception as e:
            print(f"  ❌ Error adding {title}: {e}")
            error_count += 1

    # Save changes
    conn.commit()
    print(f"\n✅ Migration complete!")
    print(f"   - Successfully migrated: {success_count} movies")
    print(f"   - Skipped/Errors: {error_count} movies")

    # Show what's in the database now
    cursor.execute("SELECT COUNT(*) FROM movies")
    total_count = cursor.fetchone()[0]
    print(f"   - Total movies in database: {total_count}")

    # Show a few examples
    print("\n📽️ Sample movies in database:")
    cursor.execute("SELECT title, year, rating FROM movies LIMIT 5")
    for title, year, rating in cursor.fetchall():
        print(f"   - {title} ({year}): {rating}")

    conn.close()

    # Ask if user wants to delete the JSON file
    print("\n" + "=" * 50)
    response = input("Delete movies.json after successful migration? (y/n): ")
    if response.lower() == 'y':
        os.remove("movies.json")
        print("✓ movies.json deleted")
    else:
        print("✓ movies.json kept as backup")


# Run the migration
if __name__ == "__main__":
    print("🎬 MOVIE DATABASE MIGRATION TOOL 🎬")
    print("=" * 50)
    migrate_json_to_sqlite()