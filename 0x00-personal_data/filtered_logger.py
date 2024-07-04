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
from typing import List, Tuple
import logging
import re
import os
import mysql.connector
from mysql.connector import connection


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


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

    def __init__(self, fields: List[str]):
        '''Initialize the instance'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records.'''
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''Creates and returns a logger with the specified settings'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    Establishes a connection to the database.

    Returns:
        Database connection object.
    '''
    connection = mysql.connector.connection.MySQLConnection(
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        port=3306
    )

    return connection


def main() -> None:
    '''Main function to retrieve and display users from the database.'''
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = 'SELECT * FROM users;'
    cursor.execute(query)

    for row in cursor:
        log_message = '; '.join([f'{key}={value}'
                                 for key, value in row.items()])
        logger.info(log_message)

    cursor.close()
    db.close()
