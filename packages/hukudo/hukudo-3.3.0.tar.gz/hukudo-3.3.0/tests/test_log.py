import logging

from hukudo.log import configure_structlog_dev


def test_configure_structlog_dev():
    configure_structlog_dev(logging.DEBUG)
