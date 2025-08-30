import tkinter as tk
from tkinter import font
from queue import Queue, Empty
import threading
import sys

class GraphicsMain:
    def __init__(self, title="Text Game Window", width=800, height=600, font_family="Consolas", font_size=14, bg="#181818", fg="#f8f8f2"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, bg=bg, fg=fg, insertbackground=fg, font=(font_family, font_size))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.config(state=tk.DISABLED)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.root, textvariable=self.input_var, font=(font_family, font_size), bg=bg, fg=fg, insertbackground=fg)
        self.input_entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.input_entry.bind("<Return>", self._on_enter)
        self.input_queue = Queue()
        self.output_queue = Queue()
        self._input_ready = threading.Event()
        self._setup_fonts(font_family, font_size)
        self._focus_input()

    def _setup_fonts(self, font_family, font_size):
        try:
            self.text_font = font.Font(family=font_family, size=font_size)
            self.text_widget.configure(font=self.text_font)
            self.input_entry.configure(font=self.text_font)
        except Exception:
            pass

    def _focus_input(self):
        self.root.after(100, lambda: self.input_entry.focus_set())

    def _on_enter(self, event=None):
        value = self.input_var.get()
        self.input_var.set("")
        self.input_queue.put(value)
        self._input_ready.set()

    def print(self, text, end="\n"):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text + end)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def input(self, prompt=""):
        self.print(prompt, end="")
        self._input_ready.clear()
        self._focus_input()
        self.root.wait_variable(self.input_var)
        self._input_ready.wait()
        try:
            return self.input_queue.get_nowait()
        except Empty:
            return ""

    def run(self, main_func, *args, **kwargs):
        def game_thread():
            sys.stdout = self
            sys.stdin = self
            main_func(*args, **kwargs)
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__
        t = threading.Thread(target=game_thread, daemon=True)
        t.start()
        self.root.mainloop()

    def write(self, text):
        self.print(text, end="")

    def flush(self):
        pass

    def readline(self):
        return self.input()

# Example usage (remove or comment out for import as a module):
# if __name__ == "__main__":
#     def test_game():
#         print("Welcome to the test game!")
#         name = input("What is your name? ")
#         print(f"Hello, {name}!")
#     GraphicsMain().run(test_game)
