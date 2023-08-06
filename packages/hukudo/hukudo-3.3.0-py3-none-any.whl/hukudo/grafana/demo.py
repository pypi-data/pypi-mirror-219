from hukudo.grafana import Grafana

URL = 'https://grafana.dev.0-main.de'
USERNAME = 'admin'
PASSWORD = 'test'


def api_key(name):
    grafana = Grafana.from_basic_auth(URL, USERNAME, PASSWORD)
    return grafana.provision_api_key(name=name, role=Grafana.ADMIN)
