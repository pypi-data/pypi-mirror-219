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
        if url.hostname is None: 
            return
        is_annotell = url.hostname.endswith("pip-vproxy.annotell.com")
        is_kognic = (url.hostname.endswith("kognic.io") and "pypi" in url.hostname)
        if not (is_annotell or is_kognic):
            return

        return super().get_password("https://dummy.pkg.dev", username)
