import requests
from bs4 import BeautifulSoup
from pathlib import Path

LIBRARY_DIR = Path("library")

class Fetcher:
    def __init__(self):
        LIBRARY_DIR.mkdir(exist_ok=True)

    def search(self, keyword: str) -> list:
        """Search Gutenberg for matching books."""
        url = f"https://www.gutenberg.org/ebooks/search/?query={keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("li.booklink")

        books = []
        for result in results[:5]:  # limit to top 5 results
            title_tag = result.select_one("span.title")
            link_tag = result.select_one("a")
            if title_tag and link_tag:
                title = title_tag.text.strip()
                book_id = link_tag["href"].split("/")[-1]
                books.append((title, book_id))

        return books

    def download_txt(self, title: str, book_id: str) -> Path:
        """Download the plain text version of the book."""
        txt_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        response = requests.get(txt_url)
        if response.status_code != 200:
            txt_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt"
            response = requests.get(txt_url)

        if response.status_code == 200:
            filepath = LIBRARY_DIR / f"{title}.txt"
            with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
                f.write(response.text)
            return filepath
        else:
            raise Exception("Could not download text version.")
