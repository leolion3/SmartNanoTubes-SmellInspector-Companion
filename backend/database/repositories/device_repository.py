import sqlite3
from typing import List

from database.repositories.abstract_repository import AbstractRepository
from exception.Exceptions import InvalidDataException, DeviceNotFoundException
from log_handler.log_handler import Module, Logger, get_instance

logger: Logger = get_instance()


class DeviceRepository(AbstractRepository):
    """
    Handles SmellInspector devices operations.
    """

    __persist_device_query: str = 'INSERT INTO Device VALUES (NULL, ?, ?, ?, ?, ?, TRUE);'
    __get_all_devices_query: str = 'SELECT * FROM Device;'
    __get_device_by_mac_address: str = 'SELECT * FROM Device WHERE MAC_ADDRESS=?;'
    __update_device_by_address_query: str = ('UPDATE Device SET DEVICE_NAME=?, SOCKET=?, CONNECTED=? '
                                             'WHERE MAC_ADDRESS=?;')
    __update_device_state_by_address_query: str = 'UPDATE Device SET SOCKET=?, CONNECTED=? WHERE MAC_ADDRESS=?;'
    __delete_device_query: str = 'DELETE FROM Device WHERE MAC_ADDRESS=?;'
    __delete_data_from_device_query: str = 'DELETE FROM Data WHERE MAC_ADDRESS=?;'
    __get_connected_devices_query: str = 'SELECT * FROM Device WHERE CONNECTED == true;'
    __get_disconnected_devices_query: str = 'SELECT * FROM Device WHERE CONNECTED == false;'

    def get_connected_devices(self) -> List[List]:
        """
        Get all connected devices.
        :return: a list of connected devices.
        :raise InvalidDataException: on error.
        """
        try:
            cursor: sqlite3.Cursor = self.conn.cursor()
            data = cursor.execute(self.__get_connected_devices_query).fetchall()
            cursor.close()
            return data
        except Exception as e:
            logger.error('Error fetching available devices. Trace:', e, module=Module.DB)
            raise InvalidDataException()

    def get_disconnected_devices(self) -> List[List]:
        """
        Get all disconnected devices.
        :return: a list of disconnected devices.
        :raise InvalidDataException: on error.
        """
        try:
            cursor: sqlite3.Cursor = self.conn.cursor()
            data = cursor.execute(self.__get_disconnected_devices_query).fetchall()
            cursor.close()
            return data
        except Exception as e:
            logger.error('Error fetching unavailable devices. Trace:', e, module=Module.DB)
            raise InvalidDataException()

    def delete_data_from_device(self, mac_address: str) -> None:
        """
        Deletes all data given a device's MAC address.
        :param mac_address: the device's MAC address.
        :return:
        :raise DeviceNotFoundException: if the device is not found.
        """
        try:
            self.execute_commit_update_query(self.__delete_data_from_device_query, [mac_address])
        except Exception as e:
            logger.error(f'Error deleting device \"{mac_address}\" data. Trace:', e, module=Module.DB)
            raise DeviceNotFoundException()

    def delete_device(self, mac_address: str) -> None:
        """
        Delete a device along with its recorded data.
        :param mac_address: mac address of the device to delete.
        :return:
        :raise DeviceNotFoundException: if the device is not found.
        """
        try:
            self.execute_commit_update_query(self.__delete_device_query, [mac_address])
        except Exception as e:
            logger.error(f'Error deleting device \"{mac_address}\". Trace:', e, module=Module.DB)
            raise DeviceNotFoundException()

    def update_device_state_by_mac_address(
            self,
            mac_address: str,
            connected: bool,
            socket: str
    ) -> None:
        """
        Updates a device's state and  given its mac address.
        :param mac_address: the device's mac address.
        :param connected: whether the device is connected.
        :param socket: the socket on which the device is connected.
        :return:
        :raise DeviceNotFoundException: if the device is not found.
        """
        try:
            self.execute_commit_update_query(self.__update_device_state_by_address_query,
                                             [socket, connected, mac_address])
        except Exception as e:
            logger.error(f'Error updating device with mac address \"{mac_address}\". Trace:', e, module=Module.DB)
            raise DeviceNotFoundException()

    def update_device_by_mac_address(
            self,
            nickname: str,
            mac_address: str,
            connected: bool,
            socket: str
    ) -> None:
        """
        Updates a device's state and  given its mac address.
        :param nickname: the device's nickname.
        :param mac_address: the device's mac address.
        :param connected: whether the device is connected.
        :param socket: the socket on which the device is connected.
        :return:
        :raise DeviceNotFoundException: if the device is not found.
        """
        try:
            self.execute_commit_update_query(self.__update_device_by_address_query,
                                             [nickname, socket, connected, mac_address])
        except Exception as e:
            logger.error(f'Error updating device with mac address \"{mac_address}\". Trace:', e, module=Module.DB)
            raise DeviceNotFoundException()

    def get_device_by_mac_address(self, mac_address: str) -> List:
        """
        Get a device by its mac address.
        :param mac_address: the mac address.
        :return: The device's values.
        :raise DeviceNotFoundException: if the device doesn't exist.
        """
        cursor: sqlite3.Cursor = self.execute_fetch_query(self.__get_device_by_mac_address, [mac_address])
        devices: List[List] = cursor.fetchall()
        cursor.close()
        if len(devices) == 0:
            raise DeviceNotFoundException()
        return devices[0]

    def get_all_devices(self) -> List[List[str]]:
        """
        Get all SmellInspector devices from the database.
        :return: a list of all SmellInspector devices.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        data = cursor.execute(self.__get_all_devices_query).fetchall()
        cursor.close()
        return data

    def persist_device(
            self,
            device_name: str,
            mac_address: str,
            software_version: str,
            socket: str
    ) -> None:
        """
        Persist a new (connected) SmellInspector device to the database.
        :param device_name: the device's nickname.
        :param mac_address: the device's MAC address.
        :param software_version: the device's software version.
        :param socket: the socket the device is currently attached to.
        :return:
        :raise InvalidDataException: if the data provided is formatted incorrectly.
        """
        try:
            self.get_device_by_mac_address(mac_address)
            self.update_device_by_mac_address(device_name, mac_address, True, socket)
            return
        except DeviceNotFoundException:
            pass
        self.execute_commit_update_query(self.__persist_device_query,
                                         [device_name, mac_address, software_version, '3', socket])

    def clear_connections(self) -> None:
        """
        Clear connections on reboot.
        """
        logger.info('Resetting devices connection status...', module=Module.DB)
        devices: List = self.get_all_devices()
        for device in devices:
            _, _, mac_address, _, _, _, _ = device
            try:
                self.update_device_state_by_mac_address(mac_address, False, '')
            except DeviceNotFoundException:
                logger.error(f'Error resetting device \"{mac_address}\".', module=Module.DB)

    def __init__(self, conn: sqlite3.Connection):
        """
        Constructor.
        :param conn: Database connection object.
        """
        super().__init__(conn)
        self.conn: sqlite3.Connection = conn
