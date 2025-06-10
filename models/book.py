from pathlib import Path


class Book:
    def __init__(self, title: str, filepath: Path):
        self.title = title
        self.filepath = filepath
        self.pages = []
        self.current_page_index = 0
        self.page_size = 500  # number of characters per page (adjustable)

    def load(self, start_page=0):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            self.pages = [
                content[i : i + self.page_size]
                for i in range(0, len(content), self.page_size)
            ]
            self.current_page_index = start_page

    def get_current_page(self) -> str:
        if not self.pages:
            self.load(self.current_page_index)
        return self.pages[self.current_page_index]

    def next_page(self) -> str:
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
        return self.get_current_page()

    def prev_page(self) -> str:
        if self.current_page_index > 0:
            self.current_page_index -= 1
        return self.get_current_page()

    def reset(self):
        self.current_page_index = 0
