import tkinter as tk
from tkinter import ttk
from fetcher import Fetcher
from models.book import Book
from reader import BookmarkStore


class PyReaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("📖 PyReader - Public Domain eBook Reader")
        self.master.geometry("800x600")
        self.create_widgets()
        self.fetcher = Fetcher()
        self.search_results = []  # store (title, book_id) tuples
        self.book_list.bind("<<ListboxSelect>>", self.on_book_select)
        self.current_book = None  # track which book is open
        self.bookmark_store = BookmarkStore()

    def create_widgets(self):
        # Top: Search Bar
        search_frame = ttk.Frame(self.master)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_button = ttk.Button(
            search_frame, text="Search", command=self.search_books
        )
        self.search_button.pack(side="left", padx=5)

        # Left: Book List
        self.book_list = tk.Listbox(self.master)
        self.book_list.pack(side="left", fill="y", padx=10, pady=5)

        # Right: Book Content
        text_frame = ttk.Frame(self.master)
        text_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.book_text = tk.Text(text_frame, wrap="word")
        self.book_text.pack(fill="both", expand=True)

        # Bottom: Navigation
        nav_frame = ttk.Frame(self.master)
        nav_frame.pack(fill="x", padx=10, pady=5)

        self.prev_button = ttk.Button(
            nav_frame, text="⏪ Previous", command=self.prev_page
        )
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(nav_frame, text="Next ⏩", command=self.next_page)
        self.next_button.pack(side="right")

    # Placeholder methods
    def search_books(self):
        keyword = self.search_var.get()
        if not keyword.strip():
            return

        self.search_results = self.fetcher.search(keyword)
        self.book_list.delete(0, tk.END)

        for title, _ in self.search_results:
            self.book_list.insert(tk.END, title)

        print(f"Found {len(self.search_results)} books.")

    def next_page(self):
        if self.current_book:
            self.current_book.next_page()
            self.display_current_page()
            self.bookmark_store.save(
                self.current_book.title, self.current_book.current_page_index
            )

    def prev_page(self):
        if self.current_book:
            self.current_book.prev_page()
            self.display_current_page()
            self.bookmark_store.save(
                self.current_book.title, self.current_book.current_page_index
            )

    def on_book_select(self, event):
        if not self.search_results:
            return

        selection = self.book_list.curselection()
        if not selection:
            return

        index = selection[0]
        title, book_id = self.search_results[index]

        try:
            filepath = self.fetcher.download_txt(title, book_id)
            start_page = self.bookmark_store.get(title)
            self.current_book = Book(title, filepath)
            self.current_book.load(start_page)
            self.display_current_page()
        except Exception as e:
            print("❌ Failed to download or open book:", e)

    def display_current_page(self):
        if self.current_book:
            content = self.current_book.get_current_page()
            self.book_text.delete("1.0", tk.END)
            self.book_text.insert(tk.END, content)
