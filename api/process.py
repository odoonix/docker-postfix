import subprocess
import logging

logger = logging.getLogger(__name__)

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