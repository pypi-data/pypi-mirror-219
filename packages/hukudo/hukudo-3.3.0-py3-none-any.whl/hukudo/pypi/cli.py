import click
import structlog

logger = structlog.get_logger()


@click.group()
def pypi():
    pass


@pypi.command()
def names():
    from . import names

    print('\n'.join(names()))
