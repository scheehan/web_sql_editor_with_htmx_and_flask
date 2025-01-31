import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


# Connect to the database specified in the config file
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Close the database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Initialise the database with setup sql schema template - this only needs to be run once
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Create a command that can be run with flask ("flask init-db") to initialise the database
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Initialsed the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
