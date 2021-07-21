import os
import json
import collections
import subprocess

from datetime import datetime

from dialogs import user_dialogs

class configure_runner:

    """
    Read/write config files pertaining to Abaqus analyses.
    """

    # ini_file = 'abaqus_jobrun_configuration.ini'
    __json_file = 'abaqus_jobrun_configuration.json'
    __max_recents = 10
    __section_names = {
        'dirs': 'default directories',
        'subs': 'default subroutines',
        'jobs': 'recent jobs'
    }    

    def __init__(self, config_file=__json_file):
        self.check_json_exist(config_file=config_file)
    
    # Create config .json if one doesn't already exist, get config if it does.
    def check_json_exist(self, config_file=__json_file):
        if not os.path.isfile(config_file): 
            self.write_json(config_file=config_file)
        else:
            self.read_json(config_file=config_file)

    # Load configuration from .json.
    def read_json(self, config_file=__json_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f, object_pairs_hook=collections.OrderedDict)
        # return config

    # Write configuration to .json with indentation.
    def write_json(self, config={}, config_file=__json_file):
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    # Read default lookup directory.
    def read_def_dir(self):        
        # Initiate default directory config if none exists.
        config = self.config
        section = self.__section_names['dirs']
        option = 'inp lookup'
        if not section in config: config[section] = {}
        if not option in config[section]:
            fmtstr = 'Initializing default directory to start browsing for .inp files in...\n'
            print(fmtstr)
            title = "Select directory to start browsing for .inp files in"
            outdir = user_dialogs().set_dir_dialog(title=title)
            config[section][option] = outdir
            self.write_json(config=config)

        option = 'analysis output'
        if not option in config[section]:
            fmtstr = 'Initializing default analysis output directory...\n'
            print(fmtstr)
            title = "Select directory for all analysis files to be written to"
            outdir = user_dialogs().set_dir_dialog(title=title)
            config[section][option] = outdir
            self.write_json(config=config)

        # Display default directory to command line.
        fmtstr = '*Default directories:\n-----'
        print(fmtstr)
        for opt in config[section]:
            fmtstr = 'Name: {name} | Directory: {dir}'.format(name=opt, dir=config[section][opt])
            print(fmtstr)

        self.config = config

    # Read default subroutine locations.
    def read_def_sub(self):
        # Initate subroutine repository if none exists.
        config = self.config
        section = self.__section_names['subs']
        if not section in config or config[section] == {}:
            config[section] = {}
            fmtstr = '\nInitializing default subroutine location(s)...\n'
            print(fmtstr)
            self.create_new_sub()
            self.write_json(config=config)

        # Display subroutines to command line.
        fmtstr = '\n*Subroutines currently stored in the job runner repository for future use:\n-----'
        print(fmtstr)
        for id in config[section]:
            sub = config[section][id]
            fmtstr = 'Subroutine ID: {id} | File: {subfile}'.format(id=id, subfile=sub)
            print(fmtstr)

        self.config = config

    # Create new subroutine(s) to be added to config.
    def create_new_sub(self):
        config = self.config
        section = self.__section_names['subs']
        while True:
            fmtstr = 'Please select a subroutine from the file explorer to be added to the job runner repository.'
            print(fmtstr)
            sub = user_dialogs().get_sub_dialog(inidir=config['default directories'])
            fmtstr = 'Enter a unique identifier to name this subroutine for future use: '
            id = raw_input(fmtstr)
            config[section][id] = sub
            fmtstr = 'Would you like to add another subroutine to the repository for future use? [Y/N]: '
            reply = raw_input(fmtstr)
            if reply.lower() != 'y':
                break
        self.config = config

    # Update existing subroutine(s) in config.
    def update_sub(self):
        config = self.config
        section = self.__section_names['subs']
        
        # Create keys for existing subroutines.
        fmtstr = '\nThe following subroutines can be updated:\n-----'
        print(fmtstr)
        for i, id in enumerate(config[section], start=1):
            fmtstr = 'Key: {key} | Subroutine ID: {id} | File: {subfile}'.format(
                key=i, id=id, subfile=config[section][id])
            print(fmtstr)

        # Allow user to select subroutines to be updated by key.
        fmtstr = (
            '\nSelect by key the subroutine you would like to update.'
            + '\n-----\nNote:'
            + '\n(1) Multiple subroutines can be chosen -- separate key with space'
        )
        print(fmtstr)
        key = raw_input('Subroutine key(s): ').split()
        old_subs = [config[section].keys()[int(i) - 1] for i in key]
        for old_id in old_subs:
            fmtstr = 'Please select a subroutine from the file explorer to replace {sub_id} in the job runner repository.'
            print(fmtstr.format(sub_id=old_id))
            new_sub = user_dialogs().get_sub_dialog(inidir=config['default directories'])
            fmtstr = 'Enter a unique identifier to name this subroutine for future use: '
            new_id = raw_input(fmtstr)
            config[section][new_id] = config[section].pop(old_id)
            config[section][new_id] = new_sub

        self.config = config

    def build_jobs(self, inpfiles=None, subname=None, delete_mode='ON'):

        if inpfiles == None: inpfiles = self.inp_files
        if subname == None: subname = self.use_subroutine

        if delete_mode.lower() == 'on':
            fmtstr = '\n*Warning! delete_mode is turned ON. Previous jobs (in the output directory) that have the same name as those being run will be overwritten.\n'
            print(fmtstr)

        # Ensure all input file names and subroutien names are set to strings.
        for inpname in inpfiles: 
            if type(inpname) is not str: inpname = str(inpname)            
        if type(subname) is not str: subname = str(subname)

        # Loop through all input files and build job commands from selected input files/subroutine.
        job_list = []
        for f in inpfiles:
            # Create job name from inp file name.
            jobname, __ = os.path.splitext(os.path.basename(inpname))

            # Dictionary to setup job run.
            job_dict = {
                'cmd': 'abaqus inter job={job} input="{inp}" user="{sub}" double=both ask_delete={delete}',
                'inp': 'inpname',
                'solver': 'subname',
            }
            job_list.append(job_dict['cmd'].format(job=jobname, inp=inpname, sub=subname, delete=delete_mode))

        self.job_list = job_list

    # Read recent jobs.
    def read_recents(self):
        config = self.config
        section_jobs = self.__section_names['jobs']
        section_dirs = self.__section_names['dirs']
        inidir = config[section_dirs]['inp lookup']
        if section_jobs in config:
            fmtstr = 'Would you like to re-run a recently submitted job? [Y/N]: '
            reply = raw_input(fmtstr)
            if reply.lower() == 'y':
                self.job_list = self.select_recent_jobs()
                self.use_recents = True
            else:
                self.inp_files= user_dialogs().get_inp_dialog(inidir=inidir)
                self.use_recents = False
        else:
            fmtstr = '\nNo recent files detected in the config file!'
            print(fmtstr)
            self.inp_files= user_dialogs().get_inp_dialog(inidir=inidir)
            self.use_recents = False

    # Select subroutine from repository.
    def set_subroutine(self):
        config = self.config
        section = self.__section_names['subs']
        fmtstr = '\nSelect by key ONE subroutine to be used when running the input files.\n-----'
        print(fmtstr)
        for i, id in enumerate(config[section], start=1):
            fmtstr = 'Key {key} | Subroutine ID: {sub} | File: {subfile}'
            print(fmtstr.format(key=i, sub=id, subfile=config[section][id]))
        fmtstr = 'Subroutine key: '
        reply = int(raw_input(fmtstr)) - 1
        id = config[section].keys()[reply]
        self.use_subroutine = config[section][id]

    # Prompt user to select recent job(s) by key.
    def select_recent_jobs(self):
        config = self.config
        section = self.__section_names['jobs']

        # Create keys for all recent job entries.
        fmtstr = '\nRecent jobs available for re-run:\n-----'
        print(fmtstr)
        for i, r in enumerate(config[section], start=1):
            recent = config[section][r]
            cmd = [str(c) for c in recent['cmd']]
            date = recent['date']
            time = recent['time']
            fmtstr = '\nKey: {key}\nDate: {date} | Time: {time}\nCommand(s): {cmd}\n-----'
            print(fmtstr.format(key=i, date=date, time=time, cmd=cmd))

        # Allow user to select multiple keys.
        fmtstr = 'Select recent job(s) by key: '
        reply = raw_input(fmtstr).split()

        # Create new job list from all keys.
        reply = [int(i) - 1 for i in reply]        
        jobs = []
        for r in reply:
            key = config[section].keys()[r]
            jobs = jobs + config[section][key]['cmd']

        # Allow user to select part or all of new job list.
        fmtstr = '-----\nSelected recent job commands\n-----'
        print(fmtstr)
        for i, job in enumerate(jobs, start=1):
            fmtstr = '\nKey: {key}\nCommand: {job}\n-----'
            print(fmtstr.format(key=i, job=job))
        fmtstr = '\nSelect jobs to run their key numbers separated by a space OR type A to select all: '
        reply = raw_input(fmtstr).split()
        if reply[0].lower() != 'a':
            reply = [int(i) - 1 for i in reply]
            selected_jobs = []
            for i in reply:
                selected_jobs.append(str(jobs[i]))
        else:
            selected_jobs = [str(j) for j in jobs]

        return selected_jobs   

    # Save selected jobs.
    def save_selected_jobs(self, job_list):
        # Create json if one doesn't already exit.
        section = self.__section_names['jobs']

        # Ensure input job command(s) are in list form.       
        if type(job_list) is not list: job_list = [job_list] 

        # Create dictionary to store in config for current job list.
        now = datetime.today()
        store_dict = {
            'cmd': job_list,
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
        }     

        # Check number of existing options in recent jobs section.
        config = self.config
        if section in config:
            recents = [r for r in config[section]]
            num_recents = len(recents)
            if num_recents == self.__max_recents:
                num_recents = num_recents - 1
        else:
            config[section] = {}
            recents = []
            num_recents = 0

        # Create temp option for recents section to be populated by job command(s).
        fmtstr = 'recent {num}'.format(num=(num_recents + 1))
        config[section][fmtstr] = 'temp'

        # Insert list of commands to beginning of recents list, then update config.
        old_jobs = [config[section][r] for r in recents]
        old_jobs.insert(0, store_dict)

        for i, r in enumerate(config[section]):
            config[section][r] = old_jobs[i]

        # Write updated config file.     
        self.config = config

    # Run an Abaqus job by command.
    @staticmethod
    def run_job(cmd, output_dir):
        curr_dir = os.getcwd()
        os.chdir(output_dir)

        # Print Abaqus command to terminal.
        fmtstr = (
            '\n----- ABAQUS JOB COMMAND -----\n'
            + '{cmd}\n\N'
            + '*Output located at: {dir}\n'
            + '------------------------------'
        ).format(cmd=cmd, dir=output_dir)
        print(fmtstr)

        # Run analysis.
        print(cmd)
        # subprocess.call(cmd, shell=True)

        # Return to starting directory.
        os.chdir(curr_dir)

# Testing framework.
if __name__ == "__main__":
    
    test_inp = [
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp1.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp2.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp3.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp4.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp5.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp6.inp',
        r'C:\Users\micha\Google Drive\coding\projects\abaqus-job-runner\python3\test_inp7.inp'
    ]
    subname = r"C:\Users\micha\Google Drive\PhD\06-code\process_model\dev_branch\source\curing\curing_main.for"

    config_aba = configure_abaqus()
    new_recent = []

    for f in test_inp:
        cmd = config_aba.build_job(inpname=f, subname=subname)
        new_recent.append(cmd)

    config_aba.save_selected_jobs(new_recent)
    config_aba.read_recents()
