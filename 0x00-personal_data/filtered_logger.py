#!/usr/bin/env python3
"""
filtered_logger.py
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    * Copy the following code into filtered_logger.py.
    * Update the class to accept a list of strings fields constructor argument.
    * Implement the format method to filter values in incoming log records
    using filter_datum. Values for fields in fields should be filtered.
    * DO NOT extrapolate FORMAT manually. The format method should be less than
    5 lines long.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Format """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa
    """
    a function called filter_datum that returns the log message obfuscated:
    * Arguments:
        - fields: a list of strings representing all fields to obfuscate
        - redaction: a string representing by what the field will be obfuscated
        - message: a string representing the log line
        - separator: a string representing by which character is separating all
    fields in the log line (message)
    * The function should use a regex to replace occurrences of certain field
    values.
    * filter_datum should be less than 5 lines long and use re.sub to perform
    the substitution with a single regex.
    """
    for f in fields:
        message = re.sub(rf"{f}=(.*?)\{separator}",
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    * Use user_data.csv for this task
    * Implement a get_logger function that takes no arguments and returns a
    logging.Logger object.
    * The logger should be named "user_data" and only log up to logging.INFO
    level. It should not propagate messages to other loggers. It should have a
    StreamHandler with RedactingFormatter as formatter.
    * Create a tuple PII_FIELDS constant at the root of the module containing
    the fields from user_data.csv that are considered PII. PII_FIELDS can
    contain only 5 fields - choose the right list of fields that can are
    considered as “important” PIIs or information that you must hide in your
    logs. Use it to parameterize the formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    * In this task, you will connect to a secure holberton database to read a
    users table. The database is protected by a username and password that are
    set as environment variables on the server named PERSONAL_DATA_DB_USERNAME
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default as
    an empty string) and PERSONAL_DATA_DB_HOST (set the default as “localhost”)
    * The database name is stored in PERSONAL_DATA_DB_NAME.
    * Implement a get_db function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
        - Use the os module to obtain credentials from the environment
        - Use the module mysql-connector-python to connect to the MySQL
        database (pip3 install mysql-connector-python)
    """
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main() -> None:
    """
    * Implement a main function that takes no arguments and returns nothing.
    The function will obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under a filtered format.
    * Filtered fields:
        - name
        - email
        - phone
        - ssn
        - password
    * Only your main function should run when the module is executed.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
