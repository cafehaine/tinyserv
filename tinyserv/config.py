"""
Define the Config class, holding all the options for tinyserv.
"""


class Config:
    """A place to store all tinyserv options."""

    def __init__(self, **kwargs):
        self.open_browser: bool = kwargs['open_browser']
        self.base_port: int = kwargs['base_port']
        self.listen_address: str = kwargs['listen_address']
        self.allow_uploads: bool = kwargs['allow_uploads']
        self.all_files: bool = kwargs['all_files']
        self.serve_index: bool = kwargs['serve_index']
        self.path: str = kwargs['path']
