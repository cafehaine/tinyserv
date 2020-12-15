from http.server import BaseHTTPRequestHandler
from typing import Optional

from tinyserv.config import Config


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    configuration: Optional[Config] = None

    @classmethod
    def initialize(cls, configuration: Config) -> None:
        cls.configuration = configuration

    @classmethod
    def check_initialized(cls) -> None:
        if cls.configuration is None:
            raise RuntimeError(
                "Tried to handle HTTP request before initializing CustomHTTPRequestHandler."
            )

    def do_HEAD(self) -> None:
        self.check_initialized()
        print("HEAD")

    def do_GET(self) -> None:
        self.check_initialized()
        print("GET")

    def do_POST(self) -> None:
        self.check_initialized()
        print("POST")
