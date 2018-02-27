from datetime import datetime, timedelta
from datetime import date as pydate
from cinema_tickets.db import db_session
from cinema_tickets.db_statements import *
import math

def get_movies():
    return list(db_session.execute(getMovies))

def get_cinemas():
    return list(db_session.execute(getCinemas))

def get_movie(id):
    result = db_session.execute(getMovie, (id,))

    if not result:
        return None

    return result[0]

def get_session(id):
    result = db_session.execute(getSession, (id,))

    if not result:
        return None

    return result[0]

def get_sessions_with_counters(movie, cinema, date):
    sessions = get_sessions(movie, cinema, date)
    counters = dict(get_tickets_count(movie))

    for session in sessions:
        counter = counters[session.id] if session.id in counters else 0
        yield (session, counter)

def get_sessions(movie, cinema, date):
    if cinema is None:
        conditions = [movie, date.strftime('%Y-%m-%d')]
        query = getSessions
    else:
        conditions = [movie, date.strftime('%Y-%m-%d'), cinema]
        query = getCinemaSessions

    return db_session.execute(query, conditions)

def get_tickets_count(movie_id):
    conditions = (movie_id,)

    res = db_session.execute(getTicketsCount, conditions)

    for r in res:
        yield r.session_id, r.sold_count

def get_tickets(session):
    session_data = get_session(session)

    if session_data is None:
        return []

    conditions = (session, session_data.hall_capacity)

    return list(db_session.execute(getTickets, conditions))

def buy_ticket(session, user, id, timestamp):
    session_data = get_session(session)

    if session_data is None:
        return False

    # i mamy first write wins
    # decreasing_timestamp = 2000000000000000 - math.trunc(timestamp * 1000000)
    # conditions = [session, id, user, datetime.fromtimestamp(timestamp), decreasing_timestamp]
    conditions = [session, id, user, datetime.fromtimestamp(timestamp)]

    res = db_session.execute(buyTicket, conditions, trace=True)
    trace = res.get_query_trace()
    for event in trace.events:
        if event.description.startswith('Parsing'):
            print(event.description)

    db_session.execute(updateTicketCounter, (session_data.movie_id, session))

    return True
