
import subprocess
import logging
import os

logger = logging.getLogger(__name__)


def folder_exist(folder_path, create=False):
    # Check if the directory already exists
    if not os.path.exists(folder_path):
        # Create the directory
        if not create:
            return False
        os.makedirs(folder_path)
    return True


def file_wirte(str, file_path):
    with open(file_path, 'w') as file:
        file.write(str)


def file_read(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def file_touch(file_path):
    with open(file_path, 'a') as fp:
        pass


def file_exist(file_path, touch=False):
    if not os.path.exists(file_path):
        if not touch:
            return False
        file_touch(file_path)
    return True


def file_link(source_path, link_path):
    """
    a wrapper of ln command
    """
    # ln -snf "$TZ_FILE" /etc/localtime
    return run([
        'ln',
        '-s',
        '-n',
        '-f',
        source_path,
        link_path
    ])


def file_content_replace(file_path, __old, __new):
    # Safely read the input filename using 'with'
    with open(file_path) as file:
        s = file.read()

    # Safely write the changed content, if found in the file
    with open(file_path, 'w') as file:
        file.write(s.replace(__old, __new))


def file_cp(src_file_path, dst_file_path):
    with open(src_file_path,'r') as firstfile, open(dst_file_path,'w') as secondfile: 
        for line in firstfile: 
             secondfile.write(line)
    return True 

def file_mv(src_file_path, dst_file_path):
    file_cp(src_file_path, dst_file_path)
    os.remove(src_file_path)
    return True


def get_env(key, default=False):
    if key in os.environ:
        return os.environ[key]
    return default


def run(command, shell=False, cwd='.'):
    try:
        ret = subprocess.call(
            command,
            shell=shell,
            cwd=cwd)
        return ret < 0
    except Exception as e:
        logger.error('Failed to execute command: %s', e)
        return False


def setup_timezone():
    """
    Sets local timezone in the linux machine.

    Check if we need to configure the container timezone
    """
    tz_env = get_env('TZ')
    if tz_env:
        file = "/usr/share/zoneinfo/{}".format(tz_env)
        if file_exist(file):
            logger.info("Setting container timezone to: {}", tz_env)
            file_link(file, '/etc/localtime')
            file_wirte(tz_env, '/etc/timezone')
        else:
            logger.warn(
                "Cannot set timezone to: {} -- this timezone does not exist.", tz_env)
            pass
    else:
        logger.warn("Not setting any timezone for the container")
