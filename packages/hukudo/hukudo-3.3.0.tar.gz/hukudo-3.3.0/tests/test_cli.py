from click.testing import CliRunner

import hukudo.cli


def test_logs_to_stderr():
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(hukudo.cli.root, ['version'], env={'LOGLEVEL': 'debug'})
    assert hukudo.__version__ in result.stdout
    assert 'logging configured' in result.stderr
