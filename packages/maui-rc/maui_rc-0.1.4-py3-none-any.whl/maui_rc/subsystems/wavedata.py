from enum import Enum
import struct
import numpy as np

class WaveformData:

    class RecordType(Enum):
        SingleSweep = 0
        Interleaved = 1
        Histogram = 2
        Graph = 3
        FilterCoefficient = 4
        Complex = 5
        Extrema = 6
        SequenceObsolete = 7
        CenteredRIS = 8
        PeakDetect = 9

        def __str__(self):
            return self.name
        
    class ProcessingDone(Enum):
        NoProcessing = 0
        FirFilter = 1
        Interpolated = 2
        Sparsed = 3
        AutoScaled = 4
        NoResult = 5
        Rolling = 6
        Cumulative = 7
    
        def __str__(self):
            return self.name
        
    class TimeBase(Enum):
        """Enum identifying a specific timebase."""
        PS_1 = 0
        PS_2 = 1
        PS_5 = 2
        PS_10 = 3
        PS_20 = 4
        PS_50 = 5
        PS_100 = 6
        PS_200 = 7
        PS_500 = 8
        NS_1 = 9
        NS_2 = 10
        NS_5 = 11
        NS_10 = 12
        NS_20 = 13
        NS_50 = 14
        NS_100 = 15
        NS_200 = 16
        NS_500 = 17
        US_1 = 18
        US_2 = 19
        US_5 = 20
        US_10 = 21
        US_20 = 22
        US_50 = 23
        US_100 = 24
        US_200 = 25
        US_500 = 26
        MS_1 = 27
        MS_2 = 28
        MS_5 = 29
        MS_10 = 30
        MS_20 = 31
        MS_50 = 32
        MS_100 = 33
        MS_200 = 34
        MS_500 = 35
        S_1 = 36
        S_2 = 37
        S_5 = 38
        S_10 = 39
        S_20 = 40
        S_50 = 41
        S_100 = 42
        S_200 = 43
        S_500 = 44
        KS_1 = 45
        KS_2 = 46
        KS_5 = 47
        EXTERNAL = 100

        def value(self) -> float:
            """Return the timebase in seconds."""

            # Deal with external
            if self.name == 'EXTERNAL':
                raise Exception("unimplemented error: external timebase is not implemented")

            # extract the letter part of the name and the number part
            name = self.name.split("_")
            # letter part represents the unit/scale of the timebase
            scale = name[0]
            # number part is the factor of the timebase
            factor = float(name[1])

            match scale:
                case "PS": scale = 1.e-12
                case "NS": scale = 1.e-9
                case "US": scale = 1.e-6
                case "MS": scale = 1.e-3
                case "S": scale = 1.
                case "KS": scale = 1.e3
            
            return scale * factor

    class Coupling(Enum):
        DC_50_Ohms = 0
        Ground = 1 | 3
        DC_1M_Ohm = 2
        AC_1MOhm = 4

        def __str__(self):
            return self.name 
        
    class VertGain(Enum):
        UV_1 = 0
        UV_2 = 1
        UV_5 = 2
        UV_10 = 3
        UV_20 = 4
        UV_50 = 5
        UV_100 = 6
        UV_200 = 7
        UV_500 = 8
        MV_1 = 9
        MV_2 = 10
        MV_5 = 11
        MV_10 = 12
        MV_20 = 13
        MV_50 = 14
        MV_100 = 15
        MV_200 = 16
        MV_500 = 17
        V_1 = 18
        V_2 = 19
        V_5 = 20
        V_10 = 21
        V_20 = 22
        V_50 = 23
        V_100 = 24
        V_200 = 25
        V_500 = 26
        KV_1 = 27

        def value(self) -> float:
            """Return the vertical gain in volts."""

            name = self.name.split("_")
            scale = name[0]
            factor = float(name[1])

            match scale:
                case "UV": scale = 1.e-6
                case "MV": scale = 1.e-3
                case "V": scale = 1.
                case "KV": scale = 1.e3

            return scale * factor
        
    class Source(Enum):
        CHANNEL_1 = 0
        CHANNEL_2 = 1
        CHANNEL_3 = 2
        CHANNEL_4 = 3
        UNKNOWN = 9

        def __str__(self):
            return self.name
        
    class Timestamp:
        def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: float):
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
            self.second = second

        def __str__(self):
            return f"{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}"

    # GENERAL DESCRIPTION VARIABLES

    byteorder: str
    """Order in which bytes are read to numbers in the waveform data"""
    wf_datapoint_size: int
    """Size in bytes of a single data point in the waveform data"""

    wave_desc_size: int
    """Number of bytes in the DESC block"""
    user_text_size: int
    """Number of bytes in the TEXT block"""
    reserved_desc_size: int
    """Number of bytes in the reserved description block"""
    trigtime_array_size: int
    """Number of bytes in the TIME block"""
    ris_time_array_size: int
    """Number of bytes in the rising time block"""
    res1_array_size: int
    """Number of bytes in the reserved array 1 block"""
    res2_array_size: int
    """Number of bytes in the reserved array 2 block"""
    res3_array_size: int
    """Number of bytes in the reserved array 3 block"""

    # IDENTIFICATION VARIABLES

    instrument_name: str
    """Name of the instrument"""
    instrument_number: int
    """Identifying number of the instrument"""
    trace_label: str
    """Label of the trace associated this waveform data"""
    reserved_1: int
    """Reserved space 1"""
    reserved_2: int
    """Reserved space 2"""

    # WAVEFORM CONDITIONS

    wave_array_count: int
    """Number of data points in the array. If there are two arrays, this number applies to each array separatly."""
    points_per_screen: int
    """Nominal number of data points on the screen."""
    first_valid_point: int
    """Count of number of points to skip before first good point. It is `0` for normal waveforms."""
    last_valid_point: int
    """Index of last good data pount in record before padding was started. Usually `wave_array_count - 1` except for aborted sequence and rollmode acquisitions."""
    first_point: int
    """For I/O, indicates the offset relative to the beginning of the trace buffer."""
    sparsing_factor: int
    """For I/O, indicates the sparsing into the transmitted data block."""
    segment_index: int
    """For I/O, indicates the index of the transmitted segment."""

    subarray_count: int
    """For Sequence, acquired segment count, between `0` and `nominal_subarray_count`."""
    nominal_subarray_count: int
    """For Sequence, nominal segment count, otherwise just `1`."""

    sweeps_per_acquisition: int
    """For Average or Extrema, number of sweeps accumulated, otherwise just `1`."""
    points_per_pair: int
    """For Peak Detect waveforms (data points in DAT1 and min/max pairs in DAT2), number of data points for each min/max pair."""
    pair_offset: int
    """For Peak Detect waveforms only, number of data points by which the first min/max pair in DAT2 is offset relative to the first data value in DAT1."""

    vertical_gain: float
    """Vertical gain."""
    vertical_offset: float
    """To get floating point values from data: `vertical_gain * data - vertical_offset`."""
    max_value: float
    """Max vertical value, the top edge of the grid."""
    min_value: float
    """Minimum vertical value, the bottom edge of the grid."""

    nomimal_bits: int
    """Measure of intrinsic precision of the observation: ADC data is 8 bit, averaged data is 10-12 but, etc."""
    
    horizontal_interval: float
    """Sampling interval for the time domain."""
    horizontal_offset: float
    """Trigger offset for the first sweep of the trigger, seconds between the trigger and the first data point."""

    pixel_offset: float
    """Needed to know how to display the waveform."""

    vertical_unit: str
    """Units of the vertical axis."""
    horizontal_unit: str
    """Units of the horizontal axis."""
    horizontal_uncertainty: float
    """Uncertainty from one acquisition to the next, of the horizontal offset in seconds"""
    trigger_time: Timestamp
    """Time of the trigger."""
    acquisition_duration: float
    """Duration of the acquisition in seconds."""

    record_type: RecordType
    """What kind of data we was transfered. Defines how we will treat it."""
    processing_done: ProcessingDone
    """Processing done to the data on the device."""

    ris_sweeps: int
    """For RIS, the number of sweeps, otherwise `1`."""

    # ACQUISITION CONDITIONS

    timebase: TimeBase
    """Timebase of the acquisition."""
    vertical_coupling: Coupling
    """Coupling used for the acquisition."""
    probe_attenuation: float
    """Attenuation of the probe."""
    fixed_vertical_gain: VertGain
    """Vertical gain of the acquisition."""
    bandwidth_limit: bool
    """Whether the bandwidth limit is active or not."""
    vertical_vernier: float
    """Vertical vernier of the acquisition."""
    acquisition_vertical_offset: float
    """Vertical offset of the acquisition."""
    wave_source: Source
    """The channel from which the data comes from."""

    def __parse_to_string(self, data: bytes):
        """Parse a chunk of bytes into a string."""
        return data.decode('utf-8').strip("\x00").strip()
    
    def __parse_timestamp(self, data: bytes):
        """Parse a chunk of bytes as a timestamp"""
        if len(data) != 16:
            raise Exception("parsing error: timestamp must be 16 bytes long")
        
        second = self.__parse_to_float(data[0:8])
        minute = self.__parse_to_int(data[8:9])
        hour = self.__parse_to_int(data[9:10])
        day = self.__parse_to_int(data[10:11])
        month = self.__parse_to_int(data[11:12])
        year = self.__parse_to_int(data[12:14])

        return self.Timestamp(year, month, day, hour, minute, second)



    def __parse_to_int(self, data: bytes):
        """Parse a chunk of bytes into an integer."""
        if len(data) == 1:
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}b", data)[0]
        if len(data) == 2:
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}h", data)[0]
        elif len(data) == 4:
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}l", data)[0]
        elif len(data) == 8:
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}q", data)[0]
        else:
            raise Exception("parsing error: data is not 8, 16 or 32 bits, cannot parse to int")

        return int.from_bytes(data, self.byteorder)

    def __parse_to_float(self, data: bytes):
        """Parse a chunk of bytes into a float."""
        # first check if its 32 or 64 bit
        if len(data) == 4:
            # 32 bit
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}f", data)[0]
        elif len(data) == 8:
            # 64 bit
            return struct.unpack(f"{'>' if self.byteorder == 'big' else '<'}d", data)[0]
        else:
            # can't parse to float
            raise Exception("parsing error: data is not 32 or 64 bits, cannot parse to float")

    def __parse_wavedesc(self, desc_block: bytes):
        desc = desc_block
        # Get the descriptor name and template name
        self.descriptor_name = self.__parse_to_string(desc[:15])
        self.template_name = self.__parse_to_string(desc[16:31])

        # validate that the waveform uses the correct template
        if self.template_name != "LECROY_2_3":
            print(len(self.template_name))
            print(len("LECROY_2_3"))
            raise Exception("Waveform data does not use Lecroy 2.3 template.")

        # Determine out the byte order
        comm_order = int.from_bytes(desc[34:36], 'big')
        if comm_order != 1 or comm_order != 0:
            comm_order = int.from_bytes(desc[34:36], 'little')
        if comm_order == 0:
            self.byteorder = 'big'
        else:
            self.byteorder = 'little'

        # Determine the size of waveform data
        comm_type = self.__parse_to_int(desc[32:34])
        if comm_type == 0:
            self.wf_datapoint_size = 1 # byte
        else:
            self.wf_datapoint_size = 2 # bytes

        # Determine the size of arrays in bytes
        self.wave_desc_size = self.__parse_to_int(desc[36:40])
        self.user_text_size = self.__parse_to_int(desc[40:44])
        self.reserved_desc_size = self.__parse_to_int(desc[44:48])
        self.trigtime_array_size = self.__parse_to_int(desc[48:52])
        self.ris_time_array_size = self.__parse_to_int(desc[52:56])
        self.res1_array_size = self.__parse_to_int(desc[56:60])
        self.dat1_array_size = self.__parse_to_int(desc[60:64])
        self.dat2_array_size = self.__parse_to_int(desc[64:68])
        self.res2_array_size = self.__parse_to_int(desc[68:72])
        self.res3_array_size = self.__parse_to_int(desc[74:76])

        # Get instrument identification variables
        self.instrument_name = self.__parse_to_string(desc[76:92])
        self.instrument_number = self.__parse_to_int(desc[92:96])
        self.trace_label = self.__parse_to_string(desc[96:112])
        self.reserved_1 = self.__parse_to_int(desc[112:114])
        self.reserved_2 = self.__parse_to_int(desc[114:116])

        # Waveform and time descriptions
        self.wave_array_count = self.__parse_to_int(desc[116:120])
        self.points_per_screen = self.__parse_to_int(desc[120:124])
        self.first_valid_point = self.__parse_to_int(desc[124:128])
        self.last_valid_point = self.__parse_to_int(desc[128:132])
        self.first_point = self.__parse_to_int(desc[132:136])
        self.sparsing_factor = self.__parse_to_int(desc[136:140])
        self.segment_index = self.__parse_to_int(desc[140:144])
        self.subarray_count = self.__parse_to_int(desc[144:148])
        self.sweeps_per_acquisition = self.__parse_to_int(desc[148:152])
        self.points_per_pair = self.__parse_to_int(desc[152:154])
        self.pair_offset = self.__parse_to_int(desc[154:156])

        self.vertical_gain = self.__parse_to_float(desc[156:160])
        self.vertical_offset = self.__parse_to_float(desc[160:164])
        self.max_value = self.__parse_to_float(desc[164:168])
        self.min_value = self.__parse_to_float(desc[168:172])
        self.nomimal_bits = self.__parse_to_int(desc[172:174])
        self.nominal_subarray_count = self.__parse_to_int(desc[174:176])
        self.horizontal_interval = self.__parse_to_float(desc[176:180])
        self.horizontal_offset = self.__parse_to_float(desc[180:188])
        self.pixel_offset = self.__parse_to_float(desc[188:196])
        self.vertical_unit = desc[196:244]
        self.horizontal_unit = desc[244:292]
        self.horizontal_uncertainty = self.__parse_to_float(desc[292:296])
        self.trigger_time = self.__parse_timestamp(desc[296:312])
        self.acquisition_duration = self.__parse_to_float(desc[312:316])
        self.record_type = self.RecordType(self.__parse_to_int(desc[316:318]))
        self.processing_done = self.ProcessingDone(self.__parse_to_int(desc[318:320]))
        self.ris_sweeps = self.__parse_to_int(desc[322:324])
        self.timebase = self.TimeBase(self.__parse_to_int(desc[324:326]))
        self.vertical_coupling = self.Coupling(self.__parse_to_int(desc[326:328]))
        self.probe_attenuation = self.__parse_to_float(desc[328:332])
        self.fixed_vertical_gain = self.VertGain(self.__parse_to_int(desc[332:334]))
        self.bandwidth_limit = bool(self.__parse_to_int(desc[334:336]))
        self.vertical_vernier = self.__parse_to_float(desc[336:340])
        self.acquisition_vertical_offset = self.__parse_to_float(desc[340:344])
        self.wave_source = self.Source(self.__parse_to_int(desc[344:346]))

    def __parse_usertext(self, text_block: bytes):
        self.usertext = self.__parse_to_string(text_block)

    def __parse_horizontal_values(self, time_block: bytes):
        # First, we need to check if we are in SingleSweep, Sequence or RIS
        if len(time_block.strip()) == 0:
            # The time block is ONLY used by Sequence OR RIS, so 
            # if it is empty, we MUST be in single sweep
            data = []
            for i in range(self.first_valid_point, self.last_valid_point):
                data.append((self.horizontal_interval * i + self.horizontal_offset))
            self.data_x = np.array(data)
        elif self.nominal_subarray_count != 1:
            # If it is not 1, then we MUST be in a sequence
            # First, get the times and offsets from the TIME block
            data = []
            # go through each time data point and collect the 
            first_trig_times = []
            trigger_offsets = []
            for i in range(0,self.nominal_subarray_count):
                start_pos = i * 16
                first_trig_times.append(self.__parse_to_float(time_block[start_pos:start_pos+8]))
                trigger_offsets.append(self.__parse_to_float(time_block[start_pos+8:start_pos+16]))
            # Here, the time represents the time for a 
            points_per_segment = int(self.wave_array_count / self.nominal_subarray_count)
            for i in range(self.first_valid_point, self.last_valid_point):
                m = (i // points_per_segment)
                data.append(self.horizontal_interval * i + trigger_offsets[m] + first_trig_times[m])

            self.data_x = np.array(data)
        elif self.ris_sweeps != 1:
            # if it isn't 1, then we are in RIS mode
            offsets = []
            for i in range(0, self.ris_sweeps):
                start_pos = i * 8
                ris_offset = self.__parse_to_float(time_block[start_pos:start_pos+8])
                offsets.append(ris_offset)
            data = []
            for i in range(self.first_valid_point, self.last_valid_point):
                m = i % self.ris_sweeps
                j = i - m
                data.append(self.horizontal_interval * j + ris_offset[m])
            self.data_x = np.array(data)

    def __parse_vertical_values(self, data_block_1: bytes, data_block_2: bytes):
        # Parse the first block
        data_1 = []
        for i in range(self.first_valid_point, self.last_valid_point):
            start_pos = i * self.wf_datapoint_size
            data = data_block_1[start_pos:start_pos+self.wf_datapoint_size]
            data_1.append(self.__parse_to_int(data))
        data_1 = self.vertical_gain * np.array(data_1) - self.vertical_offset

        # check that the second block is populated
        data_2 = []
        if len(data_block_2) != 0:
            # The second block is set
            if len(data_block_2) != len(data_block_1):
                # If both blocks have a different size: Peak Detect mode
                for i in range(self.first_valid_point, self.last_valid_point):
                    m = i % self.points_per_pair
                    start_pos = (m + self.pair_offset) * self.wf_datapoint_size
                    data = data_block_2[start_pos:(start_pos + self.wf_datapoint_size)]
                    data_2.append(self.__parse_to_int(data))
                data_2 = self.vertical_gain * np.array(data_2) - self.vertical_offset
            else:
                # both have the same size: Complex FFT OR Extrema modes
                for i in range(self.first_valid_point, self.last_valid_point):
                    start_post = i * self.wf_datapoint_size
                    data = data_block_2[start_pos:(start_pos + self.wf_datapoint_size)]
                    data_2.append(self.__parse_to_int(data))
                data_2 = self.vertical_gain * np.array(data_2) - self.vertical_offset

        if len(data_2) != 0:
            self.data_y = np.array([data_1, data_2])
        else:
            self.data_y = data_1


    
    def __init__(self, desc: bytes, text: bytes, time: bytes, dat1: bytes, dat2: bytes):
        # It begins with parsing the description
        # ----------

        
        # for the sake of shortening code, I'll put the blocks in a dict
        blocks = {
            "desc": desc,
            "text": text,
            "time": time,
            "dat1": dat1,
            "dat2": dat2,
        }

        # first, remove the query message bit and block size for each set of bytes
        for key in blocks:
            start_pos = blocks[key].index(b"#9")
            blocks[key] = blocks[key][start_pos+11:]

        # again for shortening the code
        desc = blocks["desc"]

        # Parse the WAVEDESC block
        self.__parse_wavedesc(blocks["desc"])
        
        # Parsing USERTEXT block
        self.__parse_usertext(blocks["text"])

        # Parse the horizontal values
        self.__parse_horizontal_values(blocks["time"])

        # Parse the vertical values
        self.__parse_vertical_values(blocks["dat1"].strip(), blocks["dat2"].strip())
