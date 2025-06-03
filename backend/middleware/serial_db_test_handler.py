import threading
from datetime import datetime
from typing import List, Tuple, Optional
from flask_socketio import SocketIO

from database.db_handler import DatabaseHandler
from log_handler.log_handler import Logger, Module, get_instance
from serial_com.serial_com_handler import SerialComHandler

logger: Logger = get_instance()


class TestHandler:
    """
    Handles an ongoing test for a given SmellInspector device.
    """

    @staticmethod
    def __split_data(data: str) -> Tuple[List[str], str, str] | None:
        """
        Splits the serial data into chunks required for database.
        :param data: The serial data as a string.
        :return: The data chunks.
        """
        data = data.split(';')
        if len(data) != 67:
            return None
        _, data, temperature, humidity = data[0], data[1:65], data[-2], data[-1]
        return data, temperature, humidity

    def __serial_to_db_thread(self):
        """
        Reads serial data and writes it to the database.
        Also emits a socketio event for the frontend.
        """
        errors: int = 0
        self.__serial_com.flush()
        while self.__running:
            try:
                data = self.__serial_com.read()
                data = self.__split_data(data)
                if data is None:
                    continue
                data, temperature, humidity = data
                now = datetime.now()
                self.__database.DataRepository.persist_data(
                    self.__test_name,
                    self.__mac_address,
                    self.__substance_id,
                    now,
                    data,
                    temperature,
                    humidity
                )
                json_data = {
                    'test name': self.__test_name,
                    'mac address': self.__mac_address,
                    'substance': self.__substance_id,
                    'start time': now.strftime('%Y-%m-%d %H:%M:%S'),
                    'data': ';'.join(data),
                    'temperature': temperature,
                    'humidity': humidity
                }
                self.__socketio.emit('data_collected', json_data)
                logger.debug('Cached data:', json_data, module=Module.TEST)
            except Exception as e:
                logger.error('Error during data collection. Trace:', e, module=Module.TEST)
                errors += 1
                if errors > 3:
                    logger.error('Error during 3 executions. Terminating...', module=Module.TEST)
                    self.__running = False


    def update_substance_id(self, substance_id: str) -> None:
        """
        Updates the substance currently being tested.
        :param substance_id: the new substance.
        :return:
        """
        self.__substance_id: str = substance_id
        logger.info('Updated substance to', substance_id, module=Module.TEST)

    def get_substance_id(self) -> str:
        """
        Gets the substance currently being tested.
        :return: the substance.
        """
        return self.__substance_id

    def get_test_start_time(self) -> datetime:
        """
        Gets the time at which the test was started.
        :return: the time at which the test was started.
        """
        return self.__test_start_time

    def get_substance_start_time(self) -> datetime:
        """
        Gets the time at which the substance was changed.
        :return: the time at which the substance was changed.
        """
        return self.__substance_start_time

    def stop_test(self):
        """
        Stops the running test instance.
        :return:
        """
        if not self.__running:
            logger.error('Test is not running, ignoring stop command.', module=Module.TEST)
            return
        if self.__test_thread is None:
            logger.error('Test thread is none, ignoring.', module=Module.TEST)
            return
        self.__running = False
        self.__test_thread.join()
        logger.info(f'Stopped test \"{self.__test_name}\"', module=Module.TEST)

    def start_test(self):
        """
        Starts the test instance.
        :return:
        """
        if self.__running or self.__test_thread is not None:
            logger.error(f'Test \"{self.__test_name}\" is already running, skipping.')
            return
        now: datetime = datetime.now()
        self.__substance_start_time = now
        self.__test_start_time = now
        self.__running = True
        self.__test_thread = threading.Thread(target=self.__serial_to_db_thread)
        self.__test_thread.start()

    def __init__(self, serial_com: SerialComHandler, database: DatabaseHandler, test_name: str, mac_address: str,
                 socketio: SocketIO):
        """
        Constructor.
        :param serial_com: serial com object for reading serial data.
        :param database: db connection for persisting data.
        :param test_name: the name of the test.
        :param mac_address: the MAC address of the device.
        :param socketio: the flask socketio context.
        """
        self.__running = False
        self.__serial_com: SerialComHandler = serial_com
        self.__database: DatabaseHandler = database
        self.__test_thread: Optional[threading.Thread] = None
        self.__test_name: str = test_name
        self.__substance_id: str = '1'  # Air
        self.__mac_address: str = mac_address
        self.__substance_start_time: Optional[datetime] = None
        self.__test_start_time: Optional[datetime] = None
        self.__socketio: SocketIO = socketio
