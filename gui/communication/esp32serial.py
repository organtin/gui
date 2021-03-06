"""
Library to interface with the ESP32
"""

from threading import Lock
import serial # pySerial


__all__ = ("ESP32Serial",)


class ESP32Serial:
    """
    Main class for interfacing with the ESP32 via a serial connection.
    """

    def __init__(self, port, **kwargs):
        """
        Contructor

        Opens a serial connection to the MVM ESP32

        arguments:
        - port           the port device (e.g. "/dev/ttyUSB0")

        named arguments:
        - any argument available for the serial.Serial pySerial class
        - baudrate       the preferred baudrate, default 115200
        - terminator     the line terminator, binary encoded, default
                         b'\n'
        """

        baudrate = kwargs["baudrate"] if "baudrate" in kwargs else 115200
        self.term = kwargs["terminator"] if "terminator" in kwargs else b'\n'
        self.connection = serial.Serial(port=port, baudrate=baudrate)
        self.lock = Lock()

    def __del__(self):
        """
        Destructor.

        Closes the connection.
        """

        with self.lock:
            self.connection.close()

    def set(self, name, value):
        """
        Set command wrapper

        arguments:
        - name           the parameter name as a string
        - value          the value to assign to the variable as any type
                         convertible to string

        returns: an "OK" string in case of success.
        """

        with self.lock:
            # I know about Python 3.7 magic string formatting capability
            # but I don't really remember now the version running on
            # Raspbian
            command = 'set ' + name + ' ' + str(value) + '\r\n'
            self.connection.write(command.encode())
            result = self.connection.read_until(terminator=self.term)
            return result.decode().strip()

    def get(self, name):
        """
        Get command wrapper

        arguments:
        - name           the parameter name as a string

        returns: the requested value
        """

        with self.lock:
            command = 'get ' + name + '\r\n'
            self.connection.write(command.encode())
            result = self.connection.read_until(terminator=self.term)
            return result.decode().strip()
