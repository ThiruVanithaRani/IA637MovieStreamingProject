import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_utils import fetch_users, get_connection, get_user, register_user, fetch_movies, add_movie, update_movie, delete_movie, assign_movie_to_platform, add_rating_and_comment, fetch_watched_movies
from datetime import timedelta
from db_utils import add_rating_and_comment, fetch_movies, assign_movie_to_platform, add_movie, \
    update_movie, delete_movie, fetch_watched_movies, fetch_movies, register_user, get_user, get_connection
import hashlib
from flask_session import Session
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "e5bff5a6e28747a67d8df8c678f5e6f3e7a9b123456789ab"

# === ROUTES === #

@app.route('/')
def home():
    return redirect(url_for('login'))

def hash_password(password):
    salt = 'xyz'  # Add a salt to the password for better security
    return hashlib.md5((password + salt).encode('utf-8')).hexdigest()
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        user = get_user(username, password)
        
        if user:
            session['user_id'] = user['UserID']
            session['user_type'] = user['UserType']
            session['username'] = user['UserName']

            if user['UserType'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = hash_password(password)

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        register_user(username, password)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('user_type') != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            title = request.form['title']
            description = request.form['description']
            genre = request.form['genre']
            add_movie(title, description, genre)
            flash('Movie added successfully!', 'success')
        elif action == 'delete':
            movie_id = request.form['movie_id']
            delete_movie(movie_id)
            flash('Movie deleted successfully!', 'success')

    movies = fetch_movies()
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM StreamingPlatforms")
        platforms = cursor.fetchall()
        users, total_users = fetch_users()

    return render_template('admin_dashboard.html', movies=movies, platforms=platforms, users=users,
        total_users=total_users)

@app.route('/admin/movie_platform', methods=['POST'])
def add_movie_platform():
    movie_id = request.form.get('movie_id')
    platform_id = request.form.get('platform_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    assign_movie_to_platform(movie_id, platform_id, start_date, end_date)
    flash('Movie assigned successfully!', 'success')
    #print(f"Assigned movie {movie_id} to platform {platform_id}")  # Debug log
    return redirect('/admin')

@app.route('/admin/update/<int:movie_id>', methods=['GET', 'POST'])
def update_movie_route(movie_id):
    if session.get('user_type') != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        genre = request.form['genre']
        update_movie(movie_id, title, description, genre)
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('update_movie.html', movie_id=movie_id)

@app.route('/admin/platforms', methods=['GET', 'POST'])
def manage_platforms():
    if session.get('role') != 'admin':
        return redirect('/login')

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                action = request.form.get('action')
                platform_name = request.form.get('platform_name')
                platform_id = request.form.get('platform_id')

                if action == 'add' and platform_name:
                    query = "INSERT INTO StreamingPlatforms (PlatformName) VALUES (%s)"
                    cursor.execute(query, (platform_name,))
                elif action == 'delete' and platform_id:
                    query = "DELETE FROM StreamingPlatforms WHERE PlatformID = %s"
                    cursor.execute(query, (platform_id,))
                elif action == 'update' and platform_id and platform_name:
                    query = "UPDATE StreamingPlatforms SET PlatformName = %s WHERE PlatformID = %s"
                    cursor.execute(query, (platform_name, platform_id))
                connection.commit()

            query = "SELECT * FROM StreamingPlatforms"
            cursor.execute(query)
            platforms = cursor.fetchall()
    finally:
        connection.close()

    return render_template('platforms.html', platforms=platforms)

@app.route('/admin/movie_platform', methods=['POST'])
def assign_movie_platform():
    """Assign a movie to a streaming platform."""
    
    movie_id = request.form.get('movie_id')
    platform_id = request.form.get('platform_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not (movie_id and platform_id and start_date and end_date):
        flash("All fields are required.", "danger")
        return redirect('/admin')

    try:
        assign_movie_to_platform(movie_id, platform_id, start_date, end_date)
        flash("Successfully assigned the movie to the platform.", "success")
    except Exception as e:
        flash(f"Error assigning movie: {e}", "danger")
    return redirect('/admin')


@app.route('/user', methods=['GET'])
def user_dashboard():
    if session.get('user_type') != 'user':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    movies = fetch_movies()
    return render_template('user_dashboard.html', movies=movies)

@app.route('/user/rate/<int:movie_id>', methods=['GET', 'POST'])
def rate_movie(movie_id):
    if session.get('user_type') != 'user':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        add_rating_and_comment(session['user_id'], movie_id, rating, comment)
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('user_dashboard'))

    if request.method == 'GET':
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT Title FROM Movies WHERE MovieID = %s"
                cursor.execute(query, (movie_id,))
                movie = cursor.fetchone()

                comments_query = """
                SELECT w.Comment, u.UserName, w.Timestamp
                FROM WatchedMovies w
                JOIN Users u ON w.UserID = u.UserID
                WHERE w.MovieID = %s
                """
                cursor.execute(comments_query, (movie_id,))
                comments = cursor.fetchall()
        finally:
            connection.close()

        return render_template('rate_movie.html', movie_id=movie_id, movie=movie, comments=comments)
    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']

        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO WatchedMovies (UserID, MovieID, Rating, Comment, Timestamp)
                VALUES (%s, %s, %s, %s, NOW())
                """
                cursor.execute(query, (user_id, movie_id, rating, comment)) # type: ignore
                connection.commit()
        finally:
            connection.close()

        return redirect(f'/user/movie/{movie_id}')

@app.route('/user/watched', methods=['GET'])
def watched_movies():
    if session.get('user_type') != 'user':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    movies = fetch_watched_movies(session['user_id'])
    return render_template('watched_movies.html', movies=movies)

@app.route('/user/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    if session.get('role') != 'user':
        return redirect('/login')

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch movie details
            movie_query = "SELECT * FROM Movies WHERE MovieID = %s"
            cursor.execute(movie_query, (movie_id,))
            movie = cursor.fetchone()

            # Fetch comments with usernames
            comments_query = """
            SELECT wm.Comment, u.Username, wm.Timestamp
            FROM WatchedMovies wm
            JOIN Users u ON wm.UserID = u.UserID
            WHERE wm.MovieID = %s
            """
            cursor.execute(comments_query, (movie_id,))
            comments = cursor.fetchall()
    finally:
        connection.close()

    return render_template('movie_details.html', movie=movie, comments=comments)

@app.route('/user/trending', methods=['GET'])
def trending_movies():
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT m.Title, COUNT(w.MovieID) AS CommentCount
            FROM Movies m
            JOIN WatchedMovies w ON m.MovieID = w.MovieID
            WHERE w.Timestamp >= NOW() - INTERVAL 7 DAY
            GROUP BY m.MovieID
            ORDER BY CommentCount DESC
            LIMIT 5
            """
            cursor.execute(query)
            trending = cursor.fetchall()
    finally:
        connection.close()

    return render_template('trending.html', movies=trending)

if __name__ == "__main__":
    app.run(debug=True)
