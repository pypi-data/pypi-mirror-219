import gitlab
from gitlab.v4.objects import ProjectJob


class Gitlab:
    """
    Note the use of `iterator=True` to handle pagination
    https://python-gitlab.readthedocs.io/en/stable/api-usage.html#pagination.
    """

    PAGINATION_ARGS = {'iterator': True, 'per_page': 1000}

    def __init__(self, python_gitlab_instance):
        self.gl: gitlab.Gitlab = python_gitlab_instance

    @classmethod
    def from_ini(cls, name):
        return cls(gitlab.Gitlab.from_config(name))

    def jobs_of_project(self, project_id) -> [ProjectJob]:
        """
        Note that project_id can also be a string like "namespace/project". :)
        """
        p = self.gl.projects.get(project_id)
        return p.jobs.list(**self.PAGINATION_ARGS)
