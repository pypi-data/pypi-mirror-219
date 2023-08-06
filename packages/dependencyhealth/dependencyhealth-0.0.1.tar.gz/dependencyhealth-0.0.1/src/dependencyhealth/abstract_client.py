import logging
import requests


class AbstractClient:
    def __init__(self, token: str = None, log_level=logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self._session = requests.session()
        self._base = f"https://api.dependency.health/v1"
        self._token = token
        self._session.headers["Authorization"] = f"Bearer {self._token}"
        self._system = None  # Should be defined on a subclass level

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __del__(self):
        self._session.close()

    def _request(self, method, path, params=None):
        self.logger.debug(f"{method} request {self._base + path}")

        if params is None:
            params = dict()

        if method == "GET":
            return self._session.get(self._base + path, params=params)
        else:
            raise NotImplementedError

    def check_package(self, package: str):
        self.logger.debug(f"Getting info for package {package}")
        path = f"/systems/{self._system}/packages/{package}"
        r = self._request("GET", path)

        self.logger.debug(f"Got code {r.status_code}")
        if r.status_code == 200:
            return r.json()
