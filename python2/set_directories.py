from set_config import configure_runner
from dialogs import user_dialogs


def set_def_directories():
    configurator = configure_runner()
    configurator.read_json()
    dlgs = user_dialogs()

    fmtstr = '-----\nDefault extraction directory configuration setup\n-----'
    print(fmtstr)

    def_dirs = []
    section = 'default directories'
    configurator.read_def_dir()
    config = configurator.config
    # def_dirs.append(config[section]['odb data'])

    fmtstr = 'Would you like to update any of the directories in the config file? [Y/N]: '
    reply = raw_input(fmtstr)
    if reply.lower() == 'y':
        for k in config[section]:
            curr_dir = config[section][k]
            fmtstr = '\nCurrent option: {key} default directory'.format(key=k)
            print(fmtstr)
            fmtstr = 'Current directory: {dir}\nEnter 1 if updating directory, or 0 if leaving as-is: '.format(dir=curr_dir)
            reply = raw_input(fmtstr)
            if reply == '1':
                title = 'Select updated {key} default directory'.format(key=k)
                new_dir = dlgs.set_dir_dialog(title=title, inidir=curr_dir)
                fmtstr = 'Successfully updated!\nFrom: {old}\nTo: {new}'.format(old=curr_dir, new=new_dir)
                print(fmtstr)
                config[section][k] = new_dir
        configurator.write_json(config=config)

if __name__ == "__main__":
    set_def_directories()
