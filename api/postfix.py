import logging

import process
import config

logger = logging.getLogger(__name__)

def postmap(file_name,
            file_type = 'lmdb',
            config_dir = None):
    """
    postmap - Postfix lookup table management

    The postmap(1) creates or queries one or more Postfix lookup tables, 
    or updates an existing one.

    If the result files do not exist they will be created with the same 
    group and other read permissions as their source file.

    While the table update is in progress, signal delivery is postponed, 
    and an exclusive, advisory, lock is placed on the entire table, in 
    order to avoid surprises in spectator processes.

    Parameters
    ----------
    file_name:str
        The name of the lookup table source file when rebuilding a database.
    
    file_type:str
        The database type. {btree, cdb, dbm, fail, hash, lmdb, sdbm}
    """
    logger.info('Try to load a postmap for the path {}', file_name)

    if not config_dir:
        config_dir = config.get_config_dir()
    return process.run([
        "postmap",
        "-c",
        config_dir,
        file_type + ":" + file_name
    ])

def restart():
    logger.info('Try to restart the postfix')
    return process.run([
        "postfix",
        "reload",
    ])