import os

import tkinter as tk
import tkinter.filedialog as tkdialogs
import configparser

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

class configure_abaqus:

    """
    Read/write config .ini files pertaining to Abaqus analyses.
    """

    ini_file = 'abaqus_jobrun_configuration.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()

    def save_selected_jobs(self, file_list):
        if file_list is not list: file_list = [file_list]
        section = 'RECENT-JOBS'
        config = self.config
        config[section] = {
            'Recent 1': {
                'Input files': file_list,
                'Solver': 'iCure'
            }
        }
        print(config)
        with open(self.ini_file, 'w') as f:
            config.write(f)

    # def 


# print(tkdialogs.askopenfilenames)
# Open file dialog for 

# Testing framework.
if __name__ == "__main__":
    # dialog = dialogs()
    # inp_files = dialog.get_inp_dialog(inidir=r'C:\Users\micha\Google Drive\PhD\04-development\finite_strain')
    # print(inp_files)
    # title = "Select directory all output files are to be written to"
    # # title = "Select default initial .inp file lookup directory"
    # outdir = dialog.set_dir_dialog(title=title)
    # print(outdir)

    inp_files = "test1.inp"
    outdir = "testout1/test"

    config_aba = configure_abaqus()
    config_aba.save_selected_jobs(file_list=inp_files)
    



