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
    tickets_count = get_tickets_count
    if not movie:
        abort(404)

    date = request.args.get('date', datetime.now(), lambda x: datetime.strptime(x, '%Y-%m-%d'))
    cinema = request.args.get('cinema', None, uuid.UUID)
    sessions = get_sessions(id, cinema, date)

    sessions_list = []
    for session in sessions:
        sessions_list.append([session, get_tickets_count(session.id)])
        
    print(list(sessions_list))

    return render_template('movie.html', movie=movie, sessions=sessions_list, title='Movie')

@app.route('/movie/<uuid:id>/cover')
def movie_cover(id):
    movie = get_movie(id)
    if not movie or movie.cover is None:
        abort(404)

    return send_file(io.BytesIO(movie.cover), mimetype='image/jpeg')

@app.route('/session/<uuid:id>')
def show_tickets(id):
    tickets = get_tickets(id)
    print(list(tickets))

    return render_template('session.html', tickets=tickets, title='Session')

@app.route('/session/<uuid:id>/buy/<string:user>')
def buy(id, user):
    buy_ticket(id, user)

    return show_tickets(id)

@app.route('/session/<uuid:id>/buy')
def show_buy_ticket(id):

    return render_template('buy.html', session=id, title='Buy')
