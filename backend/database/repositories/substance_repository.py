import sqlite3
from sqlite3 import Cursor
from typing import List, Tuple

from database.repositories.abstract_repository import AbstractRepository, logger
from exception.Exceptions import InvalidDataException
from log_handler.log_handler import Module


class SubstanceRepository(AbstractRepository):
    """
    Handles substances in the database.
    """

    __add_substance_query: str = 'INSERT INTO Substance VALUES (NULL, ?, ?);'
    __get_substance_by_id_query: str = 'SELECT * FROM Substance WHERE ID=?;'
    __update_substance_query: str = 'UPDATE Substance SET SUBSTANCE_NAME=?, QUANTITY=? WHERE ID=?;'
    __check_datapoint_for_substance_exists: str = 'SELECT * FROM Data WHERE ID=? LIMIT 1;'
    __check_substance_exists_query: str = 'SELECT * FROM Substance WHERE SUBSTANCE_NAME=? AND QUANTITY=?'
    __delete_substance_query: str = 'DELETE FROM Substance WHERE ID=?;'
    __fetch_substances_query: str = 'SELECT * FROM Substance;'

    def __check_substance_name_and_quantity_exist(self, substance_name: str, quantity: str) -> bool:
        """
        Checks whether a given substance name and quantity already exist.
        :param substance_name: The substance name.
        :param quantity: The quantity.
        :return: True if a substance with the given name and quantity exist, False otherwise.
        """
        substance_name = substance_name.lower()
        quantity = quantity.lower()
        results: Cursor = self.execute_fetch_query(self.__check_substance_exists_query, [substance_name, quantity])
        result_set: List[List[str]] = results.fetchall()
        return result_set is not None and len(result_set)

    def get_substance_by_id(self, substance_id: str) -> Tuple[str, str]:
        """
        Get the substance details for a given substance id.
        :param substance_id: The substance id.
        :return: The substance details for the given substance id.
        :raises InvalidDataException: If the substance does not exist.
        """
        try:
            result: Cursor = self.execute_fetch_query(self.__get_substance_by_id_query, [substance_id])
            result_set: List[List[str]] = result.fetchall()
            if result_set is None or not len(result_set):
                raise InvalidDataException('Substance does not exist.')
            _, substance_name, quantity = result_set[0]
            return substance_name, quantity
        except InvalidDataException:
            raise
        except Exception as e:
            logger.error(f'Error fetching substance with id \"{substance_id}\". Trace:', e, module=Module.DB)
            raise InvalidDataException('Invalid substance id.')

    def get_substances(self) -> List[List[str]]:
        """
        Fetch all substances from the database.
        :return: A list of all substances.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        data = cursor.execute(self.__fetch_substances_query).fetchall()
        cursor.close()
        return data

    def add_substance(self, substance_name: str, quantity: str) -> None:
        """
        Adds a new substance to the database.
        :param substance_name: The name of the substance.
        :param quantity: The quantity of the substance.
        :return:
        :raise InvalidDataException: on error.
        """
        try:
            if self.__check_substance_name_and_quantity_exist(substance_name, quantity):
                raise InvalidDataException('Substance with given name and quantity already exists.')
            self.execute_commit_update_query(self.__add_substance_query, [substance_name, quantity])
            logger.info(f'Created new substance with name \"{substance_name}\" '
                        f'and quantity \"{quantity}\"', module=Module.DB)
        except InvalidDataException:
            raise
        except Exception as f:
            logger.error('Error adding new substance. Trace:', f, module=Module.DB)
            raise InvalidDataException('Error creating substance. Invalid data provided.')

    def update_substance(self, substance_id: str, substance_name: str, quantity: str) -> None:
        """
        Updates a substance in the database.
        :param substance_id: Substance ID.
        :param substance_name: new Substance name.
        :param quantity: new Substance quantity.
        :return:
        :raise InvalidDataException: on error.
        """
        try:
            substance, _ = self.get_substance_by_id(substance_id)
            if substance == 'air':
                raise InvalidDataException('Cannot update the default "air" substance.')
            result: Cursor = self.execute_fetch_query(self.__get_substance_by_id_query, [substance_id])
            result_set: List[List[str]] = result.fetchall()
            if result_set is None or not len(result_set):
                raise InvalidDataException(f'No substance found for given ID \"{substance_id}\"')
            if self.__check_substance_name_and_quantity_exist(substance_name, quantity):
                raise InvalidDataException('Substance with given name and quantity already exist.')
            self.execute_commit_update_query(self.__update_substance_query,
                                             [substance_name.lower(), quantity.lower(), substance_id])
            logger.info(f'Updated substance with id \"{substance_id}\". Name set to \"{substance_name}\" '
                        f'and quantity set to \"{quantity}\".', module=Module.DB)
        except InvalidDataException:
            raise
        except Exception as f:
            logger.error('Error updating substance. Trace:', f, module=Module.DB)
            raise InvalidDataException('Error updating substance. Invalid data provided.')

    def delete_substance(self, substance_id: str) -> None:
        """
        Deletes a substance from the database.
        :param substance_id: Substance ID for the substance to be deleted.
        :return:
        :raise InvalidDataException: on error.
        """
        try:
            substance, _ = self.get_substance_by_id(substance_id)
            if substance == 'air':
                raise InvalidDataException('Cannot remove the default "air" substance.')
            result: Cursor = self.execute_fetch_query(self.__check_datapoint_for_substance_exists, [substance_id])
            result_set: List[List[str]] = result.fetchall()
            if result_set is None or not len(result_set):
                self.execute_commit_update_query(self.__delete_substance_query, [substance_id])
                logger.info(f'Deleted substance with id \"{substance_id}\"', module=Module.DB)
                return
            raise InvalidDataException(f'No substance found for given ID \"{substance_id}\"')
        except InvalidDataException:
            raise
        except Exception as f:
            logger.error('Error deleting substance. Trace:', f, module=Module.DB)
            raise InvalidDataException('Error deleting substance. Invalid data provided.')

    def create_air_substance(self) -> None:
        """
        Adds the default substance - air - to the database.
        :return:
        """
        try:
            substances: List[List[str]] = self.get_substances()
            if not len(substances):
                logger.info('Substances empty, adding default "air" substance.', module=Module.DB)
                self.add_substance('air', '')
                return
            logger.info('Substances present, skipping defaults.', module=Module.DB)
        except Exception as e:
            logger.error('Error creating air substance. Trace:', e, module=Module.DB)

    def __init__(self, conn: sqlite3.Connection):
        """
        Constructor.
        :param conn: DB connection object.
        """
        super().__init__(conn)
        self.conn: sqlite3.Connection = conn
