from set_config import configure_runner
from stopwatch import stopwatch

configurator = configure_runner()
sw = stopwatch()

fmtstr = '-----\nWelcome to the Abaqus job running tool!\nWritten by: Michael N. Olaya (c) iComp2 Research Group, UMass Lowell\n-----\n'
print(fmtstr)
configurator.read_def_dir()
configurator.read_def_sub()
fmtstr = (
    '\n-If you would like to update any of the listed default directories, please run set_directories.py'
    + '\n-If you would like to update any of the listed subroutines, please run set_subroutines.py\n-----'
)
print(fmtstr)

while True:

    # Read recent jobs from config file. If recent jobs are not requested, promprt user to select new .inp files.
    configurator.read_recents()

    # Build job commands from subroutine selection and selected .inp files if recents are not requested.
    if not configurator.use_recents:
        configurator.set_subroutine()
        configurator.build_jobs()

    # Save job list to config file recents.
    configurator.save_selected_jobs(job_list=configurator.job_list)
    configurator.write_json(config=configurator.config)

    # Run jobs.
    sw.start_clock()
    for job in configurator.job_list:
        configurator.run_job(cmd=job, output_dir=configurator.config['default directories']['analysis output'])
        sw.stop_clock()
        fmtstr = (
            '\n----- RUNTIME INFORMATION -----\n'
            + '-Analaysis date: {date}\n'
            + '-Analysis runtime: {runtime} minutes\n'
            + '-Total elapsed time: {elapsed} minutes\n'
            + '------------------------------\n'
        ).format(date=sw.date, runtime=sw.lap/60, elapsed=sw.total_time/60)
        print(fmtstr)
    
    # Continue?
    fmtstr = 'Would you like to continue running jobs? [Y/N]: '
    reply = raw_input(fmtstr)
    if reply.lower() != 'y':
        print('\nTerminating Abaqus job running tool...\n...\nI was tired anyway.')
        break
