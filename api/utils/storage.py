import os
import linux


#########################################################################################
# Postfix
#########################################################################################
# Specify the directory path
CDIRECTORY = os.environ['GPOT_STORAGE_PATH'] \
    if 'GPOT_STORAGE_PATH' in os.environ \
    else '.gpost/postfix'
linux.folder_exist(CDIRECTORY, create=True)


def get_allowed_senders_path():
    return linux.file_exist(CDIRECTORY + "/allowed_senders", touch=True)


def get_main_config_path():
    return linux.file_exist(CDIRECTORY + "/main.cf", touch=True)


def get_config_dir():
    return CDIRECTORY


def get_config_file_path(name):
    return CDIRECTORY + '/' + name


#########################################################################################
# OpenDKIM
#########################################################################################
# Specify the directory path
DKIM_CDIRECTORY = os.environ['GPOT_DKIM_STORAGE_PATH'] \
    if 'GPOT_DKIM_STORAGE_PATH' in os.environ \
    else '.gpost/opendkim'
linux.folder_exist(DKIM_CDIRECTORY, create=True)


def get_dkim_path():
    return DKIM_CDIRECTORY
