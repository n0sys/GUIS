import tkinter as tk
from tkinter import Frame, scrolledtext, OptionMenu
import sys
from io import StringIO
import platform
import uuid
import os
import subprocess
import stat

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
        # Switch language bind
        self.window.bind("<Alt-Right>", self.switch_right_lang)
        self.window.bind("<Alt-Left>", self.switch_left_lang)
        # Delete whole word
        self.window.bind("<Control-BackSpace>", self.delete_whole_word)

        # Nav Frame
        self.nav = tk.Frame(self.window)
        self.nav.pack(fill=tk.X)

        # Script Frame
        self.scriptbox = scrolledtext.ScrolledText(self.window)
        self.scriptbox.pack(fill=tk.BOTH, expand=True)
        self.scriptbox.bind("<Control-Key-a>", self.select_all)
        self.scriptbox.bind("<Control-Key-A>", self.select_all)
        self.focus_widget(self.scriptbox)

        # Run button
        self.runbtn = tk.Button(self.nav, text="Run", command=self.runscript)
        self.runbtn.pack(side=tk.RIGHT)

        # Help button
        self.helpbtn = tk.Button(self.nav, text="Help", command=self.show_help)
        self.helpbtn.pack(side=tk.RIGHT)

        # Change script languages based on OS
        self.platform = platform.system()
        if self.platform == "Windows":
            self.languages = ['Python', 'Powershell']
        elif self.platform == "Linux":
            self.languages = ['Python', 'Bash']

        # Script Language Menu
        self.lang = tk.StringVar(self.window)
        self.lang.set(self.languages[0])
        self.languageMenu = OptionMenu(self.nav, self.lang, *self.languages)
        self.languageMenu.pack(side=tk.LEFT)

    def runscript(self, event=None):
        # Check current language set
        language = self.lang.get()

        script = self.scriptbox.get("1.0", tk.END)

        # Python
        if language == "Python":
            try:
                sys.stdout = mystdout = StringIO()
                exec(script)
                output = mystdout.getvalue()
            except Exception as e:
                output = e
        # Bash
        elif language == "Bash":
            # Create tmp bash file 
            write_dir = '/tmp'
            filepath = f"{write_dir}/{str(uuid.uuid4())}.sh"
            with open(filepath, "w") as scriptfile:
                scriptfile.write(script)
            
            # Add file permissions
            os.chmod(filepath, stat.S_IRWXU)

            # Run script
            outputfile = f"{write_dir}/output.{str(uuid.uuid4())}.guis"
            os.system(f"bash {filepath} >{outputfile} 2>&1")
            with open(outputfile, "r") as outputfile:
                output = "".join(outputfile.readlines())

            os.remove(filepath)
        self.output(output)
        
    
    def output(self, output):
        outputWindow = tk.Tk()
        outputWindow.title("Output")
        
        outputWindow.bind("<Escape>", self.exit_window)

        outputBox = scrolledtext.ScrolledText(outputWindow)

        # Output box binds
        outputBox.bind("<Control-Key-a>", self.select_all)
        outputBox.bind("<Control-Key-A>", self.select_all)
        outputBox.bind("<Control-BackSpace>", self.delete_whole_word)

        outputBox.pack(expand=True, fill=tk.BOTH)

        outputBox.insert(tk.INSERT, output)
        self.focus_widget(outputBox)

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

        self.focus_widget(helpBox)
        
        helpBox.pack(expand=True, fill=tk.BOTH)

        helpBox.insert(tk.INSERT, _help_text)
        helpBox.configure(state = tk.DISABLED)

    def focus_widget(self, widget):
        widget.focus_set()
        widget.focus_force()

    def switch_right_lang(self, event):
        self.lang.set(self.languages[(self.languages.index(self.lang.get()) + 1) % len(self.languages)])
    
    def switch_left_lang(self, event):
        self.lang.set(self.languages[(self.languages.index(self.lang.get()) - 1) % len(self.languages)])

    def delete_whole_word(self, event):
        event.widget.delete("insert-1c wordstart", "insert")
        return "break"
    
_help_text = """Graphical User Interface Script is a tool to run your scripts in a GUI.

But why? Cz im sick of creating files to run my scripts only to delete them right afterwards

Hotkeys to help you go fast:
- CTRL+ESC: Close open window
- CTRL+A: Select all
- CTRL+R: Run script
- ALT+Right/Left: Switch languages
- Control-BackSpace: Delete whole word
- CTRL+H: Display this text message"""

root = tk.Tk()
root.title("GUIS")
root.geometry('500x400')
myapp = App(root)

myapp.mainloop()