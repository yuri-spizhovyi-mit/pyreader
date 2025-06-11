import ttkbootstrap as tb
from gui import PyReaderGUI

if __name__ == "__main__":
    root = tb.Window(themename="solar")  # 🔥 Try "darkly", "cyborg", "morph", etc.
    app = PyReaderGUI(root)
    root.mainloop()
