import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.widgets import Button, Label, Combobox, Frame, Labelframe

from ttkbootstrap import Style

from ttkbootstrap.constants import *
from tkinter import StringVar
from fetcher import Fetcher
from models.book import Book
from reader import BookmarkStore
from pathlib import Path

LIBRARY_DIR = Path("library")


class PyReaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("📖 PyReader - Public Domain eBook Reader")
        self.master.geometry("800x600")

        # Initialize state
        self.current_font_size = 12
        self.dark_mode = False
        self.default_font = ("Courier New", self.current_font_size)
        self.search_results = []
        self.current_book = None

        # Models
        self.fetcher = Fetcher()
        self.bookmark_store = BookmarkStore()

        # Create GUI elements
        self.create_widgets()

        # ✅ Safe to bind now
        self.book_list.bind("<<ListboxSelect>>", self.on_book_select)

    def create_widgets(self):
        # Top: Search Bar
        search_frame = tb.Frame(self.master)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = StringVar()
        self.search_entry = tb.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_button = Button(
            search_frame,
            text="🔍 Search",
            command=self.search_books,
            bootstyle="primary"
        )

        self.search_button.pack(side="left", padx=5)

        # ✅ Add "My Library" button right after "Search"
        self.library_button = tb.Button(
            search_frame, text="My Library", command=self.load_local_books
        )
        self.library_button.pack(side="left", padx=5)

        # Left: Book List
        # self.book_list = tb.Listbox(self.master)
        # self.book_list.pack(side="left", fill="y", padx=10, pady=5)

        left_frame = tb.Frame(self.master)
        left_frame.pack(side="left", fill="y", padx=10, pady=5)

        self.book_list = tk.Listbox(left_frame, width=30)  # wider
        self.book_list.pack(fill="both", expand=True)

        # Right: Book Content
        text_frame = tb.Frame(self.master)
        text_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.book_text = tk.Text(text_frame, wrap="word")
        self.book_text.pack(fill="both", expand=True)

        # Bottom: Navigation Frame
        nav_frame = tb.Frame(self.master)
        nav_frame.pack(fill="x", padx=10, pady=5)

        # Previous/Next Buttons
        self.prev_button = tb.Button(
            nav_frame, text="⏪ Previous", command=self.prev_page
        )
        self.prev_button.pack(side="left")

        self.next_button = tb.Button(nav_frame, text="Next ⏩", command=self.next_page)
        self.next_button.pack(side="left", padx=5)

        # Font size toggle
        font_frame = tb.Frame(nav_frame)
        font_frame.pack(side="left", padx=10)

        tb.Label(font_frame, text="Font Size:").pack(side="left")
        self.font_size_box = tb.Combobox(
            font_frame, values=[10, 12, 14, 16, 18], width=3
        )
        self.font_size_box.set(self.current_font_size)
        self.font_size_box.bind("<<ComboboxSelected>>", self.update_font_size)
        self.font_size_box.pack(side="left")

        # Dark mode toggle
        self.theme_button = tb.Button(
            nav_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode
        )
        self.theme_button.pack(side="right")

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
            if book_id:  # If online search result
                filepath = self.fetcher.download_txt(title, book_id)
            else:  # If local book
                filepath = LIBRARY_DIR / f"{title}.txt"
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

    def load_local_books(self):
        self.book_list.delete(0, tk.END)
        self.search_results = []  # Clear web search data

        for file in LIBRARY_DIR.glob("*.txt"):
            title = file.stem
            self.book_list.insert(tk.END, title)
            # Store dummy book_id (not used for local)
            self.search_results.append((title, None))

    def update_font_size(self, event=None):
        self.current_font_size = int(self.font_size_box.get())
        self.book_text.config(font=("Courier New", self.current_font_size))

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#1e1e1e" if self.dark_mode else "white"
        fg = "white" if self.dark_mode else "black"
        self.book_text.config(bg=bg, fg=fg, insertbackground=fg)
        self.book_list.config(bg=bg, fg=fg)
        # Add styling to entry and frame if desired
        self.search_entry.config(bg=bg, fg=fg, insertbackground=fg)
        self.font_size_box.config(background=bg, foreground=fg)

    def reset_view(self):
        self.book_text.delete("1.0", "end")
        self.current_book = None
