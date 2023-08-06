import pyvisa
from maui_rc.datatypes import *
from maui_rc.subsystems.wavedata import WaveformData
import numpy as np


class Acquitision:
    """Class that groups functions relating to acquisition."""

    def __init__(self, scope: pyvisa.Resource):
        self.__scope = scope

    def arm_acquisition(self):
        """Changes the acquisition state from stopped to single."""
        self.__scope.write("ARM_ACQUISITION")

    def enable_sequence(self, number_segments: int, max_size: int):
        """Turn on sequencing with the specified parameters.

        Arguments:
        - `number_segments` -> the number of segments in one acquisition
        - `max_size` -> the maximum number of points in a segment
        """

        # setup and run the command
        cmd = "SEQUENCE ON,{},{:e}".format(int(number_segments), int(number_segments))
        self.__scope.write(cmd)

    def disable_sequence(self):
        """Turn off sequencing in the acquisition."""

        # just run an off command
        self.__scope.write("SEQUENCE OFF")

    def stop_acquisition(self):
        """Immediatly stops signal acquisition."""

        # run the command
        self.__scope.write("STOP")

    def wait_acquisition(self):
        """Prevents new analysis until the current one is complete."""

        # run the command
        self.__scope.write("WAIT")

    def set_time_div(self, value: float):
        """Modifies the timebase setting.

        Arguments:
        - `value` -> the number of seconds per division
        """

        # setup the command and then run it
        cmd = "TIME_DIV {:e}".format(float(value))
        self.__scope.write(cmd)

    def get_time_div(self) -> float:
        """Get the current timebase setting."""

        # query the device
        time_div = self.__scope.query("TIME_DIV?").strip()
        return float(time_div)

    def set_volt_div(self, value: float):
        """Sets the vertical sensitivity.
        Arguments:
        - `value` -> the volts in a division
        """

        # setup the command and then run it
        cmd = "VOLT_DIV {:e}".format(float(value))
        self.__scope.write(cmd)

    def get_volt_div(self) -> float:
        """Gets the vertical sensitivity"""

        # query the device
        volt_div = self.__scope.query("VOLT_DIV?").strip()
        return float(volt_div)

    def set_trigger_delay(self, delay: int):
        """Sets the time at which the trigger is to occur.

        Arguments:
        - `delay`
            - negative delay: (0 to -10000) x Time/div
            - positive delay: (0 to +10) x Time/div
        """

        # Validate the argument
        if delay > 10 or delay < -10000:
            raise Exception("trigger delay must be between -10000 and 10 inclusively")

        # setup and run the command
        cmd = f"TRIG_DELAY {delay}"
        self.__scope.write(cmd)

    def get_trigger_delay(self) -> int:
        """Gets the time at which the trigger is to occur"""

        # query and parse the response
        resp: str = self.__scope.query("TRIG_DELAY?").removesuffix("\n")
        delay = int(resp)

        return delay

    def set_trigger_level(self, level: float, trigger_source: Channel = None):
        """
        Adjusts the trigger level of the specified trigger source. If no trigger source is specified, the level is adjusted for all sources.

        Arguments:
        - `level` -> level in volts
        - `trigger_source` -> trigger source, set to `None` to select all sources
        """

        # setup the command
        if trigger_source is not None:
            cmd = f"TRIG_LEVEL {float(level)}V"
        else:
            cmd = f"{Channel(trigger_source)}:TRIG_LEVEL {float(level)}V"

        # run the command
        self.__scope.write(cmd)

    def get_trigger_level(self, trigger_source: Channel):
        """Gets the trigger level of the specified trigger source.

        Arguments:
        - `trigger_source` -> specified trigger source
        """

        # setup the query
        cmd = f"{Channel(trigger_source)}TRIG_LEVEL?"
        # run and parse the query
        level = self.__scope.query(cmd).removesuffix("\n")
        return level

    def trigger_normal(self):
        """Set the trigger mode to normal."""
        self.__scope.write("TRIG_MODE NORMAL")

    def trigger_auto(self):
        """Set the trigger mode to auto."""
        self.__scope.write("TRIG_MODE AUTO")

    def trigger_single(self):
        """Set the trigger mode to single. This is equivalent to manually pressing to get a single acquisition."""
        self.__scope.write("TRIG_MODE SINGLE")

    def trigger_stop(self):
        """Set the trigger mode to stop. Stops acquisitions."""
        self.__scope.write("TRIG_MODE STOP")

    def get_trigger_mode(self) -> TriggerMode:
        """Get the current specified trigger mode."""

        # query and parse the response
        resp: str = self.__scope.query("TRIG_MODE?").removesuffix("\n")
        mode = TriggerMode(resp)
        return mode

    def get_waveform_data(self, channel: Channel) -> tuple[np.array, np.array]:
        """Extract the waveform from the scope and parse it."""

        # Transfer the data blocks over
        self.__scope.write(f"{channel}:WF? DESC")
        desc = self.__scope.read_raw()
        self.__scope.write(f"{channel}:WF? TEXT")
        text = self.__scope.read_raw()
        self.__scope.write(f"{channel}:WF? TIME")
        time = self.__scope.read_raw()
        self.__scope.write(f"{channel}:WF? DAT1")
        dat1 = self.__scope.read_raw()
        self.__scope.write(f"{channel}:WF? DAT2")
        dat2 = self.__scope.read_raw()

        # Parse it into waveform data
        data = WaveformData(desc, text, time, dat1, dat2)

        # Return a tuple of arrays (x,y)
        return (data.data_x, data.data_y)
