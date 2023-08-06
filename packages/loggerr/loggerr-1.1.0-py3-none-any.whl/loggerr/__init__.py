# -*- coding: utf-8 -*-

from traceback import format_exc
from datetime import datetime
from json import dumps

"""
Log levels in order of severity
"""
levels = [
    'debug',
    'verbose',
    'info',
    'warn',
    'error',
    'critical',
    'silent'
]

synonyms = [
    ['log', 'info'],
    ['warning', 'warn'],
    ['fatal', 'critical'],
    ['panic', 'critical']
]


class Loggerr:
    """ Create a JSON logger with minimal log level
    Args:
        logLevel (str): Minimal log level (case insensitive)
        persistent (dic): Fields to append to each log record
    Example:
        logger = Loggerr('warn')
        logger.info('Something going as expected', { 'host': socket.gethostname() }) # ignored
        logger.error('Something must have gone terribly wrong') # sent
    """
    def __init__(self, logLevel='info', persistent={}):
        if not serializable(persistent):
            raise TypeError('Persistent enrichment dictionary must be JSON serializable')

        minimum = levels.index(logLevel.lower())
        for level in levels:
            if levels.index(level) < minimum:
                setattr(self, level, ignore)
            else:
                setattr(self, level, Log(level, persistent))

        for synonym in synonyms:
            setattr(self, synonym[0], Log(synonym[1], persistent))


def ignore(message, persistent={}):
    """ Ignore incoming log record
    Args:
        * match "log" function interface
    """
    return


def serializable(dic):
    """
    Check dictionary if JSON serializable
    Args:
        dic {dic} dictionary
    Return:
        boolean
    """
    try:
        dumps(dic)
        return True
    except (TypeError, OverflowError):
        return False


def Log(level, persistent={}):
    """ Create a log function
    Args:
        level (str): The log level to attach
        persistent (dic): Fields to append to each log record
    Return:
        log (function)
    """
    def log(message, enrichment={}):
        """ Log JSON to stdout
        Args:
            message (str): String to log in records' "message" key
            enrichment (dic): More fields to append to the log record
        """
        record = {
            **persistent,
            'message': str(message),
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'level': level
        }
        if (isinstance(message, Exception)):
            record['trace'] = format_exc()

        if (serializable(enrichment)):
            print(dumps({**enrichment, **record}))
        else:
            print(dumps(record))
    return log
