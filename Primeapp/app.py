from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to avoid a warning

# Initialize SQLAlchemy (note this should be after app configuration)
db = SQLAlchemy(app)

# Create the Movies model
class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    cast = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime)
    release_date = db.Column(db.DateTime)
    rating = db.Column(db.Float)
    duration = db.Column(db.Float)
    listed_in = db.Column(db.Boolean)
    description = db.Column(db.String(120), nullable=False)

# Create all database tables if they don't exist
with app.app_context():
    db.create_all()

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies')
def movies():
    movies_list = Movies.query.all()
    return render_template('movies.html', movies=movies_list)

@app.route('/submit', methods=['POST'])
def submit():
    movie_id = request.form['movie_id']
    type = request.form['type']
    title = request.form['title']
    director = request.form['director']
    cast = request.form['cast']
    country = request.form['country']
    release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d') if request.form['release_date'] else None
    rating = float(request.form['rating']) if request.form['rating'] else None
    duration = float(request.form['duration']) if request.form['duration'] else None
    listed_in = bool(request.form.get('listed_in'))
    description = request.form['description']

    # Create a new movie instance
    new_movie = Movies(movie_id=movie_id, type=type, title=title, director=director,
                       cast=cast, country=country, release_date=release_date, rating=rating,
                       duration=duration, listed_in=listed_in, description=description)

    # Add the movie to the database
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('movies'))

# Route to update movie details
@app.route('/update/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.get_json()
    movie = Movies.query.get(movie_id)

    if movie:
        movie.type = data['type']
        movie.title = data['title']
        movie.director = data['director']
        movie.cast = data['cast']
        movie.country = data['country']
        movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d') if data['release_date'] else None
        movie.rating = data['rating']
        movie.duration = data['duration']
        movie.description = data['description']

        db.session.commit()
        return jsonify({"message": "Movie updated successfully!"}), 200
    else:
        return jsonify({"message": "Movie not found!"}), 404

# Route to delete a movie
@app.route('/delete/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movies.query.get(movie_id)

    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully!"}), 200
    else:
        return jsonify({"message": "Movie not found!"}), 404

# Route to get movies (useful for editing)
@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies_list = Movies.query.all()
    return jsonify([{
        'movie_id': movie.movie_id,
        'type': movie.type,
        'title': movie.title,
        'director': movie.director,
        'cast': movie.cast,
        'country': movie.country,
        'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
        'rating': movie.rating,
        'duration': movie.duration,
        'listed_in': movie.listed_in,
        'description': movie.description
    } for movie in movies_list])

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/subscription')
def subscription():
    return render_template('subscription.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
