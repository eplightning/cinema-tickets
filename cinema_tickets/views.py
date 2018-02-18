from cinema_tickets.app import app
from cinema_tickets.db import db_session
from cinema_tickets.queries import *
from flask import render_template, send_file, abort, request
from datetime import datetime, timedelta
import io
import uuid

@app.route('/')
def list_movies():
    movies = list(get_movies())

    return render_template('index.html', movies=movies)

@app.route('/movie/<uuid:id>')
def show_movie(id):
    movie = get_movie(id)
    if not movie:
        abort(404)

    date = request.args.get('date', datetime.now(), lambda x: datetime.strptime(x, '%Y-%m-%d'))
    cinema = request.args.get('cinema', None, uuid.UUID)
    sessions = get_sessions(id, cinema, date)

    print(list(sessions))

    return render_template('movie.html', movie=movie, sessions=sessions)

@app.route('/movie/<uuid:id>/cover')
def movie_cover(id):
    movie = get_movie(id)
    if not movie or movie.cover is None:
        abort(404)

    return send_file(io.BytesIO(movie.cover), mimetype='image/jpeg')

@app.route('/tickets/<uuid:id>')
def show_tickets(id):
    tickets = get_tickets(id)
    print(list(tickets))

    return render_template('session.html', tickets=tickets, title='Session')
