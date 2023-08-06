import pyvisa

from maui_rc.subsystems.panelsetup import PanelSetup
from maui_rc.subsystems.acquisition import Acquitision


class VirtualScope:
    """
    Class representing the oscilloscope. Initialize using the VISA address of the device (e.g. 'VICP::<IP shown on device>::INSTR')
    """

    def __init__(self, visa_address: str):
        # setup the VISA library
        self.__resource_manager = pyvisa.ResourceManager("@py")
        # connect to the scope
        self.__scope = self.__resource_manager.open_resource(visa_address)

        # set the device responses to not include a full header
        self.__scope.write("COMM_HEADER OFF")
        # set the log on the device to display full dialog and to
        # reset this decision on poweroff
        self.__scope.write("COMM_HELP FD,YES")

        # setup the subsystems
        self.panelsetup = PanelSetup(self.__scope)
        self.acquisition = Acquitision(self.__scope)

    def list_instruments():
        rm = pyvisa.ResourceManager("@py")
        print(rm.list_resources())

    def set_timeout(self, duration: int):
        """Set the timeout on queries to the device.

        Arguments:
        - `duration` -> timeout duration in milliseconds
        """

        # set the timeout variable
        self.__scope.timeout = duration

    def print_log(self, clear_log=True):
        """Print the log in the standard output.

        Arguments:
        - `clear_log` -> clear the log on the device once retrieved
        """

        # setup the command
        cmd = f"COMM_HELP_LOG?{' CLR' if clear_log else ''}"
        # run the command
        resp: str = self.__scope.query(cmd)

        # parse the log out of the query
        # first remove the first and last characters (those are quotations)
        log = resp.removeprefix('"').removesuffix('\n"\n').split("\n")
        for line in log:
            print(line)

    def command(self, cmd: str):
        self.__scope.write(cmd)

    def query(self, cmd: str) -> str:
        return self.__scope.query(cmd)
    
    def query_raw(self, cmd: str) -> bytes:
        self.__scope.write(cmd)
        return self.__scope.read_raw()