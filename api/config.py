import os


# Specify the directory path
CDIRECTORY = os.environ['GPOT_STORAGE_PATH'] if 'GPOT_STORAGE_PATH' in os.environ else '.gpost'

# Check if the directory already exists
if not os.path.exists(CDIRECTORY):
    # Create the directory
    os.makedirs(CDIRECTORY)
    # TODO: replace with logger
    print("Directory created successfully!")
else:
    # TODO: replace with logger
    print("Directory already exists!")

def _file_path_check(path):
    if not os.path.exists(path):
        with open(path, 'w') as fp:
            pass
    return path


def get_allowed_senders_path():
    return _file_path_check(CDIRECTORY + "/allowed_senders")

def get_main_config_path():
    return _file_path_check(CDIRECTORY + "/main.cf")

def get_config_dir():
    return CDIRECTORY