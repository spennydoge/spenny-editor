import tkinter as tk
from tkinter import filedialog, simpledialog
import base64

def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Spenny Editor - New File")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".spny",
                                           filetypes=[("Spenny Files", "*.spny"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "rb") as file:  # open as bytes
            encoded_data = file.read()
            try:
                decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            except Exception:
                decoded_data = "[Error: This file is not a valid Spenny File]"
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, decoded_data)
        root.title(f"Spenny Editor - {file_path}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".spny",
                                             filetypes=[("Spenny Files", "*.spny"), ("All Files", "*.*")])
    if file_path:
        text_data = text_area.get(1.0, tk.END)
        encoded_data = base64.b64encode(text_data.encode("utf-8"))  # encode to secret format
        with open(file_path, "wb") as file:
            file.write(encoded_data)
        root.title(f"Spenny Editor - {file_path}")

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def find_text():
    word = simpledialog.askstring("Find", "Enter text to find:")
    if word:
        start_pos = "1.0"
        while True:
            start_pos = text_area.search(word, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.tag_config("highlight", background="yellow", foreground="black")
            start_pos = end_pos

# Main Window
root = tk.Tk()
root.title("Spenny Editor")
root.geometry("700x500")

# Text Area
text_area = tk.Text(root, wrap="word", font=("Consolas", 12))
text_area.pack(fill="both", expand=True)

# Menu Bar
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)
root.mainloop()
