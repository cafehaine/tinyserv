"""
Define the Config class, holding all the options for tinyserv.
"""
import os.path


class Config:
    """A place to store all tinyserv options."""

    def __init__(self, **kwargs):
        self.open_browser: bool = kwargs['open_browser']
        self.base_port: int = kwargs['base_port']
        self.allow_uploads: bool = kwargs['allow_uploads']
        self.all_files: bool = kwargs['all_files']
        self.serve_index: bool = kwargs['serve_index']
        self.show_qr: bool = kwargs['qr_code']
        self.path: str = os.path.abspath(kwargs['path'])
