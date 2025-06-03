import json
from typing import Dict, Tuple, List

from flask_socketio import SocketIO
from database.db_handler import DatabaseHandler
from exception.Exceptions import DriverNotInstalledException, InvalidDataException, PortNotUsedException, \
    DeviceNotFoundException, InfoFetchException, DeviceNotConnectedException
from log_handler.log_handler import Logger, Module, get_instance
from middleware.serial_db_test_handler import TestHandler
from serial_com.serial_com_handler import SerialComHandler

logger: Logger = get_instance()


class MiddlewareConnectionHandler:
    """
    Handles all connected serial devices.
    """

    __device_not_connected_error: Tuple[str, int] = json.dumps({'error': 'Device is not connected!'}), 400

    def __get_substance_by_id(self, substance_id: str) -> Tuple[str, str]:
        """
        Get the substance details for a given substance id.
        :param substance_id: the given substance id.
        :return: the substance name and quantity.
        :raise InvalidDataException: if the given substance id is invalid.
        """
        if substance_id is None or not len(substance_id) or substance_id == '':
            raise InvalidDataException('Invalid substance id.')
        try:
            return self.__database.SubstanceRepository.get_substance_by_id(substance_id)
        except InvalidDataException as e:
            raise InvalidDataException(str(e))

    def __check_device_busy(self, device_nickname: str) -> bool:
        """
        Checks whether the device with the given nickname is already running a test.
        """
        for _, test_data in self.__test_threads.items():
            if test_data['device_nickname'] == device_nickname:
                return True
        return False

    def __start_test(self, test_name: str, device_nickname: str, socketio: SocketIO) -> bool:
        """
        Starts a new test.
        :param test_name: name of the test.
        :param device_nickname: nickname of the device.
        :param socketio: socketio instance.
        :return:
        """
        try:
            if self.__check_device_busy(device_nickname):
                logger.error(f'Attempted to start a test using device \"{device_nickname}\" '
                             f'but it is already running one.', module=Module.MIDDLE)
                return False
            mac_address = self.__connected_devices[device_nickname].get_device_info()[1]
            test_obj: TestHandler = TestHandler(self.__connected_devices[device_nickname], self.__database, test_name,
                                                mac_address, socketio)
            test_obj.start_test()
            test_data: Dict = {
                'device_nickname': device_nickname,
                'start_time': test_obj.get_test_start_time(),
                'test_obj': test_obj
            }
            self.__test_threads[test_name] = test_data
            return True
        except Exception as e:
            logger.error(f'Error starting test \"{test_name}\" for device \"{device_nickname}\". Trace:',
                         e, module=Module.MIDDLE)
            return False

    def __stop_test(self, test_name: str, device_nickname: str) -> bool:
        """
        Stops a running test.
        :param test_name: name of the test.
        :param device_nickname: nickname of the device.
        :return:
        """
        try:
            test_obj: TestHandler = self.__test_threads[test_name]['test_obj']
            test_obj.stop_test()
            del self.__test_threads[test_name]
            return True
        except Exception as e:
            logger.error(f'Error stopping test \"{test_name}\" for device \"{device_nickname}\". Trace:',
                         e, module=Module.MIDDLE)
            return False

    @staticmethod
    def get_serial_ports() -> Tuple[str, int]:
        """
        Get a list of all serial ports available for device connection.
        :return: a list of free serial COM ports as a json list and a http response code.
        """
        try:
            from serial_com import win32_serial
            from serial_com.win32_serial import Win32API
            serial: Win32API = win32_serial.get_instance()
            ports: List[str] = serial.find_com_ports_by_driver()
            return json.dumps({
                'ports': ports
            }), 200
        except DriverNotInstalledException:
            return json.dumps({'error': 'No devices found. Please check installation guide.'}), 400
        except Exception as e:
            logger.error('Error fetching serial ports. Trace:', e, module=Module.MIDDLE)
            return json.dumps({'error': 'Error fetching devices. Try again.'}), 400

    def get_substances(self) -> Tuple[str, int]:
        """
        Get a list of all available substances.
        :return: a list of all available substances as json and a http response code.
        """
        return json.dumps(self.__database.SubstanceRepository.get_substances()), 200

    def add_substance(self, substance_name: str, quantity: str) -> Tuple[str, int]:
        """
        Adds a new substance.
        :param substance_name: name of the substance.
        :param quantity: quantity of the substance.
        :return: a success/error message and a http response code.
        """
        try:
            self.__database.SubstanceRepository.add_substance(substance_name, quantity)
            return json.dumps({'success': True}), 200
        except Exception as e:
            return json.dumps({'error': str(e)}), 400

    def update_substance(self, substance_id: str, substance_name: str, quantity: str) -> Tuple[str, int]:
        """
        Updates a substance.
        :param substance_id: substance id.
        :param substance_name: new name for the substance.
        :param quantity: new quantity for the substance.
        :return: a success/error message and a http response code.
        """
        try:
            self.__database.SubstanceRepository.update_substance(substance_id, substance_name, quantity)
            return json.dumps({'success': True}), 200
        except Exception as e:
            return json.dumps({'error': str(e)}), 400

    def delete_substance(self, substance_id: str) -> Tuple[str, int]:
        """
        Deletes a substance.
        :param substance_id: id of the substance.
        :return: a success/error message and a http response code.
        """
        try:
            self.__database.SubstanceRepository.delete_substance(substance_id)
            return json.dumps({'success': True}), 200
        except Exception as e:
            return json.dumps({'error': str(e)}), 400

    def get_all_devices(self) -> Tuple[str, int]:
        """
        Return a list of all devices.
        :return: a list of all devices, regardless of state, in json format and a http response code.
        """
        return json.dumps(self.__database.DeviceRepository.get_all_devices()), 200

    def get_connected_devices(self) -> Tuple[str, int]:
        """
        Return a list of connected devices.
        :return: a list of all connected devices in json format and a http response code.
        """
        try:
            return json.dumps(self.__database.DeviceRepository.get_connected_devices()), 200
        except InvalidDataException:
            return json.dumps({'error': 'Error fetching devices.'}), 400

    def get_disconnected_devices(self) -> Tuple[str, int]:
        """
        Return a list of disconnected devices.
        :return: a list of all disconnected devices in json format and a http response code.
        """
        try:
            return json.dumps(self.__database.DeviceRepository.get_disconnected_devices()), 200
        except InvalidDataException:
            return json.dumps({'error': 'Error fetching devices.'}), 400

    def get_free_devices(self) -> Tuple[str, int]:
        """
        Return a list of devices not running tests.
        :return: a list of devices not currently running tests.
        """
        try:
            free_devices: List[List[str]] = []
            devices: List[List[str]] = self.__database.DeviceRepository.get_connected_devices()
            for i, device in enumerate(devices):
                _, nickname, _, _, _, _, _ = device
                if self.__check_device_busy(nickname):
                    continue
                free_devices.append(devices[i])
            return json.dumps(free_devices), 200
        except Exception as e:
            return json.dumps({'error': str(e)}), 400

    def update_test_substance(self, test_name: str, substance_id: str) -> Tuple[str, int]:
        """
        Update the substance being tested.
        :param test_name: test name.
        :param substance_id: the id of the new substance.
        :return: json response message and http status code.
        """
        if test_name not in self.__test_threads:
            return json.dumps({'error': 'Device is not currently running a test.'}), 400
        try:
            substance_name, quantity = self.__get_substance_by_id(substance_id)
        except InvalidDataException as e:
            return json.dumps({'error': str(e)}), 400
        test_obj: TestHandler = self.__test_threads[test_name]['test_obj']
        test_obj.update_substance_id(substance_id)
        return json.dumps({
            'substance_id': test_obj.get_substance_id(),
            'substance': substance_name,
            'quantity': quantity,
            'substance_start_time': test_obj.get_substance_start_time().strftime('%Y-%m-%d %H:%M:%S'),
        }), 200

    def get_test_substance(self, test_name: str) -> Tuple[str, int]:
        """
        Get the substance currently being tested.
        :param test_name: the test name.
        :return: the substance and a http response code.
        """
        if test_name not in self.__test_threads:
            return json.dumps({'error': 'Device is not currently running a test.'}), 400
        test_obj: TestHandler = self.__test_threads[test_name]['test_obj']
        substance_id: str = test_obj.get_substance_id()
        try:
            substance_name, quantity = self.__get_substance_by_id(substance_id)
        except InvalidDataException as e:
            return json.dumps({'error': str(e)}), 400
        return json.dumps({
            'substance_id': substance_id,
            'substance': substance_name,
            'quantity': quantity,
            'substance_start_time': test_obj.get_substance_start_time().strftime('%Y-%m-%d %H:%M:%S'),
        }), 200

    def start_stop_test(self, test_name: str, device_nickname: str, socketio: SocketIO) -> Tuple[str, int]:
        """
        Starts/Stops the test with the given name.
        :param test_name: name of the test.
        :param device_nickname: nickname of the device.
        :param socketio: socketio instance.
        :return: The updated test message as json and a http response code.
        """
        if device_nickname not in self.__connected_devices:
            return self.__device_not_connected_error
        if test_name in self.__test_threads:
            if device_nickname != self.__test_threads[test_name]['device_nickname']:
                return json.dumps({'error': 'Wrong device name supplied!'}), 400
            if not self.__stop_test(test_name, device_nickname):
                return json.dumps({'error': 'Error stopping test, see server logs!'}), 400
            return json.dumps({'info': f'Test \"{test_name}\" was stopped!'}), 200
        if not len(test_name):
            return json.dumps({'error': 'Test name cannot be empty!'}), 400
        if test_name in self.__database.DataRepository.get_test_names():
            return json.dumps({'error': 'Test name was already used! Pick a new one!'}), 400
        if not self.__start_test(test_name, device_nickname, socketio):
            return json.dumps({'error': 'Error starting test, see server logs!'}), 400
        return json.dumps({'info': f'Test \"{test_name}\" started!'}), 200

    def get_active_tests(self) -> Tuple[str, int]:
        """
        Get all active tests along with their devices and names.
        :return: the data as a json string and a response code.
        """
        js_data = []
        try:
            for test_name, test_data in self.__test_threads.items():
                js_data.append({
                    'test_name': test_name,
                    'device_nickname': test_data['device_nickname']
                })
            return json.dumps(js_data), 200
        except Exception as e:
            logger.error('Error serialising test data. Trace:', e, module=Module.MIDDLE)
            return json.dumps({'error': 'Error occurred fetching data. See server logs.'}), 400

    def register_device(
            self,
            device_nickname: str,
            com_port: str = None
    ) -> Tuple[str, int]:
        """
        Register a new SmellInspector device.
        :param device_nickname: nickname for the device.
        :param com_port: (Optional) Port the device is connected to.
        :return: a json response and http response code.
        """
        if device_nickname in self.__connected_devices.keys():
            return json.dumps({'error': f'Device with name \"{device_nickname}\" already exists.'}), 400
        if com_port is not None:
            for _, device in self.__connected_devices.items():
                if device.get_port_name() == com_port:
                    return json.dumps({'error': f'Port \"{com_port}\" is already connected.'}), 400
        try:
            device: SerialComHandler = SerialComHandler(serial_port=com_port)
            software_version, mac_address = device.get_device_info()[:2]
            port: str = device.get_port_name()
            self.__database.DeviceRepository.persist_device(
                device_name=device_nickname,
                software_version=software_version,
                mac_address=mac_address,
                socket=port
            )
            self.__connected_devices[device_nickname] = device
            return json.dumps({'info': 'Device registered successfully.', 'details': device.get_device_info()}), 200
        except DriverNotInstalledException:
            return json.dumps({'error': 'Error registering device. Serial COM error.'}), 400
        except InvalidDataException:
            return json.dumps({'error': 'Error registering device. DB Error occurred.'}), 400

    def de_register_device(
            self,
            device_nickname: str
    ) -> Tuple[str, int]:
        """
        Unregisters a given device.
        :param device_nickname: the device name.
        :return: a json string and http response code.
        """
        if device_nickname not in self.__connected_devices:
            return self.__device_not_connected_error
        if self.__check_device_busy(device_nickname):
            return json.dumps({'error': 'Device busy! Stop test and re-attempt disconnecting.'}), 400
        try:
            device: SerialComHandler = self.__connected_devices[device_nickname]
            _, mac_address = device.get_device_info()[:2]
            device.shutdown()
            self.__database.DeviceRepository.update_device_state_by_mac_address(mac_address, False, '')
            del self.__connected_devices[device_nickname]
            return json.dumps({'info': f'Device with name \"{device_nickname}\" was de-registered.'}), 200
        except PortNotUsedException:
            return json.dumps({'error': f'No ports found for device \"{device_nickname}\".'}), 400
        except DeviceNotFoundException | InfoFetchException | DeviceNotConnectedException:
            return json.dumps({'error': f"Device with name \"{device_nickname}\" couldn't be found."}), 400

    def __init__(self):
        try:
            logger.info('Middleware boot-up...', module=Module.MIDDLE)
            self.__database: DatabaseHandler = DatabaseHandler()
            self.__connected_devices: Dict[str, SerialComHandler] = {}
            self.__test_threads: Dict[str, Dict] = {}
            logger.info('Middleware booted.', module=Module.MIDDLE)
        except Exception as e:
            logger.error('Error during boot. Terminating. Trace:', e, module=Module.MIDDLE)
            exit(-1)
