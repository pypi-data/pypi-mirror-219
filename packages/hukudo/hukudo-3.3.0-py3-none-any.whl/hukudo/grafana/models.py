import json
from pathlib import Path


class JSONThing:
    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return str(self.raw)[:30]

    @property
    def id(self):
        return self.raw['id']

    @property
    def uid(self):
        return self.raw['uid']

    @property
    def title(self):
        return self.raw['title']


class Dashboard(JSONThing):
    def __init__(self, raw, base_url):
        super().__init__(raw)
        base = str(base_url).rstrip('/')
        self.url = f'{base}/d/{self.uid}'

    def export(self, path):
        path = Path(path)
        path.write_text(json.dumps(self.raw, sort_keys=True, indent=2))
