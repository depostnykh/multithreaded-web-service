import os
import logging

HOST = os.environ.get('host')
PORT = int(os.environ.get('port'))
THREADS_COUNT = int(os.environ.get('threads_count'))

TIMEOUT = 15
BUFFER_SIZE = 1024
CODING_FORMAT = 'utf-8'

LOG_TO_FILE = False
FILE_NAME = 'server.log'
FILE_PATH = 'logs/'
FILE_LEVEL = 'DEBUG'
LEVEL = 'DEBUG'
NAME_TO_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARN,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}
