from github import Github
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from tkinter import *

# Global variable to track if Create Repo request initiated
switcher = 0


# Method to terminate Tkinter window upon cancellation of Create Repo request and reset of switcher variable
def exiter():
    global switcher
    switcher = 0
    root.destroy()
    return


# Tkinter window class
class Prompt_Window(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()

        # Window title
        self.winfo_toplevel().title("Create GitHub Repo")

        # Label declaration
        self.myLabel1 = Label(root, text="GitHub Access Token")
        self.myLabel2 = Label(root, text="GitHub Repo Name")

        # Entry field declaration
        self.myEntry1 = Entry(root, width=50)
        self.myEntry2 = Entry(root, width=50)

        # Button declaration
        self.repo_out = Button(root, text="Create GitHub Repo", command=make_repo)
        self.end_it = Button(root, text="Cancel", command=exiter)

        # Label positioning
        self.myLabel1.grid(row=0, column=0)
        self.myLabel2.grid(row=1, column=0)

        # Entry field positioning
        self.myEntry1.grid(row=0, column=1)
        self.myEntry2.grid(row=1, column=1)

        # Button positioning
        self.repo_out.grid(row=3, column=0)
        self.end_it.grid(row=3, column=1)


# Activation trigger
def on_modified(event):
    global switcher
    switcher = 1


# Method to create repo via GitHub API
def make_repo():
    token = app.myEntry1.get()
    repo_name = app.myEntry2.get()

    g = Github(token)
    user = g.get_user()
    user.create_repo(repo_name)

    print("Successfully Created " + repo_name + " Repository on GitHub")

    # Reset switcher global variable and close Tkinter window
    global switcher
    switcher = 0
    root.destroy()
    return


# Pipeline
if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_modified = on_modified
    # Changes to name of text file in the same directory as this main.py file
    path = "./observation"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            if switcher != 0:
                root = Tk()
                app = Prompt_Window(root)
                root.minsize(500, 100)
                root.maxsize(500, 100)
                root.mainloop()
                make_repo()

            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
