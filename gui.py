from tkinter import *
from tkinter.filedialog import askopenfilename
from main import *


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Main GUI")

        self.filename = ""

        self.label = Label(master, text="Messenger Analyzer")
        self.label.pack()

        self.file_button = Button(master, text="Browse", command=self.open_file)
        self.file_button.pack()

        self.run_button = Button(master, text="Run", command=self.run)
        self.run_button.pack()

    def open_file(self):
        self.filename = askopenfilename()
        print("Got filename")

    def run(self):
        exec_output(self.filename)


root = Tk()
my_gui = GUI(root)
root.mainloop()