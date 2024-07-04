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
from re import sub


def filter_datum(fields, redaction, message, separator):
    '''returns the log message obfuscated'''
    return sub('|'.join('(?<={}=)[^{}]+'.format(f, separator) for f in fields),
               redaction,
               message)
