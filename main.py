import tkinter as tk
from tkinter import scrolledtext
from tkinter import Frame
import sys
from io import StringIO

class App(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master)

        self.window = master

        # Run bind
        self.window.bind("<Control-Key-r>", self.runscript)
        self.window.bind("<Control-Key-R>", self.runscript)
        # Exit bind
        self.window.bind("<Escape>", self.exit_window)
        # Help bind
        self.window.bind("<Control-Key-H>", self.show_help)
        self.window.bind("<Control-Key-h>", self.show_help)

        # Nav Frame
        self.nav = tk.Frame(self.window)
        self.nav.pack(fill=tk.X)

        # Script Frame
        self.scriptbox = scrolledtext.ScrolledText(self.window)
        self.scriptbox.pack(fill=tk.BOTH, expand=True)
        self.scriptbox.bind("<Control-Key-a>", self.select_all)
        self.scriptbox.bind("<Control-Key-A>", self.select_all)
        self.scriptbox.focus_set()

        self.runbtn = tk.Button(self.nav, text="Run", command=self.runscript)
        self.runbtn.pack(side=tk.RIGHT)

        self.helpbtn = tk.Button(self.nav, text="Help", command=self.show_help)
        self.helpbtn.pack(side=tk.RIGHT)

    def runscript(self, event=None):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        script = self.scriptbox.get("1.0", tk.END)

        try:
            exec(script)
            output = mystdout.getvalue()
        except Exception as e:
            output = e

        sys.stdout = old_stdout

        self.output(output)
    
    def output(self, output):
        outputWindow = tk.Tk()
        outputWindow.title("Output")
        
        outputWindow.bind("<Escape>", self.exit_window)

        outputBox = scrolledtext.ScrolledText(outputWindow)
        outputBox.bind("<Control-Key-a>", self.select_all)
        outputBox.bind("<Control-Key-A>", self.select_all)

        outputBox.pack(expand=True, fill=tk.BOTH)

        outputBox.insert(tk.INSERT, output)
        outputBox.focus_set()

    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return 'break'
    
    def exit_window(self, event):
        event.widget.master.master.destroy()

    def show_help(self, event=None):
        helpWindow = tk.Tk()
        helpWindow.title("Help")
        
        helpWindow.bind("<Escape>", self.exit_window)

        helpBox = scrolledtext.ScrolledText(helpWindow)

        helpBox.focus_set()
        
        helpBox.pack(expand=True, fill=tk.BOTH)

        helpBox.insert(tk.INSERT, _help_text)
        helpBox.configure(state = tk.DISABLED)

_help_text = """Graphical User Interface Script is a tool to run your scripts in a GUI.

But why? Cz im sick of creating files to run my scripts only to delete them right afterwards

Hotkeys to help you go fast:
- CTRL+ESC: Close open window
- CTRL+A: Select all
- CTRL+R: Run script
- CTRL+H: Display this text message"""

root = tk.Tk()
root.title("GUIS")
root.geometry('500x400')
myapp = App(root)

myapp.mainloop()