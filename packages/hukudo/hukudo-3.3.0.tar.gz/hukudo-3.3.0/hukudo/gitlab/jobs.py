from datetime import datetime, timedelta


class JobDurationParseError(ValueError):
    pass


def get_duration(attributes) -> timedelta:
    try:
        started_at = datetime.fromisoformat(attributes['started_at'])
        finished_at = datetime.fromisoformat(attributes['finished_at'])
        return finished_at - started_at
    except (KeyError, ValueError, TypeError):
        raise JobDurationParseError('could not parse')
