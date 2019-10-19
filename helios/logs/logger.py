#!/usr/bin/env python3
# coding: utf-8

""" Logging module """

import logging
import threading

LOG_THREAD_FORMAT = 'thread-{} {}'  # when logging # threads
CUSTOM_LOG_FORMAT = '%(asctime)s %(levelname)s -> %(name)s: %(message)s'


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
