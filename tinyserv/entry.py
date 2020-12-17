from datetime import datetime, timedelta
from typing import List, Tuple
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
        self.human_timestamp, self.human_long_timestamp = self._human_date(timestamp)

        size = stat.st_size
        self.size = size
        self.human_size, self.human_long_size = self._human_size(size)

    @staticmethod
    def _human_size(size: float) -> Tuple[str, str]:
        """Return a short and full version of the human formated size."""
        sizes = [
            ("B", "byte"),
            ("KiB", "kibibyte"),
            ("MiB", "mibibyte"),
            ("GiB", "gibibyte"),
            ("TiB", "tebibyte"),
            ("PiB", "pebibyte"),
            ("EiB", "exbibyte"),
            ("ZiB", "zebibyte"),
            ("YiB", "yobibyte"),
        ]

        size_index = 0

        while size >= 1000 and size_index < len(sizes) - 1:
            size /= 1024
            size_index += 1

        value = f"{size:.2f}".rstrip("0").rstrip(".")

        short = f"{value} {sizes[size_index][0]}"
        full_unit = sizes[size_index][1] if size == 1 else f"{sizes[size_index][1]}s"
        full = f"{value} {full_unit}"
        return (short, full)

    @staticmethod
    def _human_date(timestamp: datetime) -> Tuple[str, str]:
        delta_now = datetime.now() - timestamp
        if delta_now <= timedelta(seconds=60):
            secs = delta_now.seconds
            if secs == 1:
                return (f"{secs}s ago", f"{secs} second ago")
            return (f"{secs}s ago", f"{secs} seconds ago")
        if delta_now <= timedelta(seconds=60 * 60):
            mins = delta_now.seconds // 60
            if mins == 1:
                return (f"{mins}m ago", f"{mins} minute ago")
            return (f"{mins}m ago", f"{mins} minutes ago")
        if delta_now <= timedelta(seconds=60 * 60 * 24):
            hours = delta_now.seconds // 60 // 60
            if hours == 1:
                return (f"{hours}h ago", f"{hours} hour ago")
            return (f"{hours}h ago", f"{hours} hours ago")
        if delta_now <= timedelta(days=1):
            return ("yesterday", "yesterday")

        return (f"{timestamp:%x}", f"{timestamp:%x}")

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
