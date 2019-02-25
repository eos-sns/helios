#!/usr/bin/env python3
# coding: utf-8

""" Logging module """

import logging
import threading

LOG_THREAD_FORMAT = 'thread-{} {}'  # when logging # threads
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
CUSTOM_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

LOG_LEVEL = logging.DEBUG

LOGGER = logging.getLogger('hyperion')
LOGGER.setLevel(LOG_LEVEL)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(LOG_LEVEL)
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_FORMAT))

LOGGER.addHandler(STREAM_HANDLER)


class Logger:
    def __init__(self, logger_name):
        formatter = logging.Formatter(fmt=CUSTOM_LOG_FORMAT)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def log_message(self, *message):
        """Logs message

        :param message: message to log
        """
        self.logger.debug(' '.join(message))

    def log_error(self, *error, cause=None):
        """Logs error

        :param error: error to log
        :param cause: (optional) cause of error
        """
        thread_id = threading.current_thread().ident
        text = ' '.join(error)
        if cause:
            text += ' due to ' + str(cause)

        self.logger.error(LOG_THREAD_FORMAT.format(thread_id, text))


def get_custom_logger(logger_name):
    return Logger(logger_name)
