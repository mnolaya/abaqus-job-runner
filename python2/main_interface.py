from set_config import configure_runner

configurator = configure_runner()

fmtstr = '-----\nWelcome to the Abaqus job running tool!\nWritten by: Michael N. Olaya (c) iComp2 Research Group, UMass Lowell\n-----\n'
print(fmtstr)
configurator.read_def_dir()
configurator.read_def_sub()
fmtstr = (
    'If you would like to update any of the listed default directories, please run set_directories.py\n-----'
    + 'If you would like to update any of the listed subroutines, please run set_subroutines.py\n-----'
)
print(fmtstr)