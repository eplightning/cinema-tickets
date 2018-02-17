from cinema_tickets.app import app
from cinema_tickets.db import db_session
import click

@app.cli.command()
@click.option('--name', default='Name', help='Movie name')
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
