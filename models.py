# models.py for Movie Night Planner
class Movie:
    def __init__(self, title, genre, rating, duration):
        """Initializes a Movie instance with title, genre, rating, and duration."""
        self.title = title
        self.genre = genre
        self.rating = float(rating)  # Ensure rating is a float
        self.duration = int(duration)  # Ensure duration is an integer
    def __str__(self):
        """Returns a nicely formatted string representation of the movie."""
        return f"{self.title} | Genre: {self.genre} | Rating: {self.rating} | Duration: {self.duration} mins"