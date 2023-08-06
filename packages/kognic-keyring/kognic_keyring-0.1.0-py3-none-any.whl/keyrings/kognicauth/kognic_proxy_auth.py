from urllib.parse import urlparse
from keyrings.gauth import GooglePythonAuth


class KognicPythonAuth(GooglePythonAuth):
    priority = 9

    """
    Piggy back on Google Cloud Auth
    Higher priority than typical recommended backends - but one less priority than Chainer Backend.
    """

    def get_password(self, service, username):
        url = urlparse(service)
        if url.hostname is None or not url.hostname.endswith("pip-vproxy.annotell.com"):
            return
        return super().get_password("https://dummy.pkg.dev", username)
