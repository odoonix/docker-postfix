import os

def _chekc_folder(name):
    # Check if the directory already exists
    if not os.path.exists(name):
        # Create the directory
        os.makedirs(name)
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


#########################################################################################
# Postfix
#########################################################################################
# Specify the directory path
CDIRECTORY = os.environ['GPOT_STORAGE_PATH'] \
    if 'GPOT_STORAGE_PATH' in os.environ \
        else '.gpost/postfix'
_chekc_folder(CDIRECTORY)



def get_allowed_senders_path():
    return _file_path_check(CDIRECTORY + "/allowed_senders")

def get_main_config_path():
    return _file_path_check(CDIRECTORY + "/main.cf")

def get_config_dir():
    return CDIRECTORY


#########################################################################################
# OpenDKIM
#########################################################################################
# Specify the directory path
DKIM_CDIRECTORY = os.environ['GPOT_DKIM_STORAGE_PATH'] \
    if 'GPOT_DKIM_STORAGE_PATH' in os.environ \
        else '.gpost/opendkim'
_chekc_folder(DKIM_CDIRECTORY)

def get_dkim_path():
    return DKIM_CDIRECTORY 
