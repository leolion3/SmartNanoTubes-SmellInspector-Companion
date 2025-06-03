class DriverNotInstalledException(Exception):
    pass


class DeviceNotConnectedException(Exception):
    pass


class DeviceNotFoundException(Exception):
    pass


class InfoFetchException(Exception):
    pass


class PortInUseException(Exception):
    pass


class PortNotUsedException(Exception):
    pass


class DBInitialisationException(Exception):
    pass


class InvalidDataException(Exception):
    pass
