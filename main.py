import tkinter as tk
from tkinter import scrolledtext
from tkinter import Frame
from tkinter import messagebox
import sys
from io import StringIO

class App(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master)

        self.window = master

        self.window.bind("<Control-Key-r>", self.runscript)
        self.window.bind("<Control-Key-R>", self.runscript)
        self.window.bind("<Escape>", self.exit_window)

        self.nav = tk.Frame(self.window)
        self.nav.pack(fill=tk.X)

        # Script Frame
        self.scriptbox = scrolledtext.ScrolledText(self.window)
        self.scriptbox.pack(fill=tk.BOTH, expand=True)
        self.scriptbox.bind("<Control-Key-a>", self.select_all)
        self.scriptbox.bind("<Control-Key-A>", self.select_all)
        self.scriptbox.focus_set()

        self.runbtn = tk.Button(self.nav, text="run", command=self.runscript)
        self.runbtn.pack(side=tk.RIGHT)

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

root = tk.Tk()
root.title("runPyGUI")
root.geometry('500x400')
myapp = App(root)

myapp.mainloop()