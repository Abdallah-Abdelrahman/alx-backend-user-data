#!/usr/bin/env python3
'''Module defines `filter_datum` function.

Methods:
    filter_datum:
        Args:
            fields: a list of strings representing all fields to obfuscate
            redaction: string representing by what the field will be obfuscated
            message: a string representing the log line
            separator: a string representing by which character is separating,
            all fields in the log line (message)
        Returns:
            str: log message obfuscated
'''
from typing import List
import logging
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    return re.sub(
            '|'.join('(?<={}=)[^{}]+'.format(f, separator) for f in fields),
            redaction,
            message)


class RedactingFormatter(logging.Formatter):
    '''Redacting Formatter class
    '''

    REDACTION = '***'
    FORMAT = '[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s'
    SEPARATOR = ';'

    def __init__(self, fields):
        '''Initialize the instance'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records.'''
        return filter_datum(self.fields,
                            self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)
