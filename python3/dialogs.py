import os
import tkinter as tk
import tkinter.filedialog as tkdialogs


class dialogs:

    """
    tkinter dialogs for getting input file names and setting directories used for Abaqus analyses.
    """

    def __init__(self):
        # Hide root Tk window.
        root = tk.Tk()
        root.withdraw()

    def get_inp_dialog(self, inidir=None):
        if inidir == None: inidir = os.getcwd()
        title = "Select input .inp file(s) to load"
        inp_files = tkdialogs.askopenfilenames(title=title, initialdir=inidir,
            filetypes=(("Abaqus input files", "*.inp"), )
        )
        return inp_files

    def set_dir_dialog(self, title, inidir=None):
        if inidir == None: inidir = os.getcwd()
        dir = tkdialogs.askdirectory(title=title, initialdir=inidir)
        return dir


# Testing framework.
if __name__ == "__main__":
    pass
    # dialog = dialogs()
    # inp_files = dialog.get_inp_dialog(inidir=r'C:\Users\micha\Google Drive\PhD\04-development\finite_strain')
    # print(inp_files)
    # title = "Select directory all output files are to be written to"
    # # title = "Select default initial .inp file lookup directory"
    # outdir = dialog.set_dir_dialog(title=title)
    # print(outdir)


