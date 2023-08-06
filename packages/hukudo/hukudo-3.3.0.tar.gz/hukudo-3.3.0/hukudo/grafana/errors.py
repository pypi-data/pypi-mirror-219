class GrafanaError(Exception):
    pass


class CertificateError(GrafanaError):
    pass


class DashboardWriteError(GrafanaError):
    pass
