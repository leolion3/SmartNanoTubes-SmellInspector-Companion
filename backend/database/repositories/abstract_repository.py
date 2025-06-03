import sqlite3
from typing import List

from exception.Exceptions import InvalidDataException
from log_handler.log_handler import Module, Logger, get_instance

logger: Logger = get_instance()


class AbstractRepository:
    """
    Abstract repo containing common operation queries.
    """

    def execute_fetch_query(self, query: str, params: List) -> sqlite3.Cursor:
        """
        Executes an sql query and returns the cursor for fetch operations.
        :param query: the sql query.
        :param params: the parameters of the query.
        :return: The cursor.
        :raise InvalidDataException: if the data provided is formatted incorrectly.
        """
        try:
            cursor: sqlite3.Cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor
        except Exception as e:
            logger.error(f'Error executing fetch query \"{query}\" with params \"{params}\". Trace:', e,
                         module=Module.DB)
            raise InvalidDataException()

    def execute_commit_update_query(self, query: str, params: List) -> None:
        """
        Executes an sql query with no return value.
        :param query: the sql query.
        :param params: the parameters of the query.
        :return:
        :raise InvalidDataException: if the data provided is formatted incorrectly.
        """
        try:
            cursor: sqlite3.Cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            logger.error(f'Error executing commit/update query \"{query}\" with params \"{params}\". Trace:',
                         e, module=Module.DB)
            raise InvalidDataException()

    def execute_simple_commit_query(self, query: str) -> None:
        """
        Executes an sql query and commits the changes.
        :param query: the sql query.
        :return:
        :raise InvalidDataException: on error.
        """
        try:
            cursor: sqlite3.Cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            logger.error(f'Error executing simple query \"{query}\". Trace:', e, module=Module.DB)
            raise InvalidDataException()

    def __init__(self, conn: sqlite3.Connection):
        """
        Constructor.
        :param conn: Database connection object.
        """
        self.conn = conn
