import logging
from dependencyhealth import AbstractClient


class Client(AbstractClient):
    def __init__(self, token: str = None, log_level=logging.WARNING):
        super().__init__(token=token, log_level=log_level)
        self._system = "npm"
