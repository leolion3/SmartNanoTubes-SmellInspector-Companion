from typing import List, Optional
import pythoncom
import win32com.client

from exception.Exceptions import DriverNotInstalledException, PortNotUsedException, PortInUseException
from log_handler.log_handler import Module, Logger, get_instance

logger: Logger = get_instance()


class Win32API:
    """
    (Singleton) Handles win32 api functionality for querying com ports.
    """

    def find_com_ports_by_driver(self, driver_name: str = "CP210x") -> List[str]:
        """
        Get com ports used for the SmellInspector(s) from win32 api.
        :param driver_name: (Optional) Name of the driver used for the serial device, default: "CP210x".
        :return: the COM ports currently available.
        :raise DriverNotInstalledException: if no COM ports are found.
        """
        pythoncom.CoInitialize()
        com_ports = []
        try:
            logger.info(f'Querying Win32 api for driver \"{driver_name}\"...', module=Module.WIN32)
            wmi = win32com.client.GetObject("winmgmts:")
            query = "SELECT * FROM Win32_SerialPort"
            serial_ports = wmi.ExecQuery(query)

            for serial_port in serial_ports:
                if driver_name.lower() in serial_port.Name.lower():
                    com = str(serial_port.DeviceID)
                    if com in self.__used_ports:
                        logger.info(f'Skipping port \"{com}\" because it is already being used.', module=Module.WIN32)
                        continue
                    logger.info(f'Device found: \"{com}\"', module=Module.WIN32)
                    com_ports.append(com)
            logger.debug('Found ports:', com_ports, module=Module.WIN32)
        except Exception as e:
            logger.error('Unable to query win32 api. Trace:', e, module=Module.WIN32)
        finally:
            pythoncom.CoUninitialize()
        if len(com_ports):
            return com_ports

        raise DriverNotInstalledException()

    def allocate_port(self, port: str) -> None:
        """
        Allocates (blocks) a new port.
        :param port: the port to block.
        :return:
        :raise PortInUseException: if the port is already in use.
        """
        if port in self.__used_ports:
            logger.error(f'Attempted to block port \"{port}\", but it is already in use.', module=Module.WIN32)
            raise PortInUseException()
        self.__used_ports.append(port)
        logger.info(f'Added port \"{port}\" to allocated ports.', module=Module.WIN32)

    def deallocate_port(self, port: str) -> None:
        """
        Deallocates (unblocks) the given port.
        :param port: the port to unblock.
        :return:
        :raise PortNotUsedException: if the port is not in use.
        """
        if port not in self.__used_ports:
            logger.error(f'Attempted to deallocate port \"{port}\", but it is not in use.', module=Module.WIN32)
            raise PortNotUsedException()
        self.__used_ports.remove(port)
        logger.info(f'Deallocated port \"{port}\".', module=Module.WIN32)

    def check_port_is_used(self, port: str) -> bool:
        """
        Checks if the given port is already being used.
        :param port: the port to check.
        :return: True if the port is already being used, False otherwise.
        """
        return self.__used_ports.__contains__(port)

    def __init__(self):
        self.__used_ports: List[str] = []


_win32api: Optional[Win32API] = None


def get_instance() -> Win32API:
    """
    Win32API Handler singleton instance.
    :return: The singleton instance.
    """
    global _win32api
    if _win32api is None:
        _win32api = Win32API()
    return _win32api
