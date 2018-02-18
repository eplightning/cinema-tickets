from datetime import datetime, timedelta
from datetime import date as pydate
from cinema_tickets.db import db_session

def get_movies():
    return db_session.execute('SELECT * FROM movies')

def get_cinemas():
    return db_session.execute('SELECT * FROM cinemas')

def get_movie(id):
    result = db_session.execute('SELECT * FROM movies WHERE id = %s', (id,))

    if not result:
        return None

    return result[0]

def get_sessions(movie, cinema, date):
    conditions = [movie, date.strftime('%Y-%m-%d')]

    if cinema is None:
        cinema_cond = ''
    else:
        cinema_cond = 'AND cinema_id = %s'
        conditions.append(cinema)

    query = """
    SELECT * FROM sessions
    WHERE movie_id = %s AND date = %s
    {}
    """.format(cinema_cond)

    return sorted(db_session.execute(query, conditions), key=lambda x: x.time)

def get_tickets_count(session):
    conditions = [session]

    query = """
    SELECT COUNT(*) as count FROM tickets
    WHERE session_id = %s
    """

    return list(db_session.execute(query, conditions))[0].count

def get_tickets(session):
    conditions = [session]

    query = """
    SELECT * FROM tickets
    WHERE session_id = %s
    """

    return list(db_session.execute(query, conditions))

def buy_ticket(session, user):
    conditions = [session, user]

    query = """
    INSERT INTO tickets (session_id, timestamp, user)
    VALUES (%s, toTimestamp(now()), %s);
    """

    return list(db_session.execute(query, conditions))