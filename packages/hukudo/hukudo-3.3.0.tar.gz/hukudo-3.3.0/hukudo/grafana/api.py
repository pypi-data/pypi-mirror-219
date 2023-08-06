import httpx
import structlog

from .errors import GrafanaError, DashboardWriteError, CertificateError
from .models import Dashboard

logger = structlog.get_logger()


class Grafana:
    VIEWER = 'Viewer'
    EDITOR = 'Editor'
    ADMIN = 'Admin'
    ROLES = [VIEWER, EDITOR, ADMIN]

    @staticmethod
    def bearer_header(api_key):
        return {'Authorization': f'Bearer {api_key}'}

    @classmethod
    def from_basic_auth(cls, url, username, password, verify=None, cert=None):
        client = httpx.Client(
            base_url=url,
            auth=(username, password),
            http2=True,
            verify=verify,
            cert=cert,
        )
        return cls(client)

    @classmethod
    def from_api_key(cls, url, api_key, verify=None, cert=None, auth=None):
        client = httpx.Client(
            base_url=url,
            headers=cls.bearer_header(api_key),
            auth=auth,
            http2=True,
            verify=verify,
            cert=cert,
        )
        return cls(client)

    def __init__(self, client: httpx.Client):
        self.client = client
        self.log = logger.bind(instance=self)

    def __str__(self):
        return str(self.client.base_url)

    def __repr__(self):
        return f'Grafana("{self}")'

    def health(self):
        try:
            r = self.client.get('/api/health')
        except httpx.ConnectError as e:
            if 'unable to get local issuer certificate' in str(e):
                raise CertificateError('Try setting GRAFANA_CLIENT_ROOT_CA.')
            raise
        except httpx.ReadError as e:
            if 'BAD_CERTIFICATE' in str(e):
                raise CertificateError('Try setting GRAFANA_CLIENT_CERT and GRAFANA_CLIENT_KEY')
            raise
        if r.status_code != 200:
            raise GrafanaError('no 200 on /api/health')
        elif r.json()['database'] != 'ok':
            raise GrafanaError('database nok')
        else:
            return True

    def provision_api_key(self, name, role):
        """
        https://grafana.com/docs/grafana/latest/http_api/create-api-tokens-for-org/
        """
        if role not in self.ROLES:
            self.log.debug('invalid role', name=name, role=role)
            raise ValueError('invalid role')
        response = self.client.post('/api/auth/keys', json={'name': name, 'role': role})
        response.raise_for_status()
        return response.json()['key']

    def dashboards(self):
        result = []
        # https://grafana.com/docs/grafana/latest/http_api/folder_dashboard_search/
        r = self.client.get('/api/search?query=&starred=false')
        r.raise_for_status()
        search_results = r.json()
        uids = [sr['uid'] for sr in search_results if sr['type'] == 'dash-db']
        for uid in uids:
            d = self.client.get(f'/api/dashboards/uid/{uid}').json()['dashboard']
            result.append(Dashboard(d, base_url=self.client.base_url))
        return result

    def post_dashboard(self, dashboard_data):
        # force overwrite by setting id = null
        # https://grafana.com/docs/grafana/latest/http_api/dashboard/#create--update-dashboard
        if 'id' in dashboard_data:
            dashboard_data['id'] = None
        uid = dashboard_data['uid']
        log = self.log.bind(uid=uid)
        body = {
            'dashboard': dashboard_data,
            'overwrite': True,
        }
        response = self.client.post('/api/dashboards/db', json=body)
        if response.status_code != 200:
            log.error(response.text, uid=uid)
            raise DashboardWriteError(uid)
        log.debug('create dashboard', uid=uid)
