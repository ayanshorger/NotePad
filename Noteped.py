import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Main Window
frame = tk.Tk()
frame.title("Notepad (Ayan Shorger)")
frame.geometry("800x600")

# Global variable
file_path = None

# Text Area (Default font added)
text_area = tk.Text(frame, undo=True, font=("Arial", 12))
text_area.pack(fill="both", expand=True)

# -------- Functions --------

def new_file():
    global file_path
    file_path = None
    text_area.delete(1.0, tk.END)
    frame.title("Untitled - Notepad")


def open_file():
    global file_path
    file = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file:
        file_path = file
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)
        frame.title(file)


def save_file():
    global file_path
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_area.get(1.0, tk.END))
    else:
        save_as()


def save_as():
    global file_path
    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file:
        file_path = file
        with open(file, "w", encoding="utf-8") as f:
            f.write(text_area.get(1.0, tk.END))
        frame.title(file)


def exit_app():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        frame.destroy()


def select_all():
    text_area.tag_add("sel", "1.0", "end")


def toggle_wrap():
    current = text_area.cget("wrap")
    text_area.config(wrap="none" if current == "word" else "word")


def undo_action():
    text_area.edit_undo()


def redo_action():
    text_area.edit_redo()


def cut_text():
    text_area.event_generate("<<Cut>>")


def copy_text():
    text_area.event_generate("<<Copy>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def delete_text():
    try:
        text_area.delete("sel.first", "sel.last")
    except tk.TclError:
        pass


def time_date():
    import time
    text_area.insert(tk.INSERT, time.strftime("%H:%M %d/%m/%Y"))


def view_help():
    messagebox.showinfo("Help", "This is a simple Notepad application built with Tkinter.")


def about_notepad():
    messagebox.showinfo("About Notepad", "Notepad - 5th Semester Project")


def send_feedback():
    messagebox.showinfo("Feedback", "Thank you for your feedback!")


def find_text():
    search_word = simpledialog.askstring("Find", "Enter text to find:")

    if search_word:
        text_area.tag_remove("found", "1.0", tk.END)
        start_pos = "1.0"

        while True:
            start_pos = text_area.search(search_word, start_pos, stopindex=tk.END)

            if not start_pos:
                break

            end_pos = f"{start_pos}+{len(search_word)}c"
            text_area.tag_add("found", start_pos, end_pos)
            start_pos = end_pos

        text_area.tag_config("found", background="yellow")


# -------- Zoom Functions --------

def zoom_in():
    current_font = text_area.cget("font")
    font_name, size = current_font.split()
    size = int(size) + 2
    text_area.config(font=(font_name, size))


def zoom_out():
    current_font = text_area.cget("font")
    font_name, size = current_font.split()
    size = int(size) - 2
    if size < 8:
        size = 8
    text_area.config(font=(font_name, size))


# ⭐ Mouse Scroll Zoom (Ctrl + Scroll)
def zoom_with_mouse(event):
    current_font = text_area.cget("font")
    font_name, size = current_font.split()
    size = int(size)

    if event.delta > 0:
        size += 2
    else:
        size -= 2

    if size < 8:
        size = 8

    text_area.config(font=(font_name, size))


# -------- Shortcuts --------

def bind_shortcuts(frame):
    frame.bind("<Control-n>", lambda e: new_file())
    frame.bind("<Control-o>", lambda e: open_file())
    frame.bind("<Control-s>", lambda e: save_file())
    frame.bind("<Control-a>", lambda e: select_all())


# -------- Menu --------

menu_bar = tk.Menu(frame)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo_action)
edit_menu.add_command(label="Redo", command=redo_action)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_command(label="Delete", command=delete_text)
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_command(label="Time/Date", command=time_date)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format Menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Word Wrap", command=toggle_wrap)
menu_bar.add_cascade(label="Format", menu=format_menu)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Zoom In", command=zoom_in)
view_menu.add_command(label="Zoom Out", command=zoom_out)
menu_bar.add_cascade(label="View", menu=view_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="View Help", command=view_help)
help_menu.add_command(label="Send Feedback", command=send_feedback)
help_menu.add_command(label="About Notepad", command=about_notepad)
menu_bar.add_cascade(label="Help", menu=help_menu)

frame.config(menu=menu_bar)

# Bind Shortcuts
bind_shortcuts(frame)

# ⭐ Mouse Zoom Bind
text_area.bind("<Control-MouseWheel>", zoom_with_mouse)

# Run App
frame.mainloop()