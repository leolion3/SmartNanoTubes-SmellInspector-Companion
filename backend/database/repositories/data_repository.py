import sqlite3
from datetime import datetime
from typing import List

from database.repositories.abstract_repository import AbstractRepository


class DataRepository(AbstractRepository):
    """
    Handles data db operations.
    """

    __data_placeholder_template: str = ','.join('?' for _ in range(64))
    __data_insert_query: str = f'INSERT INTO Data VALUES (NULL, ?, ?, ?, ?, {__data_placeholder_template}, ?, ?)'
    __select_test_names_query: str = 'SELECT DISTINCT TEST_ID FROM Data;'
    __select_by_test_name_query: str = 'SELECT * FROM Data WHERE TEST_ID=? ORDER BY DATETIME ASC;'
    __select_by_substance_query: str = 'SELECT * FROM Data WHERE SUBSTANCE_ID=? ORDER BY TEST_ID DESC, DATETIME ASC;'
    __select_by_test_and_substance_query: str = ('SELECT * FROM Data WHERE TEST_ID=? AND SUBSTANCE_ID=? '
                                                 'ORDER BY DATETIME ASC;')

    def persist_data(
            self,
            test_name: str,
            mac_address: str,
            substance_id: str,
            test_date: datetime,
            data: List[str],
            temperature: str,
            humidity: str
    ) -> None:
        """
        Persists test data.
        :param test_name: The test name.
        :param mac_address: The device's unique mac address (distinguish between different SmellInspector devices).
        :param substance_id: The substance id of the substance being tested.
        :param test_date: The test date.
        :param data: The data to be stored as a 64-long list of strings.
        :param temperature: The measured temperature.
        :param humidity: The measured humidity.
        :raise InvalidDataException: if the data provided is formatted incorrectly.
        """
        test_date: str = test_date.strftime('%Y-%m-%d %H:%M:%S')  # ISO 8601 for sqlite sorting
        values = [test_name, mac_address, substance_id, test_date]
        values.extend(data)
        values.extend([temperature, humidity])
        self.execute_commit_update_query(self.__data_insert_query, values)

    def get_by_test_name_and_substance(self, test_name: str, substance_id: str) -> List[List[str]]:
        """
        Gets data by test name and substance.
        :param test_name: The test name.
        :param substance_id: The substance id of the substance being tested.
        :return: All
        """
        cursor: sqlite3.Cursor = self.execute_fetch_query(self.__select_by_test_and_substance_query,
                                                          [test_name, substance_id])
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_by_substance_id(self, substance_id: str) -> List[List[str]]:
        """
        Get all test data for a given substance.
        :param substance_id: The substance id to search for.
        :return: All data samples for the given substance.
        :raise InvalidDataException: if the data provided is formatted incorrectly.
        """
        cursor: sqlite3.Cursor = self.execute_fetch_query(self.__select_by_substance_query, [substance_id])
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_by_test_name(self, test_name: str) -> List[List[str]]:
        """
        Gets the data values given a test name.
        :param test_name: The test name.
        :return: All data samples for the given test name.
        """
        cursor: sqlite3.Cursor = self.execute_fetch_query(self.__select_by_test_name_query, [test_name])
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_test_names(self) -> List[str]:
        """
        Get a list of all unique test names.
        :return: All test names.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        results: List[str] = cursor.execute(self.__select_test_names_query).fetchall()
        cursor.close()
        return results

    def __init__(self, conn: sqlite3.Connection):
        """
        Constructor.
        :param conn: DB connection object.
        """
        super().__init__(conn)
        self.conn: sqlite3.Connection = conn
