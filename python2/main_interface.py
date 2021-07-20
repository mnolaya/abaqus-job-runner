from set_config import configure_runner

configurator = configure_runner()
config = configurator.read_json()

fmtstr = '-----\nWelcome to the Abaqus job running tool!\nWritten by: Michael N. Olaya (c) iComp2 Research Group, UMass Lowell\n-----\n'
print(fmtstr)
config = configurator.read_def_dir(config=config)
configurator.write_json(config=config)
config = configurator.read_def_sub(config=config)


quit()
fmtstr = 'If you would like to update any of the listed default directories, please run save_def_directories.py\n-----'
print(fmtstr)
configurator.write_json(config=config)
