import json
import os
from pathlib import Path

import click
import dotenv
import structlog

from hukudo.grafana import Grafana
from hukudo.grafana.errors import DashboardWriteError

logger = structlog.get_logger()


@click.group()
@click.option('-c', '--config', type=click.Path())
@click.pass_context
def grafana(ctx, config):
    if config:
        logger.debug('dotenv override', config=config)
        os.environ.update(dotenv.dotenv_values(config))
    # get stuff from env
    try:
        url = os.environ['GRAFANA_URL']
        api_key = os.environ['GRAFANA_API_KEY']
    except KeyError as e:
        raise click.ClickException(f'missing environment variable {e}')
    root_ca = os.environ.get('GRAFANA_CLIENT_ROOT_CA')
    logger.debug('CA', path=root_ca)

    client_cert = None
    try:
        logger.debug('read config', what='client_cert')
        crt = os.environ['GRAFANA_CLIENT_CRT']
        key = os.environ['GRAFANA_CLIENT_KEY']
        logger.debug('client cert', crt=crt, key=key)
        client_cert = (crt, key)
    except KeyError:
        pass

    basic_auth = None
    try:
        logger.debug('read config', what='basic_auth')
        username = os.environ['GRAFANA_BASIC_AUTH_USERNAME']
        password = os.environ['GRAFANA_BASIC_AUTH_PASSWORD']
        logger.debug('basic_auth', username=username)
        basic_auth = (username, password)
    except KeyError:
        pass

    ctx.obj = Grafana.from_api_key(
        url=url,
        api_key=api_key,
        verify=root_ca,
        cert=client_cert,
        auth=basic_auth,
    )
    log = logger.bind(instance=ctx.obj)
    log.debug('instantiated')


@grafana.command()
@click.pass_context
def health(ctx):
    grafana: Grafana = ctx.obj
    if grafana.health():
        logger.info('health OK', instance=grafana)


@grafana.group()
def dashboard():
    pass


@dashboard.command(name='list')
@click.pass_context
def dashboard_list(ctx):
    grafana: Grafana = ctx.obj

    for board in grafana.dashboards():
        print(f'{board.url}\t({board.title})')


@dashboard.command()
@click.argument('target_dir', type=click.Path())
@click.pass_context
def export(ctx, target_dir):
    """
    Exports all dashboards as JSON files to the given directory.
    """
    log = logger.bind(instance=ctx.obj)
    log.info('export')

    grafana: Grafana = ctx.obj
    target = Path(target_dir)

    for board in grafana.dashboards():
        filename = target / f'{board.id}.json'
        board.export(filename)


@dashboard.command(name='import')
@click.argument('paths', type=click.Path(), nargs=-1)
@click.pass_context
def import_(ctx, paths):
    """
    Import dashboards from JSON files.
    """
    grafana: Grafana = ctx.obj

    exit_code = 0
    for path in paths:
        path = Path(path)
        with path.open() as f:
            data = json.load(f)
        try:
            grafana.post_dashboard(data)
        except DashboardWriteError:
            exit_code = 1
    return exit_code
