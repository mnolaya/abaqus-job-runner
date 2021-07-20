from set_config import configure_runner

# Set subroutines 
def set_subroutines():

    fmtstr = '-----\nDefault Abaqus analysis subroutine configuration setup\n-----'
    print(fmtstr)
    configurator = configure_runner()
    configurator.read_def_sub()

    fmtstr = (
        '\nWould you like to update the subroutine repository?\n'
        + 'Key 1 | APPEND | Add a new subroutine to repository.\n'
        + 'Key 2 | UPDATE | Update/revise an existing subroutine in the repository.\n'
        + 'Key 3 | OVERWRITE | Overwrite all existing subroutines in repository.'
    )
    print(fmtstr)
    fmtstr = 'Select option by key: '
    reply = int(raw_input(fmtstr))
    if reply == 1:
        configurator.create_new_sub()
    elif reply == 2:
        configurator.update_sub()
    elif reply == 3:
        fmtstr = '\nWarning! You are going to overwrite all existing subroutines in the repository. Okay to continue? [Y/N] '
        reply = raw_input(fmtstr)
        if reply.lower() == 'y':
            configurator.config['default subroutines'] = {}
            configurator.create_new_sub()
    else:
        print('Warning! An appropriate key was not selected. Try again...')
        return
    
    configurator.write_json(config=configurator.config)
    fmtstr = '\n-----\nUpdated default Abaqus analysis subroutine configuration setup\n-----\n'
    print(fmtstr)
    configurator.read_def_sub()

if __name__ == '__main__':
    set_subroutines()
