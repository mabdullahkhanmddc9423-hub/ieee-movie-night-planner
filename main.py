import os
from models import Movie

def load_movies(file_path: str) -> list:
    """Loads movies dynamically from an external CSV file with error handling."""
    movies = []
    try:
        # Check if the CSV file exists before reading
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} was not found.")
            return movies

        # Open and read the file safely using a context manager
        with open(file_path, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # Skip the header row and loop through data lines
            for line_no, line in enumerate(lines[1:], start=2):
                try:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        raise ValueError(f"Malformed row at line {line_no}")
                    
                    title, genre, rating_str, duration_str = parts
                    movie = Movie(title, genre, float(rating_str), int(duration_str))
                    movies.append(movie)
                except ValueError as e:
                    # Catch and report bad rows without crashing the program
                    print(f"Warning: Skipping invalid record on line {line_no} -> {e}")
                    
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        
    return movies

def display_movies(movie_list):
    """Utility function to print a numbered list of movies."""
    if not movie_list:
        print("No movies found.")
        return
    for idx, movie in enumerate(movie_list, 1):
        print(f"{idx}. {movie}")

def main():
    # Set the path to the external data file
    csv_file = os.path.join("data", "movies.csv")
    movies_library = load_movies(csv_file)
    
    if not movies_library:
        print("Exiting program due to empty or missing movie library.")
        return

    watchlist = set()  # Set is used to prevent duplicate movies

    while True:
        # Display simplified 5-option menu
        print("\n=== MOVIE NIGHT PLANNER ===")
        print("1. View All Movies")
        print("2. Search & Filter Movies (Genre / Rating)")
        print("3. Add Movie to Watchlist")
        print("4. View Watchlist, Analytics & Remove")
        print("5. Exit")

        # Safely handle non-numeric user inputs
        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input! Please enter a valid number between 1 and 5.")
            continue

        # Option 1: View all loaded movies
        if choice == 1:
            print("\n--- Full Movie Library ---")
            display_movies(movies_library)

        # Option 2: Search & Filter (by Genre or Rating)
        elif choice == 2:
            print("\n--- Filter Options ---")
            print("1. Filter by Genre")
            print("2. Filter by Minimum Rating")
            sub_choice = input("Choose filter type (1 or 2): ").strip()
            
            if sub_choice == '1':
                search_genre = input("Enter genre (e.g., Sci-Fi, Action): ").strip().lower()
                filtered = [m for m in movies_library if m.genre.lower() == search_genre]
                print(f"\n--- Movies in Genre: {search_genre.title()} ---")
                display_movies(filtered)
            elif sub_choice == '2':
                try:
                    min_rating = float(input("Enter minimum rating (e.g., 8.0): "))
                    filtered = [m for m in movies_library if m.rating >= min_rating]
                    print(f"\n--- Movies with Rating >= {min_rating} ---")
                    display_movies(filtered)
                except ValueError:
                    print("Error: Please enter a valid numerical rating.")
            else:
                print("Invalid filter choice.")

        # Option 3: Add movie to watchlist
        elif choice == 3:
            print("\n--- Available Movies to Add ---")
            display_movies(movies_library)
            try:
                idx = int(input("Enter the number of the movie to add to watchlist: ")) - 1
                if 0 <= idx < len(movies_library):
                    selected_movie = movies_library[idx]
                    if selected_movie in watchlist:
                        print(f"'{selected_movie.title}' is already in your watchlist!")
                    else:
                        watchlist.add(selected_movie)
                        print(f"Success: '{selected_movie.title}' added to your watchlist.")
                else:
                    print("Error: Invalid movie number selection.")
            except ValueError:
                print("Error: Please enter a valid number.")

        # Option 4: View Watchlist, Analytics & Optional Removal
        elif choice == 4:
            if not watchlist:
                print("\nYour watchlist is currently empty.")
            else:
                print("\n=== Your Curated Watchlist ===")
                watchlist_list = list(watchlist)
                display_movies(watchlist_list)
                
                # Calculate total duration and average rating
                total_duration = sum(m.duration for m in watchlist)
                avg_rating = sum(m.rating for m in watchlist) / len(watchlist)
                
                print("\n--- Watchlist Analytics ---")
                print(f"Total Movies: {len(watchlist)}")
                print(f"Total Duration: {total_duration} minutes ({total_duration / 60:.2f} hours)")
                print(f"Average Rating: {avg_rating:.2f}★")
                
                # Option to remove a movie from the watchlist
                remove_choice = input("\nDo you want to remove a movie from your watchlist? (y/n): ").strip().lower()
                if remove_choice == 'y':
                    try:
                        rem_idx = int(input("Enter the number of the movie to remove: ")) - 1
                        if 0 <= rem_idx < len(watchlist_list):
                            removed_movie = watchlist_list[rem_idx]
                            watchlist.remove(removed_movie)
                            print(f"Success: '{removed_movie.title}' removed from watchlist.")
                        else:
                            print("Error: Invalid number.")
                    except ValueError:
                        print("Error: Please enter a valid number.")

        # Option 5: Exit application
        elif choice == 5:
            print("Exiting Movie Night Planner. Enjoy your movie night!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")

if __name__ == "__main__":
    main()