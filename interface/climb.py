import tkinter as tk
from tkinter import filedialog, messagebox
import interpreter
import sys
import threading

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CLSS Integrated Minimalist Builder")
        self.root.geometry("600x400")

        # Initialize saved path
        self.saved_path = None

        # Create a frame to hold the line numbers and text area
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack(expand=True, fill='both')

        # Line numbers area
        self.line_numbers = tk.Text(self.frame, width=4, bg='gray20', fg='white', padx=3, takefocus=0, border=0, state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Main text area
        self.text_area = tk.Text(self.frame, wrap='word', undo=True, bg='black', fg='white', insertbackground='white')
        self.text_area.pack(expand=True, fill='both')

        # Create a menu
        self.menu = tk.Menu(self.root, bg='gray20', fg='white')
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0, bg='gray20', fg='white')
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu, tearoff=0, bg='gray20', fg='white')
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)

        # Run menu
        self.run_menu = tk.Menu(self.menu, tearoff=0, bg='gray20', fg='white')
        self.menu.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run", command=self.run)

        # Bind keyboard shortcuts
        self.root.bind('<Control-a>', self.select_all)
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-x>', self.cut_text)
        self.root.bind('<Control-z>', self.undo_action)
        self.root.bind('<Control-Shift-Z>', self.redo_action)
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-Shift-S>', self.save_as)  # Save file shortcut
        self.root.bind('<Control-o>', self.open_file)  # Open file shortcut
        self.root.bind('<Control-r>', self.run)

        # Create output area for interpreter
        self.output_area = tk.Text(self.root, height=10, wrap='word', bg='gray20', fg='white')
        self.output_area.pack(expand=False, fill='x')

        # Update line numbers when the text area is modified
        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<MouseWheel>', self.update_line_numbers)
        self.text_area.bind('<Button-1>', self.update_line_numbers)

        # Initial line numbers update
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')
        self.line_numbers.config(state='disabled')

    def find_text(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        tk.Label(find_window, text="Find:", bg='gray20', fg='white').grid(row=0, column=0)
        find_entry = tk.Entry(find_window, width=30)
        find_entry.grid(row=0, column=1)
        find_button = tk.Button(find_window, text="Find", command=lambda: self.find(find_entry.get()))
        find_button.grid(row=1, columnspan=2)

    def find(self, word):
        self.text_area.tag_remove('found', '1.0', tk.END)
        if word:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                self.text_area.tag_add('found', start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config('found', background='yellow', foreground='black')

    def run(self, event=None):
        if hasattr(self, 'saved_path') and self.saved_path:
            file_path = self.saved_path
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".clss",
                                                    initialfile="new_file.clss",
                                                    filetypes=[("Text files", "*.txt"),
                                                              ("CLSS files", "*.clss"),
                                                              ("All files", "*.*")])
        if file_path:  # Check if a file path is provided
            self.saved_path = file_path
            self.save_file()
            self.saved_path = file_path  # Save the path for future use
            self.output_area.delete(1.0, tk.END)  # Clear previous output
            # Redirect print output to the output_area
            original_stdout = sys.stdout  # Save a reference to the original standard output
            sys.stdout = self  # Redirect standard output to this object

            # Create a thread for running the interpreter
            threading.Thread(target=self.run_interpreter, args=(file_path,), daemon=True).start()

    def run_interpreter(self, file_path):
        interpreter.clss(file_path)  # Call the interpreter function

        # Restore original standard output after interpreter has finished
        sys.stdout = sys.__stdout__  # Restore original standard output

    def write(self, message):
        self.output_area.insert(tk.END, message)  # Insert the message into the output area
        self.output_area.see(tk.END)  # Scroll to the end

    def flush(self):  # This method is needed to make the output stream usable
        pass

    def replace_text(self):
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace")
        tk.Label(replace_window, text="Find:", bg='gray20', fg='white').grid(row=0, column=0)
        tk.Label(replace_window, text="Replace:", bg='gray20', fg='white').grid(row=1, column=0)
        find_entry = tk.Entry(replace_window, width=30)
        replace_entry = tk.Entry(replace_window, width=30)
        find_entry.grid(row=0, column=1)
        replace_entry.grid(row=1, column=1)
        replace_button = tk.Button(replace_window, text="Replace", command=lambda: self.replace(find_entry.get(), replace_entry.get()))
        replace_button.grid(row=2, columnspan=2)

    def replace(self, find_word, replace_word):
        content = self.text_area.get(1.0, tk.END)
        new_content = content.replace(find_word, replace_word)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, new_content)

    def update_status(self, event=None):
        line, column = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f'Line: {line} | Column: {int(column) + 1}')

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.saved_path = None
        self.update_line_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".clss",
                                                filetypes=[("Text files", "*.txt"),
                                                           ("CLSS files", "*.clss"),
                                                           ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.saved_path = file_path
            self.update_line_numbers()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".clss",
                                                    initialfile="new_file.clss",
                                                    filetypes=[("Text files", "*.txt"),
                                                               ("CLSS files", "*.clss"),
                                                               ("All files", "*.*")])
        if file_path:
            self.saved_path = file_path
            self.save_file()

    def save_file(self):
        if self.saved_path:
            with open(self.saved_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as()

    def select_all(self, event=None):
        self.text_area.tag_add('sel', '1.0', 'end')

    def copy_text(self, event=None):
        self.root.clipboard_clear()
        text = self.text_area.get('sel.first', 'sel.last')
        self.root.clipboard_append(text)

    def paste_text(self, event=None):
        text = self.root.clipboard_get()
        self.text_area.insert(tk.INSERT, text)

    def cut_text(self, event=None):
        self.copy_text()
        self.text_area.delete('sel.first', 'sel.last')

    def undo_action(self, event=None):
        self.text_area.edit_undo()

    def redo_action(self, event=None):
        self.text_area.edit_redo()

def climb():
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    climb()
