import tkinter as tk
from tkinter import ttk

class PyReaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("📖 PyReader - Public Domain eBook Reader")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Top: Search Bar
        search_frame = ttk.Frame(self.master)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_books)
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

        self.prev_button = ttk.Button(nav_frame, text="⏪ Previous", command=self.prev_page)
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(nav_frame, text="Next ⏩", command=self.next_page)
        self.next_button.pack(side="right")

    # Placeholder methods
    def search_books(self):
        print("Searching for:", self.search_var.get())

    def next_page(self):
        print("Next page")

    def prev_page(self):
        print("Previous page")
