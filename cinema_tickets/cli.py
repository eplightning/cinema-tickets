from cinema_tickets.app import app
from cinema_tickets.db import db_session
from cinema_tickets.db_statements import *
from cinema_tickets.queries import buy_ticket, get_session, get_tickets
import click
from datetime import datetime, date as pydate
import math
import time
import io
import uuid
import random
import string
from multiprocessing import Process, Pipe, set_start_method
from multiprocessing.connection import wait
from timeit import default_timer as timer

@app.cli.command()
@click.option('--name', prompt=True, help='Movie name')
@click.option('--cover', help='Path to cover image')
@click.option('--description', default='Description', help='Description')
def add_movie(name, cover, description):
    if cover is not None:
        with open(cover, 'rb') as f:
            contents = f.read()
            cover = bytearray(contents)

    db_session.execute(addMovie, (name, cover, description))

    click.echo('Movie added')

@app.cli.command()
@click.option('--name', default='Name', help='Cinema name')
def add_cinema(name):
    db_session.execute(addCinema, (name,))

    click.echo('Cinema added')

def stress_process(session, times, user, pipe):
    with app.app_context():
        for i in range(0, times):
            pipe.send('Kupowanie biletu {}'.format(i))
            timestamp = time.time()
            buy_ticket(session, user, uuid.uuid1(), timestamp)

        pipe.close()

@app.cli.command()
@click.option('--session', help='Session UUID', prompt=True)
@click.option('--proc', help='Process count', prompt=True, type=int)
@click.option('--times', prompt=True, help='Queries per process', type=int)
@click.option('--user', help='User')
def stress_test(session, proc, times, user):
    set_start_method('spawn')
    session = uuid.UUID(session)
    session_data = get_session(session)

    click.echo('Session with limit {}'.format(session_data.hall_capacity))

    if user == '' or user is None:
        user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    click.echo('User: {}'.format(user))

    pipes = []
    processes = []

    click.echo('Starting processes')

    for i in range(0, proc):
        pipe_read, pipe_write = Pipe(duplex=False)
        process = Process(target=stress_process, args=(session, times, user, pipe_write))
        pipes.append(pipe_read)
        processes.append(process)
        process.start()
        pipe_write.close()

    click.echo('Reading output')

    start = timer()

    while len(pipes) > 0:
        for ready in wait(pipes):
            try:
                msg = ready.recv()
                click.echo(msg)
            except EOFError:
                pipes.remove(ready)

    click.echo('Joining...')

    for p in processes:
        p.join()

    end = timer() - start

    click.echo('Time taken {}'.format(end))
    click.echo('Speed overall {} rows/sec'.format(proc * times / end))

    if click.confirm('Calculate errors?'):
        tickets = get_tickets(session)
        our_tickets = list(filter(lambda x: x.user == user, tickets))
        expected = proc * times
        found = len(our_tickets)

        click.echo('Expected {} * {} = {}'.format(proc, times, expected))
        click.echo('Found {}'.format(found))
        click.echo('Missing {}'.format(expected - found))
        click.echo('Speed correct {} rows/sec'.format(found / end))

@app.cli.command()
@click.option('--movie', help='Movie UUID')
@click.option('--date', help='Session date')
@click.option('--time', help='Session time')
@click.option('--cinema', help='Cinema UUID')
@click.option('--hall-name', help='Hall name', default='Sala')
@click.option('--hall-cap', help='Hall capacity', default=100)
def add_session(movie, date, time, cinema, hall_name, hall_cap):
    # get first cinema if not specified
    if cinema is None:
        cinema = db_session.execute(getCinemas)

        if not cinema:
            raise 'No cinemas'

        cinema = cinema[0].id
    else:
        cinema = uuid.UUID(cinema)

    # get first movie if not specified
    if movie is None:
        movie = db_session.execute(getMovies)

        if not movie:
            raise 'Movie not found'

        movie = movie[0].id
    else:
        movie = uuid.UUID(movie)

    # default date to now
    if date is None:
        date = pydate.today().strftime('%Y-%m-%d')

    if time is None:
        time = datetime.now().strftime('%H:%M') + ':00'

    sess_uuid = uuid.uuid4()

    db_session.execute(addSession, (movie, date, time, cinema, sess_uuid, hall_cap, hall_name))
    db_session.execute(addCinemaSession, (movie, date, time, cinema, sess_uuid, hall_cap, hall_name))

    click.echo('Session added {}'.format(sess_uuid))
