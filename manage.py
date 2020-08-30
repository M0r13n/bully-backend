import random
import random
import string

import click
from flask.cli import FlaskGroup

from app.app import create_app
from app.extensions import db
from app.models.user import User


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Main entry point"""
    pass


@cli.command()
def create_db():
    """ Drops all existing tables and creates them afterwards """
    click.echo("Dropping tables...")
    db.drop_all()
    click.echo("Creating tables...")
    db.create_all()
    click.echo("Activate Extensions...")
    db.session.commit()
    click.echo("DB created successfully!")


@cli.command("init")
def init():
    db.create_all()
    click.echo("Create default user")
    pw = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    user = User(username="Admin", password=pw)
    db.session.add(user)
    db.session.commit()
    click.echo("Successfully created default user with pw: %s" % pw)


if __name__ == "__main__":
    cli()
