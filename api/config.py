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




def get_allowed_senders_path():
    # TODO: get the file list path from main.cf
    # NOTE: maso, 2024: We just support file map in the current version
    path =  CDIRECTORY + "/allowed_senders"
    if not os.path.exists(path):
        with open(path, 'w') as fp:
            pass
    return path