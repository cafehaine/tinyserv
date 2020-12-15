"""
A tiny http server to transfer files between computers.
"""
from argparse import ArgumentParser, Namespace
from http.server import ThreadingHTTPServer

from tinyserv.handler import CustomHTTPRequestHandler
from tinyserv.config import Config


def run_server(config: Config) -> None:
    CustomHTTPRequestHandler.initialize(config)
    server = ThreadingHTTPServer(("0.0.0.0", 8000), CustomHTTPRequestHandler)
    server.serve_forever()


def main() -> None:
    parser = ArgumentParser(
        description="A tiny http server to transfer files between computers."
    )
    parser.add_argument(
        "--open-browser",
        action='store_true',
        help="Open the default browser once the server started.",
    )
    parser.add_argument(
        "--base-port",
        "-p",
        type=int,
        nargs="?",
        default=8000,
        help="The starting port for the server.",
    )
    parser.add_argument(
        "--listen-address",
        "-l",
        type=str,
        nargs="?",
        default="0.0.0.0",
        help="The listening address for the server.",
    )
    parser.add_argument(
        "--allow-uploads",
        "-u",
        action='store_true',
        help="Add a form at the top of each page allowing to upload files.",
    )
    parser.add_argument(
        "--all-files", "-a", action='store_true', help="Show hidden files."
    )
    parser.add_argument(
        "--serve-index",
        "-i",
        action='store_true',
        help="Try to serve index.htm[l] if present.",
    )
    parser.add_argument(
        "path", type=str, nargs="?", default=".", help="The directory to serve."
    )

    parser.parse_args()

    config = Config()  # TODO

    run_server(config)


if __name__ == "__main__":
    main()
