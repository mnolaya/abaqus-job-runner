import os
import json
import collections

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
        'subs': 'default subroutines'
    }
    

    def __init__(self, config_file=__json_file):
        self.check_json_exist(config_file=config_file)
    
    # Create config .json if one doesn't already exist.
    def check_json_exist(self, config_file=__json_file):
        if not os.path.isfile(config_file): self.write_json(config_file=config_file)

    # Load configuration from .json.
    def read_json(self, config_file=__json_file):
        with open(config_file, 'r') as f:
            config = json.load(f, object_pairs_hook=collections.OrderedDict)
        return config

    # Write configuration to .json with indentation.
    def write_json(self, config={}, config_file=__json_file):
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

    # Read default lookup directory.
    def read_def_dir(self, config):        
        # Initiate default directory config if none exists.
        section = self.__section_names['dirs']
        option = 'inp lookup'
        if not section in config: config[section] = {}
        if not option in config[section]:
            fmtstr = 'Initializing default directory to start browsing for .inp files in...\n'
            print(fmtstr)
            title = "Select directory to start browsing for .inp files in"
            outdir = user_dialogs().set_dir_dialog(title=title)
            config[section] = {}
            config[section][option] = outdir

        # Display default directory to command line.
        fmtstr = 'Default directory to start browsing for .inp files in:\n-----\n{dir}\n'
        print(fmtstr.format(dir=config[section][option]))
        return config

    # Read default subroutine locations.
    def read_def_sub(self, config):
        # Initate subroutine repository if none exists.
        section = self.__section_names['subs']
        if not section in config or config[section] == {}:
            config[section] = {}
            fmtstr = 'Initializing default subroutine location(s)...\n'
            print(fmtstr)
            config = self.create_new_sub(config=config)

        # Display subroutines to command line.
        fmtstr = '\nSubroutines stored in the job runner repository for future use:\n-----'
        print(fmtstr)
        for id in config[section]:
            sub = config[section][id]
            fmtstr = 'Subroutine ID: {id} | File: {subfile}'.format(id=id, subfile=sub)
            print(fmtstr)

        return config

    # Create new subroutine(s) to be added to config.
    def create_new_sub(self, config):
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
        return config

    # Update subroutine

    def build_job(self, inpname, subname, jobname=None, delete_mode='ON'):
        # Create job name from inp file name if none is provided.
        if jobname == None:
            jobname, __ = os.path.splitext(os.path.basename(inpname))

        # Dictionary to setup job run.
        job_dict = {
            'cmd': 'abaqus inter job={job} input={inp} user={sub} double=both ask_delete={delete}',
            'inp': 'inpname',
            'solver': 'subname',
        }

        fmtstr = job_dict['cmd'].format(job=jobname, inp=inpname, sub=subname, delete=delete_mode)
        return fmtstr

    # Read recent jobs.
    def read_recents(self):
        section = 'RECENT-JOBS'
        config = self.read_json()
        for i, r in enumerate(config[section]):
            recent = config[section][r]
            cmd = recent['cmd']
            date = recent['date']
            time = recent['time']
            fmtstr = '-----\nKey: {key}\nDate: {date} | Time: {time}\nCommand(s): {cmd}\n-----'
            print(fmtstr.format(key=i, date=date, time=time, cmd=cmd))

    # Save selected jobs.
    def save_selected_jobs(self, job_list):
        # Create json if one doesn't already exit.
        section = 'RECENT-JOBS'
        if not os.path.isfile(self.__json_file):
            recents = {
                section: {
                        'Recent 1': {},
                },
            }
            self.write_json(recents)

        # Ensure input job command(s) are in list form.       
        if type(job_list) is not list: job_list = [job_list]       

        # Check number of existing options in recent jobs section.
        config = self.read_json()
        if section in config:
            recents = [r for r in config[section]]
            num_recents = len(recents)
            if num_recents == self.__max_recents:
                num_recents = num_recents - 1
        else:
            recents = []
            num_recents = 0

        # Create temp option for recents section to be populated by job command(s).
        fmtstr = 'recent {num}'.format(num=(num_recents + 1))
        config[section][fmtstr] = 'temp'

        # Insert list of commands to beginning of recents list, then update config.
        old_jobs = [config[section][r] for r in recents]
        now = datetime.today()
        store_dict =  {
            'cmd': job_list,
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
        }
        old_jobs.insert(0, store_dict)
        for i, r in enumerate(config[section]):
            config[section][r] = old_jobs[i]

        # Write updated config file.     
        self.write_json(config)

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
