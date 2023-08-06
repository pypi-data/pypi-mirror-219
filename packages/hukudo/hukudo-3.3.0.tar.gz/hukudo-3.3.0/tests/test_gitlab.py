from datetime import timedelta

import pytest

from hukudo.gitlab.jobs import get_duration, JobDurationParseError


def test_job_with_duration_happy():
    assert get_duration(
        {
            'started_at': '2022-07-19T16:13:17.374+02:00',
            'finished_at': '2022-07-19T16:14:19.374+02:00',
        }
    ) == timedelta(seconds=62)


def test_job_with_duration_error():
    with pytest.raises(JobDurationParseError):
        get_duration(
            {
                'started_at': 'not-an-iso-datetime-string',
                'finished_at': 'not-an-iso-datetime-string',
            }
        )
