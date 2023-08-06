import os
from pathlib import Path
from random import choices
from string import ascii_uppercase, digits

import httpx
import pytest
from click.testing import CliRunner

import hukudo.cli
from hukudo.grafana import Grafana, demo
from hukudo.grafana.errors import DashboardWriteError
from hukudo.grafana.models import JSONThing


@pytest.fixture(scope='session')
def random_string(k=6):
    return str.join('', choices(ascii_uppercase + digits, k=k))


@pytest.fixture(scope='session')
def api_key(random_string):
    return demo.api_key(f'test-{random_string}')


@pytest.fixture(scope='session')
def demo_env(api_key):
    return {
        'GRAFANA_URL': demo.URL,
        'GRAFANA_API_KEY': api_key,
        'GRAFANA_CLIENT_ROOT_CA': str(Path('~/ingress/root.crt').expanduser()),
    }


@pytest.fixture()
def demo_envfile(demo_env, tmp_path):
    config_file = tmp_path / 'config'
    with config_file.open('w') as f:
        for k, v in demo_env.items():
            f.write(f'{k}={v}\n')
    return config_file


@pytest.fixture(scope='session')
def grafana(demo_env, example_dashboard_json):
    return Grafana.from_api_key(
        demo_env['GRAFANA_URL'],
        demo_env['GRAFANA_API_KEY'],
        verify=demo_env['GRAFANA_CLIENT_ROOT_CA'],
    )


@pytest.fixture(autouse=True)
def auto_mock_patch_os_environ(mocker):
    """
    CLI calls may change os.environ, e.g. dotenv.load_dotenv().
    Mock os.environ using the current environment and restore afterwards.
    https://docs.python.org/3/library/unittest.mock.html#patch-dict
    """
    mocker.patch.dict('os.environ', os.environ)


@pytest.fixture(scope='session')
def example_dashboard_json():
    return {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "target": {"limit": 100, "matchAny": False, "tags": [], "type": "dashboard"},
                    "type": "dashboard",
                }
            ]
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "links": [],
        "liveNow": False,
        "panels": [
            {
                "datasource": {"type": "datasource", "uid": "grafana"},
                "gridPos": {"h": 9, "w": 12, "x": 0, "y": 0},
                "id": 2,
                "options": {"content": "# Hello World!", "mode": "markdown"},
                "pluginVersion": "8.5.0",
                "title": "Test Panel",
                "type": "text",
            }
        ],
        "schemaVersion": 36,
        "style": "dark",
        "tags": [],
        "templating": {"list": []},
        "time": {"from": "now-6h", "to": "now"},
        "timepicker": {},
        "timezone": "",
        "title": "test",
        "uid": "test-uid",
        "version": 0,
        "weekStart": "",
    }


def test_json_thing():
    x = JSONThing({'foo': 'bar', 'baz': 123, 'qux': 'quux'})
    assert repr(x) == "{'foo': 'bar', 'baz': 123, 'qu"


def test_client_cert():
    from dotenv import dotenv_values

    env = dotenv_values()
    grafana = Grafana(
        httpx.Client(
            base_url=env['GRAFANA_URL'],
            headers=Grafana.bearer_header(env['GRAFANA_API_KEY']),
            verify=env['GRAFANA_CLIENT_ROOT_CA'],
            cert=(
                env['GRAFANA_CLIENT_CRT'],
                env['GRAFANA_CLIENT_KEY'],
            ),
        )
    )
    assert grafana.health()
    dashboards = grafana.dashboards()
    assert len(dashboards) > 10


def test_api_key(api_key):
    assert len(api_key) >= 80


def test_api_key_role_invalid():
    client = httpx.Client()
    with pytest.raises(ValueError):
        Grafana(client).provision_api_key('_', 'ThisIsInvalid')


def test_post_dashboard(grafana, example_dashboard_json):
    grafana.post_dashboard(example_dashboard_json)


def test_post_dashboard_error(grafana):
    with pytest.raises(DashboardWriteError):
        grafana.post_dashboard({'uid': 'foo'})


def run(env, args):
    runner = CliRunner()
    # noinspection PyTypeChecker
    result = runner.invoke(hukudo.cli.root, args, env=env, catch_exceptions=False)
    return result


def test_cli_health(demo_env):
    run(demo_env, ['grafana', 'health'])


def test_cli_dashboard_list(demo_env):
    result = run(demo_env, ['grafana', 'dashboard', 'list'])
    assert 'https://grafana.dev.0-main.de/d/test-uid' in result.output


def test_cli_dashboard_export_import(demo_env, tmp_path):
    run(demo_env, ['grafana', 'dashboard', 'export', str(tmp_path)])
    files = list(tmp_path.glob('*.json'))
    assert len(files) == 1
    # formatted json is indented on line 2
    contents = files[0].read_text()
    line_2 = contents.split('\n')[1]
    assert line_2.startswith('  ')
    for file in files:
        run(demo_env, ['grafana', 'dashboard', 'import', str(file)])


def test_cli_config(demo_envfile):
    run(env={}, args=['grafana', '-c', demo_envfile, 'dashboard', 'list'])


def test_cli_errors_empty_env(mocker, tmp_path):
    mocker.patch.dict('os.environ', {})  # empty os.environ
    os.chdir(tmp_path)  # make sure there is no .env file present
    runner = CliRunner(mix_stderr=False)
    # noinspection PyTypeChecker
    result = runner.invoke(hukudo.cli.root, ['grafana', 'health'], catch_exceptions=False)
    assert "missing environment variable 'GRAFANA_URL'" in result.stderr
