# from __future__ import unicode_literals
import click

import os
import sys
from huhk.case_project.version import version

__version__ = version


import click


@click.command()
@click.option('--count', help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def commen(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    commen()