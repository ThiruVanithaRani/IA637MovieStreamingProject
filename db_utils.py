import pymysql
import yaml

# Load database configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

db_config = config["db"]

def get_connection():
    """Establish a database connection."""
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["db"],
        port=db_config["port"],
        cursorclass=pymysql.cursors.DictCursor
    )

def get_user(username, password):
    """Fetch user based on credentials."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Users WHERE UserName = %s AND Password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()
    finally:
        connection.close()

def fetch_users():
    """Fetch all users and their details."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch user details
            query = "SELECT UserID, UserName, UserType FROM Users"
            cursor.execute(query)
            users = cursor.fetchall()

            # Fetch total count of users
            count_query = "SELECT COUNT(*) AS total_users FROM Users"
            cursor.execute(count_query)
            total_users = cursor.fetchone()['total_users']

        return users, total_users
    finally:
        connection.close()


def register_user(username, password):
    """Register a new user."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Users (UserName, Password, UserType) VALUES (%s, %s, 'user')"
            cursor.execute(query, (username, password))
            connection.commit()
    finally:
        connection.close()

'''def fetch_movies():
    """Fetch all movies with platforms, ratings, and comments."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                m.MovieID, 
                m.Title, 
                m.Description, 
                m.Genre, 
                sp.PlatformName,
                mp.StartDate, 
                mp.EndDate,
                AVG(wm.Rating) AS AvgRating, 
                GROUP_CONCAT(wm.Comment SEPARATOR '; ') AS Comments
            FROM 
                Movies m
            LEFT JOIN 
                MovieStreamingPlatforms mp ON m.MovieID = mp.MovieID
            LEFT JOIN 
                StreamingPlatforms sp ON mp.PlatformID = sp.PlatformID
            LEFT JOIN 
                WatchedMovies wm ON m.MovieID = wm.MovieID
            GROUP BY 
                m.MovieID, m.Title, m.Description, m.Genre, sp.PlatformName, mp.StartDate, mp.EndDate
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []
    finally:
        connection.close()'''

def fetch_movies():
    """Fetch all movies with their average ratings."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                m.MovieID, 
                m.Title, 
                m.Description, 
                m.Genre, 
                sp.PlatformName AS Platform,
                mp.StartDate, 
                mp.EndDate,
                COALESCE(AVG(wm.Rating), 0) AS AvgRating  -- Ensure no NULL values
            FROM 
                Movies m
            LEFT JOIN 
                MovieStreamingPlatforms mp ON m.MovieID = mp.MovieID
            LEFT JOIN 
                StreamingPlatforms sp ON mp.PlatformID = sp.PlatformID
            LEFT JOIN 
                WatchedMovies wm ON m.MovieID = wm.MovieID
            GROUP BY 
                m.MovieID, m.Title, m.Description, m.Genre, sp.PlatformName, mp.StartDate, mp.EndDate
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()


def add_movie(title, description, genre):
    """Add a movie."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Movies (Title, Description, Genre) VALUES (%s, %s, %s)"
            cursor.execute(query, (title, description, genre))
            connection.commit()
    finally:
        connection.close()

def update_movie(movie_id, title=None, description=None, genre=None):
    """Update a movie's details."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT Title, Description, Genre FROM Movies WHERE MovieID = %s"
            cursor.execute(query, (movie_id,))
            movie = cursor.fetchone()

            # Keep old values for fields not being updated
            title = title if title else movie["Title"]
            description = description if description else movie["Description"]
            genre = genre if genre else movie["Genre"]

            update_query = "UPDATE Movies SET Title = %s, Description = %s, Genre = %s WHERE MovieID = %s"
            cursor.execute(update_query, (title, description, genre, movie_id))
            connection.commit()
    finally:
        connection.close()

'''def delete_movie(movie_id):
    """Delete a movie."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Movies WHERE MovieID = %s"
            cursor.execute(query, (movie_id,))
            connection.commit()
    finally:
        connection.close()'''

def delete_movie(movie_id):
    """Delete a movie and its related records."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Delete related records in MovieStreamingPlatforms
            delete_related_query = "DELETE FROM MovieStreamingPlatforms WHERE MovieID = %s"
            cursor.execute(delete_related_query, (movie_id,))

            # Delete the movie from Movies table
            delete_movie_query = "DELETE FROM Movies WHERE MovieID = %s"
            cursor.execute(delete_movie_query, (movie_id,))

            connection.commit()
    finally:
        connection.close()

def assign_movie_to_platform(movie_id, platform_id, start_date, end_date):
    """Assign a movie to a streaming platform with start and end dates."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO MovieStreamingPlatforms (MovieID, PlatformID, StartDate, EndDate)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (movie_id, platform_id, start_date, end_date))
            connection.commit()
    finally:
        connection.close()


def add_rating_and_comment(user_id, movie_id, rating, comment):
    """Add rating and comment."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO WatchedMovies (UserID, MovieID, Rating, Comment)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, movie_id, rating, comment))
            connection.commit()
    finally:
        connection.close()

def fetch_watched_movies(user_id):
    """Fetch movies watched by a user."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT m.Title, wm.Rating, wm.Comment
            FROM WatchedMovies wm
            JOIN Movies m ON wm.MovieID = m.MovieID
            WHERE wm.UserID = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
    finally:
        connection.close()
