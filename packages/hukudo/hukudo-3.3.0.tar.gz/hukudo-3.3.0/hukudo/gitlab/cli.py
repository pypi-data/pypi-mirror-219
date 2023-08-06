import json

import click
import structlog

from hukudo.gitlab.api import Gitlab
from hukudo.gitlab.jobs import get_duration, JobDurationParseError

logger = structlog.get_logger()


@click.group()
@click.option('--name')
@click.pass_context
def gitlab(ctx, name):
    ctx.obj = Gitlab.from_ini(name)
    log = logger.bind(instance=ctx.obj)
    log.debug('instantiated')


@gitlab.command()
@click.argument('project')
@click.pass_context
def jobs(ctx, project):
    gitlab: Gitlab = ctx.obj
    for job in gitlab.jobs_of_project(project):
        try:
            job.attributes['duration'] = get_duration(job.attributes)
            print(json.dumps(job.attributes))
        except JobDurationParseError:
            pass
