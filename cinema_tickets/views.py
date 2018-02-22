from cinema_tickets.app import app
from cinema_tickets.db import db_session
from cinema_tickets.queries import *
from flask import render_template, send_file, abort, request, redirect, url_for
from datetime import datetime, timedelta
import math
import time
import io
import uuid

@app.route('/')
def list_movies():
    movies = get_movies()

    return render_template('index.html', movies=movies)

@app.route('/movie/<uuid:id>')
def show_movie(id):
    movie = get_movie(id)
    if not movie:
        abort(404)

    date = request.args.get('date', datetime.now(), lambda x: datetime.strptime(x, '%Y-%m-%d'))
    cinema = request.args.get('cinema', None, uuid.UUID)
    sessions = get_sessions_with_counters(id, cinema, date)

    return render_template('movie.html',
        movie=movie, sessions=sessions, cinemas=get_cinemas(), title='Movie',
        cinema=cinema, date=date, path=request.path
    )

@app.route('/movie/<uuid:id>/cover')
def movie_cover(id):
    movie = get_movie(id)
    if not movie or movie.cover is None:
        abort(404)

    return send_file(io.BytesIO(movie.cover), mimetype='image/jpeg')

@app.route('/session/<uuid:id>')
def show_tickets(id):
    tickets = get_tickets(id)

    return render_template('session.html', tickets=tickets, title='Session')

@app.route('/session/<uuid:session>/buy/<uuid:id>', methods=['POST'])
def buy(session, id):
    user = request.form['user']

    if not user:
        abort(400)

    timestamp = time.time()
    result = buy_ticket(session, user, id, timestamp)

    if not result:
        abort(500)

    return redirect(url_for('.show_tickets', id=session))

@app.route('/session/<uuid:id>/buy')
def show_buy_ticket(id):
    return render_template('buy.html', session=id, id=uuid.uuid1(), title='Buy')
