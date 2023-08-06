import os
import subprocess

import pytest
from click.testing import CliRunner

import hukudo.cli
from hukudo.exc import HukudoException


@pytest.fixture(autouse=True, scope='session')
def auto_requests_cache(session_mocker, tmp_path_factory):
    env = os.environ.copy()
    env['REQUESTS_CACHE_DIR'] = str(tmp_path_factory.mktemp('cache'))
    session_mocker.patch.dict('os.environ', env)


def test_download(tmp_path):
    from hukudo.chromedriver import download_and_symlink, is_matching_my_major

    # download and test-run the executable
    version, driver_path = download_and_symlink(tmp_path)
    output = subprocess.check_output([str(driver_path), '--version'], encoding='utf-8')
    assert 'ChromeDriver' in output
    assert str(version) in output
    # check the symlink
    link = tmp_path / 'chromedriver'
    assert link.absolute().is_file()
    assert is_matching_my_major(driver_path)


def test_lookup():
    from hukudo.chromedriver import ChromedriverRepo

    repo = ChromedriverRepo('linux64')
    versions = repo.versions()
    assert len(versions) > 0
    lv = repo.latest_version(100)
    assert lv.version.startswith('100.')


def test_my_chrome():
    from hukudo.chromedriver import my_chrome_version

    v = my_chrome_version()
    assert v.version
    assert v.major > 90


def run(args):
    runner = CliRunner(mix_stderr=False)
    # noinspection PyTypeChecker
    result = runner.invoke(hukudo.cli.root, args)
    return result


def test_cli(pytester):
    pytester.chdir()

    result = run(['chromedriver', 'download'])
    assert result.exit_code == 0
    path = next(pytester.path.glob('chromedriver-*'))
    assert path.is_file()
    x = path.stat()
    assert x.st_size > 0

    cannot_overwrite = run(['chromedriver', 'download'])
    assert 'Error: file exists' in cannot_overwrite.stderr
    assert cannot_overwrite.exit_code == 1

    can_force_overwrite = run(['chromedriver', 'download', '--force'])
    assert can_force_overwrite.stderr == ''

    skip_symlink = run(['chromedriver', 'download', '--force', '--skip-symlink'])
    assert skip_symlink.stderr == ''

    # must download to a directory
    file_path = pytester.path / 'foo'
    file_path.write_text('hello')
    # noinspection PyTypeChecker
    invalid_directory = run(['chromedriver', 'download', str(file_path)])
    assert 'Error: not a directory' in invalid_directory.stderr
    assert invalid_directory.exit_code == 1


def test_cli_error(mocker):
    # noinspection PyUnusedLocal
    def raiser(*args, **kwargs):
        raise HukudoException('test')

    mocker.patch('hukudo.chromedriver.download_and_symlink', raiser)
    runner = CliRunner(mix_stderr=False)
    # noinspection PyTypeChecker
    result = runner.invoke(hukudo.cli.root, ['chromedriver', 'download'])
    assert result.stderr == 'Error: test\n'
