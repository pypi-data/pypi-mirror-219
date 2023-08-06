import pyvisa

class Waveform:
    """Class used to extract the waveform and parse the binary data into human and program readable data formats."""

    def __init__(self, scope: pyvisa.Resource):
        self.__scope = scope

    # NOTE: I don't want to implement this function because it leads to very involved parsing to do on the data
    #       and I do not have the time nor the reason to use this function.
    #
    # def setup_waveform(
    #     self,
    #     sparsing: int = 0,
    #     number_of_points: int = 0,
    #     first_point: int = 0,
    #     segment_number: int = None,
    # ):
    #     """Setup how the waveform is transfered from the device.

    #     Arguments:
    #     - `sparsing` -> Interval between data points
    #         - `0` = sends all data points
    #         - `1` = sends all data points
    #         - `4` = sends every 4th data point
    #         - `n` = sends every nth data point
    #     - `number_of_points` -> How many points should be transmitted
    #         - `0` = sends all data points
    #         - `1` = sends 1 data point
    #         - `9` = sends a maximum of 50 data points
    #         - `n` = sends a maximum of n data points
    #     - `first_point` -> Defines the index of the first data point to start sending from
    #         - `0` = starts sending from the first point
    #         - `1` = starts sending form the second point
    #         - `n` = starts sending from the (n+1)th point
    #     - `segment_number` -> Defines which segment to transfer if in sequence acquisition mode
    #     """

    #     # check if the segment_number is set
    #     if segment_number is not None:
    #         # get the setup of the sequence
    #         sequence_setup = self.__scope.query("SEQUENCE?").strip().split(",")
    #         sequence_mode = sequence_setup[0]
    #         sequence_segments = int(sequence_setup[1])

    #         # check that sequence mode is not OFF
    #         if sequence_mode == "OFF":
    #             raise Exception(
    #                 "Sequence acquisition mode is off. Turn it on before setting a segment_number in the waveform setup."
    #             )

    #         # check that the selected segment number is within range
    #         if not (segment_number >= 0 and segment_number < sequence_segments):
    #             raise Exception("segment_number is out of range.")
    #     else:
    #         segment_number = 0

    #     # Setup the command
    #     cmd = f"WAVEFORM_SETUP SP,{int(sparsing)},NP,{int(number_of_points)},FP,{int(first_point)},SN,{segment_number}"
    #     # Run the command
    #     self.__scope.write(cmd)

    def get_waveform(self) -> str:
        return "ok"
