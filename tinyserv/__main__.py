"""
A tiny http server to transfer files between computers.
"""
from argparse import ArgumentParser, Namespace
from http.server import ThreadingHTTPServer
from json import loads
from subprocess import run
from typing import List
from webbrowser import open as webopen

from tinyserv.handler import CustomHTTPRequestHandler
from tinyserv.config import Config
from tinyserv.qr import show_qrs


def list_ips() -> List[str]:
    """
    Return a list of valid IP addresses for this computer.

    Uses the ip -j command, might not be available everywhere.
    """
    ip_show = run(["ip", "-j", "addr", "show"], capture_output=True)
    devices = loads(ip_show.stdout)

    output = []

    for device in devices:
        if device['operstate'] == 'DOWN':
            continue
        for address in device['addr_info']:
            host = address['scope'] == 'host'
            if host:
                continue
            v6 = address['family'] == 'inet6'
            addr = address['local']
            if v6:
                addr = f"[{addr}]"
                continue  # At the moment, Python's TCP server only supports ipv4
            output.append(addr)

    return output


def run_server(config: Config) -> None:
    CustomHTTPRequestHandler.initialize(config)
    server = ThreadingHTTPServer(("", config.base_port), CustomHTTPRequestHandler)
    try:
        ips = list_ips()
        urls = [f"http://{ip}:{config.base_port}" for ip in ips]
        if not ips:
            print(
                "Couldn't find any ip for this device, are you connected to the network?"
            )
        else:
            print("Connect to:")
            if config.open_browser:
                webopen(urls[0])
        for url in urls:
            print(f"- {url}")
        if config.show_qr:
            show_qrs(urls)
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Goodbye!")


def main() -> None:
    parser = ArgumentParser(
        description="A tiny http server to transfer files between computers."
    )
    parser.add_argument(
        "--open-browser",
        "-b",
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
        "--qr-code",
        "-Q",
        action='store_true',
        help="Show qr codes with the urls to connect to the server.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action='store_true',
        help="Show entering connections.",
    )
    parser.add_argument(
        "path", type=str, nargs="?", default=".", help="The directory to serve."
    )

    arguments = parser.parse_args()

    config = Config(**vars(arguments))

    run_server(config)


if __name__ == "__main__":
    main()
