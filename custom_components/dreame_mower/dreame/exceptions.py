class DeviceException(Exception):
    """Exception wrapping any communication errors with the device."""


class DeviceUpdateFailedException(DeviceException):
    """ """


class DeviceAuthFailedException(DeviceException):
    """The cloud account rejected the stored credentials."""


class InvalidValueException(ValueError):
    """ """


class InvalidActionException(ValueError):
    """ """
