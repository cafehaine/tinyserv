from datetime import datetime
from typing import List
import os
import os.path
from stat import S_IFDIR


class Entry:
    def __init__(
        self, root: str, path: str, stat: os.stat_result, *, override_name=None
    ):
        if override_name is not None:
            self.name = override_name
        else:
            self.name = os.path.basename(path)
            if stat.st_mode & S_IFDIR:
                self.name += "/"

        self.path = "/" + path
        timestamp = datetime.fromtimestamp(stat.st_mtime)
        self.timestamp = timestamp.isoformat()
        self.human_timestamp = self.timestamp  # TODO prettier format
        self.human_long_timestamp = self.timestamp  # TODO long version of human
        size = stat.st_size
        self.size = size
        self.human_size = size  # TODO prettier format
        self.human_long_size = size  # TODO long version of human

    @classmethod
    def generate_dir_up(cls, root: str, path: str) -> 'Entry':
        if path.endswith("/"):
            path = path[:-1]
        path = os.path.dirname(path)
        stat = os.stat(os.path.join(root, path))
        return cls(root, path, stat, override_name="..")

    @classmethod
    def generate_listing(cls, root: str, path: str, show_hidden: bool) -> List['Entry']:
        output = []
        if path != "":
            output.append(cls.generate_dir_up(root, path))
        for dir_entry in os.scandir(os.path.join(root, path)):
            if not show_hidden and dir_entry.name.startswith("."):
                continue
            output.append(
                cls(root, os.path.join(path, dir_entry.name), dir_entry.stat())
            )
        # TODO default sort by name
        return output
