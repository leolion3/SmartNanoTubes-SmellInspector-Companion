#!/usr/bin/env python3
from typing import List
from serial.tools import list_ports

from exception.Exceptions import DriverNotInstalledException, PortNotUsedException, PortInUseException
from log_handler.log_handler import Module, log as logger


class PosixSerialAPI:
    """
    (Singleton) Handles macOS/Linux functionality for discovering CP210x serial ports.

    Detection strategy:
      - Prefer VID match (Silicon Labs: 0x10C4).
      - Fall back to manufacturer/description/name containing 'Silicon Labs' or 'CP210'.
    This works on both macOS (/dev/cu.* or /dev/tty.*) and Linux (/dev/ttyUSB*).
    """

    # Silicon Labs USB Vendor ID
    SILABS_VID = 0x10C4

    def find_com_ports_by_driver(self, driver_name: str = "CP210x") -> List[str]:
        """
        Get serial ports backed by the CP210x driver on macOS/Linux.

        :param driver_name: (Optional) Name hint for the driver (default: "CP210x").
        :return: list of device paths (e.g., '/dev/cu.SLAB_USBtoUART', '/dev/ttyUSB0', ...)
        :raise DriverNotInstalledException: if no matching ports are found.
        """
        logger.info(f'Querying POSIX serial ports for driver "{driver_name}"...', module=Module.POSIX)

        matches: List[str] = []
        try:
            for p in list_ports.comports():
                # Gather safe, lowercased strings for matching
                desc = (p.description or "").lower()
                mfg = (p.manufacturer or "").lower()
                name = (p.name or "").lower()
                drv_hint = driver_name.lower()

                is_silabs_vid = (p.vid == self.SILABS_VID)
                looks_like_cp210x = (
                        drv_hint in desc
                        or "cp210" in desc
                        or "cp210" in name
                        or "silicon labs" in mfg
                        or "slab" in (p.device or "").lower()
                )

                if is_silabs_vid or looks_like_cp210x:
                    dev = str(p.device)
                    if dev in self.__used_ports:
                        logger.info(f'Skipping port "{dev}" because it is already being used.', module=Module.POSIX)
                        continue
                    logger.info(
                        f'Device found: "{dev}" (vid={p.vid}, pid={p.pid}, mfg="{p.manufacturer}", desc="{p.description}")',
                        module=Module.POSIX)
                    matches.append(dev)

            logger.debug('Found ports:', matches, module=Module.POSIX)
        except Exception as e:
            logger.error('Unable to query POSIX serial ports. Trace:', e, module=Module.POSIX)
        if matches:
            return matches
        raise DriverNotInstalledException()

    def allocate_port(self, port: str) -> None:
        """
        Allocates (blocks) a new port.
        :param port: the port to block.
        :raise PortInUseException: if the port is already in use.
        """
        if port in self.__used_ports:
            logger.error(f'Attempted to block port "{port}", but it is already in use.', module=Module.POSIX)
            raise PortInUseException()
        self.__used_ports.append(port)
        logger.info(f'Added port "{port}" to allocated ports.', module=Module.POSIX)

    def deallocate_port(self, port: str) -> None:
        """
        Deallocates (unblocks) the given port.
        :param port: the port to unblock.
        :raise PortNotUsedException: if the port is not in use.
        """
        if port not in self.__used_ports:
            logger.error(f'Attempted to deallocate port "{port}", but it is not in use.', module=Module.POSIX)
            raise PortNotUsedException()
        self.__used_ports.remove(port)
        logger.info(f'Deallocated port "{port}".', module=Module.POSIX)

    def check_port_is_used(self, port: str) -> bool:
        """
        Checks if the given port is already being used.
        :param port: the port to check.
        :return: True if the port is already being used, False otherwise.
        """
        return port in self.__used_ports

    def __init__(self):
        self.__used_ports: List[str] = []


posix_serial_api: PosixSerialAPI = PosixSerialAPI()
