import logging

import utils.linux as linux
import api.utils.storage as storage
import os

logger = logging.getLogger(__name__)


def postmap(file_name,
            file_type='lmdb',
            config_dir=None):
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
        config_dir = storage.get_config_dir()
    return linux.run([
        "postmap",
        "-c",
        config_dir,
        file_type + ":" + file_name
    ])


def postalias(file_name):
    logger.info('Try to load a postalias for the path {}', file_name)
    return linux.run([
        "postalias",
        file_name
    ])


def restart():
    logger.info('Try to restart the postfix')
    return linux.run([
        "postfix",
        "reload",
    ])


def setup_conf():
    """
    Copy over files from /etc/postfix.template to /etc/postfix,
    if the user mounted the folder manually
    """
    template_path = "./templates/"
    base_path = storage.get_config_dir()

    # Make sure the /etc/postfix directory exists
    linux.run(['mkdir', '-p', base_path])

    # Make sure all the neccesary files (and directories) exist
    if linux.folder_exist(template_path):
        for file_path in os.listdir(template_path):
            file_name = os.path.basename(file_path)
            dst_file_path = storage.get_config_file_path(file_name)

            if not linux.file_exist(dst_file_path):
                logger.info("Creating {}.", dst_file_path)
                linux.file_cp(file_path, dst_file_path)

    # linux.run([
    #     'mkdir',
    #     '-p',
    #     '/var/spool/postfix/pid',
    #     '/var/spool/postfix/dev'
    # ])
    # linux.run(['chown', 'root:', '/var/spool/postfix/'])
    # linux.run(['chown', 'root:', '/var/spool/postfix/pid'])

    config_set("manpage_directory", "/usr/share/man")

    # postfix set-permissions complains if documentation files do not exist
    linux.run(['postfix', '-c', base_path, 'set-permissions'])


def config_set(key, value):
    # XXX
    pass


def config_add(key, value):
    # XXX
    pass


def config_load():
    # XXX
    pass


def config_flush():
    # XXX
    # Check for any references to the old "hash:" and "btree:" databases and replae them with "lmdb:"
    # Upgrade old coniguration, replace "hash:" and "btree:" databases to "lmdb:"
    pass

    # TODO: postalias /etc/postfix/aliases


##############################################################################
# Configuration and checks
##############################################################################
def check_utf8_support():
    # Disable SMTPUTF8, because libraries (ICU) are missing in alpine
    if linux.file_exist('/etc/alpine-release'):
        config_set('smtputf8_enable', 'no')


def check_aliases():
    logger.info(
        "Update aliases database. It's not used, but postfix complains if the .db file is missing")

    alias_file = storage.get_config_file_path('aliases')
    linux.file_touch(alias_file)
    postalias(alias_file)
