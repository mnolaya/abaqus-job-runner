from set_config import configure_runner
from dialogs import user_dialogs

def set_subroutines(config):
    configurator = configure_extractor()
    config = configurator.read_json()
    dlgs = user_dialogs()

    fmtstr = '-----\nDefault Abaqus analysis subroutine configuration setup\n-----'
    section = 'default subroutines'





if __name__ == '__main__':
    config = {
        'default subroutines': {
            'sub 1': 'subroutine 1',
            'sub 2': 'subroutine 2',
        }
    }
    set_subroutines(config)
