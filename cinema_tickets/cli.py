from cinema_tickets.app import app
from cinema_tickets.db import db_session
import click
from datetime import datetime, date as pydate

@app.cli.command()
@click.option('--name', prompt=True, help='Movie name')
@click.option('--cover', help='Path to cover image')
@click.option('--description', default='Description', help='Description')
def add_movie(name, cover, description):
    if cover is not None:
        with open(cover, 'rb') as f:
            contents = f.read()
            cover = bytearray(contents)

    db_session.execute(
        """
        INSERT INTO movies (id, name, cover, description) VALUES (uuid(), %s, %s, %s)
        """,
        (name, cover, description)
    )

    click.echo('Movie added')

@app.cli.command()
@click.option('--name', default='Name', help='Cinema name')
def add_cinema(name):
    db_session.execute(
        """
        INSERT INTO cinemas (id, name) VALUES (uuid(), %s)
        """,
        (name,)
    )

    click.echo('Cinema added')

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
        cinema = db_session.execute('SELECT * FROM cinemas')

        if not cinema:
            raise 'No cinemas'

        cinema = cinema[0].id

    # get first movie if not specified
    if movie is None:
        movie = db_session.execute('SELECT * FROM movies')

        if not movie:
            raise 'Movie not found'

        movie = movie[0].id

    # default date to now
    if date is None:
        date = pydate.today().strftime('%Y-%m-%d')

    if time is None:
        time = datetime.now().strftime('%H:%M') + ':00'

    db_session.execute(
        """
        INSERT INTO sessions (movie_id, date, time, cinema_id, id, hall_capacity, hall_name)
        VALUES (%s, %s, %s, %s, uuid(), %s, %s)
        """,
        (movie, date, time, cinema, hall_cap, hall_name)
    )

    click.echo('Session added')
