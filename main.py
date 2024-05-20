import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_event('cut'))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_event('copy'))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_event('paste'))
        self.edit_menu.add_command(label="Delete", command=lambda: self.text_event('delete'))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=lambda: self.text_event('select_all'))

        self.current_file = None

    def new_file(self):
        self.current_file = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("Notepad - New File")

    def open_file(self):
        self.current_file = filedialog.askopenfilename(defaultextension=".txt", 
                                                       filetypes=[("All Files", "*.*"), 
                                                                  ("Text Documents", "*.txt")])
        if self.current_file:
            with open(self.current_file, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.root.title(f"Notepad - {self.current_file}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                         filetypes=[("All Files", "*.*"), 
                                                                    ("Text Documents", "*.txt")])
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"Notepad - {self.current_file}")

    def exit_app(self):
        self.root.quit()

    def text_event(self, event):
        if event == 'cut':
            self.text_area.event_generate("<<Cut>>")
        elif event == 'copy':
            self.text_area.event_generate("<<Copy>>")
        elif event == 'paste':
            self.text_area.event_generate("<<Paste>>")
        elif event == 'delete':
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        elif event == 'select_all':
            self.text_area.tag_add(tk.SEL, "1.0", tk.END)
            self.text_area.mark_set(tk.INSERT, "1.0")
            self.text_area.see(tk.INSERT)

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
