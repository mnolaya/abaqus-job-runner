import os
import configparser
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

class configure_abaqus:

    """
    Read/write config .ini files pertaining to Abaqus analyses.
    """

    ini_file = 'abaqus_jobrun_configuration.ini'
    max_recents = 10

    def __init__(self):
        self.config = configparser.ConfigParser()

    def save_selected_jobs(self, file_list):
        if file_list is not list: file_list = [file_list]
        section = 'RECENT-JOBS'
        config = self.config

        # Read config file and check for existence of section.

        # Set first recent option in config.
        config.read(self.ini_file)
        if config.has_section(section): 
            recents = config.options(section)
            num_recents = len(recents)
            # recents = recents[0:-1]
            if num_recents < self.max_recents:
                recents = ["Recent {num}".format(num=(n + 1)) for n in range(1, num_recents)]



            # if num_recents < self.max_recents:
            #     last_recent = num_recents + 1
            #     last_recent = "Recent {num}".format(num=last_recent)

            # elif num_recents == self.max_recents:
            #     last_recent = "Recent {num}".format(num=self.max_recents)

            # for       

        # else:
        #     last_recent = "Recent 1"

            # # Remove last recent and add most recent to beginning of options, and push others down.
            # if num_recents == self.max_recents:
            #     recent_no = self.max_recents
            #     # recents = recents[1:]

            # # Otherwise, just add most recent to begging of options and push others down.
            # else:
            #     recent_no = num_recents + 1

            # print(recent_no)
            # for opt in config.options(section): print(opt)
            #     print(opt)
            # print('check')
            # print(config.options(section))

        # config

        # config[section] = {
        #     recent_no: {
        #         'Input files': file_list,
        #         'Solver': 'iCure'
        #     }
        # }
        # # print(config)
        # with open(self.ini_file, 'w') as f:
        #     config.write(f)

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

    # test = [1, 2, 3]
    # print(test)
    # test = test[1:]
    # print(test)
    # test.append(5)
    # print(test)    



