from cinema_tickets.app import app
from cinema_tickets.db import db_session
from flask import render_template, send_file, abort
import io

@app.route('/')
def list_movies():
    movies = list(db_session.execute('SELECT * FROM movies'))

    return render_template('index.html', movies=movies)

@app.route('/movie/<uuid:id>')
def show_movie(id):
    movie = db_session.execute('SELECT * FROM movies WHERE id = %s', (id,))
    if not movie:
        abort(404)

    return render_template('movie.html', movie=movie[0])

@app.route('/movie/<uuid:id>/cover')
def movie_cover(id):
    movie = db_session.execute('SELECT * FROM movies WHERE id = %s', (id,))
    if not movie or movie[0].cover is None:
        abort(404)

    return send_file(io.BytesIO(movie[0].cover), mimetype='image/jpeg')
