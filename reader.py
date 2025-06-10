import json
from pathlib import Path

BOOKMARK_FILE = Path("data/bookmarks.json")


class BookmarkStore:
    def __init__(self):
        if BOOKMARK_FILE.exists():
            with open(BOOKMARK_FILE, "r") as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = {}

    def get(self, title: str) -> int:
        return self.bookmarks.get(title, 0)

    def save(self, title: str, page_index: int):
        self.bookmarks[title] = page_index
        with open(BOOKMARK_FILE, "w") as f:
            json.dump(self.bookmarks, f, indent=2)
