import os
import configparser
import json

from datetime import datetime

class configure_abaqus:

    """
    Read/write config .ini files pertaining to Abaqus analyses.
    """

    ini_file = 'abaqus_jobrun_configuration.ini'
    json_file = 'abaqus_jobrun_configuration.json'
    max_recents = 10

    def __init__(self):
        pass

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

    def read_json(self, json_file=json_file):
        with open(json_file, 'r') as f:
            config = json.load(f)
        return config
    
    def write_json(self, config, json_file=json_file):
        with open(json_file, 'w') as f:
            json.dump(config, f, indent=4)

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

    def save_selected_jobs(self, job_list):
        # Create json if one doesn't already exit.
        section = 'RECENT-JOBS'
        if not os.path.isfile(self.json_file):
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
            if num_recents == self.max_recents:
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