from http.server import BaseHTTPRequestHandler
from typing import Optional

from tinyserv.config import Config

from jinja2 import Environment, PackageLoader, select_autoescape, Template


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    configuration: Optional[Config] = None
    template_404: Optional[Template] = None
    template_listing: Optional[Template] = None

    @classmethod
    def initialize(cls, configuration: Config) -> None:
        cls.configuration = configuration
        env = Environment(
                loader=PackageLoader('tinyserv', 'templates'),
                autoescape=select_autoescape('html',),
                )
        cls.template_404 = env.get_template('404.html')
        cls.template_listing = env.get_template('listing.html')

    @classmethod
    def check_initialized(cls) -> None:
        if cls.configuration is None or cls.template_404 is None or cls.template_listing is None:
            raise RuntimeError(
                "Tried to handle HTTP request before initializing CustomHTTPRequestHandler."
            )

    def do_HEAD(self) -> None:
        self.check_initialized()
        print("HEAD", self.path)

    def do_GET(self) -> None:
        self.check_initialized()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(self.template_404.render(path=self.path).encode("utf-8"))

    def do_POST(self) -> None:
        self.check_initialized()
        print("POST", self.path)
