import sys
from typing import Tuple, List

import serial
import serial.tools.list_ports

from exception.Exceptions import DriverNotInstalledException, DeviceNotConnectedException, PortInUseException, \
    PortNotUsedException, InfoFetchException
from log_handler.log_handler import Module, log as logger
if sys.platform.startswith("win"):
    from serial_com.win32_serial import win32api as serial_com
else:
    from serial_com.posix_serial import posix_serial_api as serial_com


class SerialComHandler:
    """
    Handles the serial communication interface with the SmellInspector.
    """

    @staticmethod
    def __get_com_port() -> str:
        """
        Get the com port used for the SmellInspector from win32.
        :return: the com port from win32 api.
        :raise DriverNotInstalledException: if the device is not found.
        """
        ports: List[str] = serial_com.find_com_ports_by_driver()
        if len(ports) > 1:
            logger.info('Multiple SmellInspector devices present. Using first unused one.', module=Module.SERIAL)
        return ports[0]

    @staticmethod
    def __open_serial_connection(serial_port: str) -> serial.Serial:
        """
        Try to open a channel to the provided serial port.
        :param serial_port: the serial port to open.
        :return: the open serial connection.
        :raise DeviceNotConnectedException: if the device is not connected.
        :raise PortInUseException: if the device is already connected.
        """
        try:
            if serial_com.check_port_is_used(port=serial_port):
                raise PortInUseException()
            _port = serial.Serial(
                port=serial_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
            )
            # Retry 3 times
            for i in range(3):
                if len(_port.readline()):
                    serial_com.allocate_port(port=serial_port)
                    return _port
                logger.error(f'Port \"{serial_port}\" connection failed, retrying {i + 1}/3...', module=Module.SERIAL)
            raise DriverNotInstalledException()
        except Exception:
            logger.error(f'Unable to connect to serial port \"{serial_port}\".', module=Module.SERIAL)
            raise DeviceNotConnectedException()

    def __get_serial_port(self, serial_port=None) -> serial.Serial:
        """
        Get the serial port used for communicating with the SmellInspector.
        :param serial_port: (Optional) The serial port to open.
        :return: The serial port object.
        :raise DriverNotInstalledException: if the com port is not found.
        """
        if serial_port is not None:
            logger.info(f'Serial port \"{serial_port}\" was provided. Testing connection...')
            try:
                return self.__open_serial_connection(serial_port=serial_port)
            except DeviceNotConnectedException:
                pass
        serial_port: str = self.__get_com_port()
        return self.__open_serial_connection(serial_port=serial_port)

    def write(self, command: str) -> Tuple[bool, str]:
        """
        Writes commands to the serial interface.
        :param command: the command to be written to the serial interface.
        :return: True if the command was processed successfully, False otherwise along with a frontend message.
        """
        valid_commands: List[str] = ['FAN0', 'FAN1', 'FAN2', 'FAN3', 'GET_INFO']
        if command not in valid_commands:
            return False, 'Invalid command provided.'
        try:
            self.__lock = True
            if 'GET_INFO' == command:
                result: Tuple[bool, str] = True, ';'.join(self.get_device_info())
            else:
                self.__port.write(bytes(f'{command}\n', 'ascii'))
                logger.debug(f'Wrote command \"{command}\" to interface.', module=Module.SERIAL)
                result: Tuple[bool, str] = True, f'\"{command}\" Setting applied.'
            self.__lock = False
            logger.debug(f'Command executed. Output: \"{result[1]}\"')
            return result
        except Exception as e:
            logger.error(f'Error writing command \"{command}\" to interface.', module=Module.SERIAL)
            return False, f'Error writing command. Trace: {e}'

    def flush(self) -> None:
        """
        Flushes the serial com. Used after device was reconnected.
        :return:
        """
        if not self.__connected:
            return
        try:
            self.__port.reset_input_buffer()
            self.__port.reset_output_buffer()
        except Exception as e:
            logger.error('Attempted to flush serial com, but was apparently not connected.', module=Module.SERIAL)
            logger.error('Ignored error trace:', e, module=Module.SERIAL)

    def read(self, lock_bypass: bool = False) -> str | None:
        """
        Return next line of serial data.
        :param lock_bypass: bypasses thread lock for reading during command execution.
        :return: the next line of serial data.
        """
        while self.__connected:
            if self.__lock and not lock_bypass:
                continue
            try:
                data = self.__port.readline()
                data = data.decode('ascii').strip()

                if not len(data):
                    continue
                logger.debug(f'[{self.__port.port}] Read data: \"{data}\".', module=Module.SERIAL)
                return data
            except Exception as e:
                logger.error('Error reading data. Trace:', e, module=Module.SERIAL)
        return None

    def get_device_info(self) -> List[str]:
        """
        Execute the GET_INFO and return its output.
        :return: The device info.
        :raise InfoFetchException: if the output is invalid.
        :raise DeviceNotConnectedException: if an error occurs during the read process.
        """
        if len(self.__device_metadata):
            return self.__device_metadata
        self.__lock = True
        self.__port.write(bytes('GET_INFO\n', 'ascii'))
        try:
            for _ in range(5):
                data: str = self.read(lock_bypass=True)
                data: List[str] = data.split(';')
                if len(data) > 10:
                    continue
                self.__lock = False
                self.__device_metadata = data
                return data
            self.__lock = False
            raise InfoFetchException()
        except Exception as e:
            logger.error('Error fetching device data. Trace:', e, module=Module.SERIAL)
            raise DeviceNotConnectedException()

    def get_port_name(self) -> str:
        """
        Gets the port used by the device.
        :return: The port being used.
        :raise PortNotInstalledException: if the device is currently disconnected.
        """
        if self.__port is not None:
            return str(self.__port.port)
        raise PortNotUsedException()

    def shutdown(self) -> None:
        """
        Shuts down the current connection (for instance on device disconnect).
        :return:
        :raise PortNotUsedException: if the device is already disconnected.
        """
        if self.__port is None:
            logger.error('Port was already closed.', module=Module.SERIAL)
            raise PortNotUsedException()
        self.__connected: bool = False
        name: str = self.get_port_name()
        serial_com.deallocate_port(name)
        self.__port.close()
        logger.info(f'Closed serial port \"{name}\".', module=Module.SERIAL)

    def __init__(self, serial_port: str = None):
        """
        Constructor.
        :param serial_port: (Optional) the serial port to open for multi-device support.
        """
        try:
            logger.info('Opening Serial Connection...', module=Module.SERIAL)
            self.__port: serial.Serial = self.__get_serial_port(serial_port=serial_port)
            self.__connected: bool = True
            self.__lock: bool = False
            self.__device_metadata: List[str] = []
            logger.info('Serial connection established.', module=Module.SERIAL)
        except DriverNotInstalledException:
            logger.error('Driver not installed. Terminating...', module=Module.SERIAL)
            raise DriverNotInstalledException()  # re-raise for frontend
