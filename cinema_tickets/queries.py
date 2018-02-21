from datetime import datetime, timedelta
from datetime import date as pydate
from cinema_tickets.db import db_session
import math

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
    SELECT sold_count FROM tickets_counter
    WHERE session_id = %s
    """

    res = db_session.execute(query, conditions)
    for r in res:
        return r.sold_count

    return 0

def get_tickets(session):
    conditions = [session]

    query = """
    SELECT * FROM tickets
    WHERE session_id = %s
    """

    return list(db_session.execute(query, conditions))

def buy_ticket(session, user, id, timestamp):
    decreasing_timestamp = 2000000000000000 - math.trunc(timestamp * 1000000)
    conditions = [session, id, user, datetime.fromtimestamp(timestamp), decreasing_timestamp]

    query = """
    INSERT INTO tickets (session_id, id, user, timestamp)
    VALUES (%s, %s, %s, %s)
    USING TIMESTAMP %s
    """

    res = db_session.execute(query, conditions, trace=True)
    trace = res.get_query_trace()
    for event in trace.events:
        if event.description.startswith('Parsing'):
            print(event.description)
        
    db_session.execute(
        """
        UPDATE tickets_counter SET sold_count = sold_count + 1 WHERE session_id = %s
        """,
        ([session])
    )
