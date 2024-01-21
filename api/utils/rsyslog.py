import linux
import logging

logger = logging.getLogger(__name__)


def log_format():
    # Setup rsyslog output format
    log_format = linux.get_env("LOG_FORMAT", "plain")
    logger.info("Using {} log format for rsyslog.", log_format)
    linux.file_content_replace(
        file_path='/etc/rsyslog.conf',
        pattern='<log-format>',
        value=log_format
    )
