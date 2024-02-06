import os
from . import linux 


#########################################################################################
# Postfix
#########################################################################################
# Specify the directory path
CDIRECTORY = os.environ['GPOT_STORAGE_PATH'] \
    if 'GPOT_STORAGE_PATH' in os.environ \
    else '.gpost/postfix'
linux.folder_exist(CDIRECTORY, create=True)


def get_allowed_senders_path():
    path = CDIRECTORY + "/allowed_senders"
    if linux.file_exist(path, touch=True):
        return path
    
    raise "File not found"

def get_virtual_alias_maps_path():
    path = CDIRECTORY + "/virtual_alias_maps"
    if linux.file_exist(path, touch=True):
        return path
    
    raise "\"virtual_alias_maps\" File not found"

def get_main_config_path():
    path = CDIRECTORY + "/main.cf"
    if linux.file_exist(path, touch=True):
        return path
    raise "File not fount"


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
