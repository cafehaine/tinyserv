from http.server import BaseHTTPRequestHandler
from mimetypes import guess_type
import os.path
from typing import Optional

from jinja2 import Environment, PackageLoader, select_autoescape, Template

from tinyserv.config import Config
from tinyserv.entry import Entry


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    configuration: Optional[Config] = None
    template_404: Optional[Template] = None
    template_listing: Optional[Template] = None

    def _real_path(self) -> str:
        """
        Return the real path for the request.

        Removes the leading /.

        Adds a trailing / to directories (except for root dir).

        If serve_index is enabled, return the path for index.html/index.htm if
        it exists.

        Returns None if the target doesn't exist.
        """
        target = self.path.lstrip("/")
        abspath = os.path.abspath(os.path.join(self.configuration.path, target))
        if not os.path.exists(abspath):
            return None
        if os.path.isdir(abspath):
            if self.configuration.serve_index:
                if os.path.exists(os.path.join(abspath, "index.html")):
                    return os.path.join(target, "index.html")
                if os.path.exists(os.path.join(abspath, "index.htm")):
                    return os.path.join(target, "index.htm")
            return target + "/" if target else target
        return target

    @classmethod
    def initialize(cls, configuration: Config) -> None:
        cls.configuration = configuration
        env = Environment(
            loader=PackageLoader('tinyserv', 'templates'),
            autoescape=select_autoescape(
                'html',
            ),
        )
        cls.template_404 = env.get_template('404.html')
        cls.template_listing = env.get_template('listing.html')

    @classmethod
    def check_initialized(cls) -> None:
        if (
            cls.configuration is None
            or cls.template_404 is None
            or cls.template_listing is None
        ):
            raise RuntimeError(
                "Tried to handle HTTP request before initializing CustomHTTPRequestHandler."
            )

    def _send_get_headers(self) -> None:
        """Return the headers for the given path."""
        real_path = self._real_path()
        if real_path is None:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            return

        self.send_response(200)
        if real_path.endswith("/") or not real_path:
            self.send_header('Content-Type', 'text/html')
        else:
            mimetype, encoding = guess_type(real_path)
            if mimetype is not None:
                self.send_header('Content-Type', mimetype)
            if encoding is not None:
                self.send_header('Content-Encoding', encoding)
        self.end_headers()

    def do_HEAD(self) -> None:
        self.check_initialized()
        self._send_get_headers()

    def do_GET(self) -> None:
        self.check_initialized()
        self._send_get_headers()
        real_path = self._real_path()

        # 404
        if real_path is None:
            self.wfile.write(self.template_404.render(path=self.path).encode("utf-8"))
        # Real file
        elif not (real_path.endswith("/") or not real_path):
            with open(real_path, 'rb') as data:
                while True:
                    block = data.read(1024)
                    if not block:
                        break
                    self.wfile.write(block)
        # Directory listing
        else:
            entries = Entry.generate_listing(
                self.configuration.path, real_path, self.configuration.all_files
            )
            self.wfile.write(
                self.template_listing.render(
                    path=self.path,
                    entries=entries,
                    allow_uploads=self.configuration.allow_uploads,
                ).encode("utf-8")
            )

    def do_POST(self) -> None:
        self.check_initialized()
        print("POST", self.path)

    def log_request(self, *args, **kwargs) -> None:
        self.check_initialized()
        if self.configuration.verbose:
            super().log_request(*args, **kwargs)
