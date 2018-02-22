from datetime import datetime, timedelta
from datetime import date as pydate
from cinema_tickets.db import db_session
import math

def get_movies():
    return list(db_session.execute('SELECT * FROM movies'))

def get_cinemas():
    return list(db_session.execute('SELECT * FROM cinemas'))

def get_movie(id):
    result = db_session.execute('SELECT * FROM movies WHERE id = %s', (id,))

    if not result:
        return None

    return result[0]

def get_session(id):
    result = db_session.execute('SELECT * FROM sessions WHERE id = %s', (id,))

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
    conditions = [movie, date.strftime('%Y-%m-%d')]
    table_name = 'sessions'

    if cinema is None:
        cinema_cond = ''
    else:
        table_name = 'sessions_by_cinema'
        cinema_cond = 'AND cinema_id = %s'
        conditions.append(cinema)

    query = """
    SELECT * FROM {}
    WHERE movie_id = %s AND date = %s
    {}
    """.format(table_name, cinema_cond)

    return db_session.execute(query, conditions)

def get_tickets_count(movie_id):
    conditions = (movie_id,)

    query = """
    SELECT sold_count, session_id FROM tickets_counter
    WHERE movie_id = %s
    """

    res = db_session.execute(query, conditions)

    for r in res:
        yield r.session_id, r.sold_count

def get_tickets(session):
    session_data = get_session(session)

    if session_data is None:
        return []

    conditions = (session, session_data.hall_capacity)

    query = """
    SELECT * FROM tickets
    WHERE session_id = %s
    LIMIT %s
    """

    return list(db_session.execute(query, conditions))

def buy_ticket(session, user, id, timestamp):
    session_data = get_session(session)

    if session_data is None:
        return False

    # i mamy first write wins
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
        UPDATE tickets_counter SET sold_count = sold_count + 1 WHERE movie_id = %s AND session_id = %s
        """,
        (session_data.movie_id, session)
    )

    return True
