import os
import sqlite3

from database.repositories.data_repository import DataRepository
from database.repositories.device_repository import DeviceRepository
from database.repositories.substance_repository import SubstanceRepository
from exception.Exceptions import DBInitialisationException
from log_handler.log_handler import Module, log as logger
import config


class DatabaseHandler:
    """
    Creates tables and serves repository apis.
    """

    __data_create_headers: str = ','.join([f'DATA_{i} TEXT NOT NULL' for i in range(64)])
    __data_create_query: str = ('CREATE TABLE IF NOT EXISTS Data ('
                                'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                                'TEST_ID TEXT NOT NULL,'
                                'MAC_ADDRESS TEXT NOT NULL,'
                                'SUBSTANCE_ID TEXT NOT NULL,'
                                'DATETIME DATE NOT NULL,'
                                f'{__data_create_headers},'
                                'TEMPERATURE TEXT NOT NULL,'
                                'HUMIDITY TEXT NOT NULL );')
    __create_device_table_query: str = ('CREATE TABLE IF NOT EXISTS Device ('
                                        'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                                        'DEVICE_NAME TEXT NOT NULL,'
                                        'MAC_ADDRESS TEXT NOT NULL,'
                                        'SOFTWARE_VERSION TEXT NOT NULL,'
                                        'FAN_STATE TEXT NOT NULL,'
                                        'SOCKET TEXT NOT NULL,'
                                        'CONNECTED BOOLEAN NOT NULL);')
    __create_substance_table_query: str = ('CREATE TABLE IF NOT EXISTS Substance ('
                                           'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                                           'SUBSTANCE_NAME TEXT NOT NULL,'
                                           'QUANTITY TEXT NOT NULL);')

    def __create_tables(self) -> None:
        """
        Creates all tables.
        :return:
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        logger.info('Creating data table...', module=Module.DB)
        cursor.execute(self.__data_create_query)
        logger.info('Data table created.', module=Module.DB)
        logger.info('Creating device table...', module=Module.DB)
        cursor.execute(self.__create_device_table_query)
        logger.info('Device table created.', module=Module.DB)
        logger.info('Creating substance table...', module=Module.DB)
        cursor.execute(self.__create_substance_table_query)
        logger.info('Substance table created.', module=Module.DB)
        self.conn.commit()
        cursor.close()

    @staticmethod
    def __connect_db(db_path: str) -> sqlite3.Connection:
        """
        Connects to the sqlite3 database.
        :param db_path: path to the database.
        :return: the connection object.
        """
        logger.info(f'Connecting to database \"{db_path}\"...')
        conn: sqlite3.Connection = sqlite3.connect(db_path, check_same_thread=False)
        logger.info('DB Connected.', module=Module.DB)
        return conn

    def __init__(self, db_path: str = None):
        logger.info('Setting up database...', module=Module.DB)
        try:
            if not db_path:
                db_path: str = config.DB_PATH
            self.conn: sqlite3.Connection = self.__connect_db(db_path)
            self.DataRepository: DataRepository = DataRepository(self.conn)
            self.DeviceRepository: DeviceRepository = DeviceRepository(self.conn)
            self.SubstanceRepository: SubstanceRepository = SubstanceRepository(self.conn)
            self.__create_tables()
            self.SubstanceRepository.create_air_substance()
            self.DeviceRepository.clear_connections()
            logger.info('Database created successfully.', module=Module.DB)
        except Exception as e:
            logger.error('Error during db initialisation. Trace:', e, module=Module.DB)
            raise DBInitialisationException()
