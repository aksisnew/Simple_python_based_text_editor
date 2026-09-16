import os
import tkinter as tk
from tkinter import filedialog, messagebox, font


class TextEditor:

  def __init__(self, root):
    self.root = root
    self.root.title("Simple Text Editor")
    self.root.geometry("800x600")

    self.current_file = None
    self.dark_mode = False

    # Main Layout Frame
    self.main_frame = tk.Frame(self.root)
    self.main_frame.pack(fill=tk.BOTH, expand=True)

    # Scrollbar
    self.scrollbar = tk.Scrollbar(self.main_frame)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text Area
    self.text_area = tk.Text(
        self.main_frame,
        font=("Courier", 12),
        undo=True,
        wrap=tk.WORD,
        yscrollcommand=self.scrollbar.set,
    )
    self.text_area.pack(fill=tk.BOTH, expand=True)
    self.scrollbar.config(command=self.text_area.yview)

    # Status Bar
    self.status_bar = tk.Label(
        self.root,
        text="Line 1, Col 0 | Words: 0",
        anchor="e",
        bd=1,
        relief=tk.SUNKEN,
    )
    self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Event Bindings for Status Bar & Shortcuts
    self.text_area.bind("<KeyRelease>", self.update_status)
    self.text_area.bind("<ButtonRelease-1>", self.update_status)

    # Menu Bar Setup
    self.create_menu()

    # Keyboard Shortcuts
    self.bind_shortcuts()

  def create_menu(self):
    menu_bar = tk.Menu(self.root)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(
        label="New", command=self.new_file, accelerator="Ctrl+N"
    )
    file_menu.add_command(
        label="Open...", command=self.open_file, accelerator="Ctrl+O"
    )
    file_menu.add_command(
        label="Save", command=self.save_file, accelerator="Ctrl+S"
    )
    file_menu.add_command(
        label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S"
    )
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.exit_app)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit Menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(
        label="Undo",
        command=lambda: self.text_area.event_generate("<<Undo>>"),
        accelerator="Ctrl+Z",
    )
    edit_menu.add_command(
        label="Redo",
        command=lambda: self.text_area.event_generate("<<Redo>>"),
        accelerator="Ctrl+Y",
    )
    edit_menu.add_separator()
    edit_menu.add_command(
        label="Cut",
        command=lambda: self.text_area.event_generate("<<Cut>>"),
        accelerator="Ctrl+X",
    )
    edit_menu.add_command(
        label="Copy",
        command=lambda: self.text_area.event_generate("<<Copy>>"),
        accelerator="Ctrl+C",
    )
    edit_menu.add_command(
        label="Paste",
        command=lambda: self.text_area.event_generate("<<Paste>>"),
        accelerator="Ctrl+V",
    )
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # View Menu
    view_menu = tk.Menu(menu_bar, tearoff=0)
    view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
    menu_bar.add_cascade(label="View", menu=view_menu)

    self.root.config(menu=menu_bar)

  def bind_shortcuts(self):
    self.root.bind("<Control-n>", lambda e: self.new_file())
    self.root.bind("<Control-o>", lambda e: self.open_file())
    self.root.bind("<Control-s>", lambda e: self.save_file())
    self.root.bind("<Control-S>", lambda e: self.save_as_file())

  def update_status(self, event=None):
    cursor_pos = self.text_area.index(tk.INSERT)
    line, col = cursor_pos.split(".")

    text_content = self.text_area.get(1.0, tk.END).strip()
    words = len(text_content.split()) if text_content else 0

    self.status_bar.config(
        text=f"Line {line}, Col {col} | Words: {words}  "
    )

  def new_file(self):
    self.text_area.delete(1.0, tk.END)
    self.current_file = None
    self.root.title("Untitled - Simple Text Editor")
    self.update_status()

  def open_file(self):
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("All Files", "*.*"),
        ]
    )
    if file_path:
      try:
        with open(file_path, "r", encoding="utf-8") as f:
          content = f.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.current_file = file_path
        self.root.title(
            f"{os.path.basename(file_path)} - Simple Text Editor"
        )
        self.update_status()
      except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")

  def save_file(self):
    if self.current_file:
      try:
        content = self.text_area.get(1.0, tk.END)
        with open(self.current_file, "w", encoding="utf-8") as f:
          f.write(content)
        self.root.title(
            f"{os.path.basename(self.current_file)} - Simple Text Editor"
        )
      except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")
    else:
      self.save_as_file()

  def save_as_file(self):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("All Files", "*.*"),
        ],
    )
    if file_path:
      self.current_file = file_path
      self.save_file()

  def toggle_theme(self):
    if not self.dark_mode:
      self.text_area.config(bg="#1e1e1e", fg="#ffffff", insertbackground="white")
      self.status_bar.config(bg="#2d2d2d", fg="#ffffff")
      self.dark_mode = True
    else:
      self.text_area.config(bg="#ffffff", fg="#000000", insertbackground="black")
      self.status_bar.config(bg="#f0f0f0", fg="#000000")
      self.dark_mode = False

  def exit_app(self):
    self.root.destroy()


if __name__ == "__main__":
  root = tk.Tk()
  app = TextEditor(root)
  root.mainloop()
