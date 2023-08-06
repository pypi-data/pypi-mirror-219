from enum import Enum


class Channel(Enum):
    """Enum of selectable channels.

    - `CHAN_1` -> channel 1
    - `CHAN_2` -> channel 2
    - `CHAN_3` -> channel 3
    - `CHAN_4` -> channel 4
    """

    CHAN_1 = "C1"
    CHAN_2 = "C2"
    CHAN_3 = "C3"
    CHAN_4 = "C4"

    def __str__(self):
        return self.value


class CouplingMode(Enum):
    """Enum of possible trigger coupling modes.

    - `DC` -> All signal frequency components are coupled to the trigger circuit for high-frequency bursts.
    - `AC` -> Signal is capacitively coupled, DC levels are rejected, and low frequencies are attenuated.
    - `HFREJ` -> Signal is coupled through a high-pass filter network, DC is rejected, and low frequencies are attenuated. Ideal for triggering on medium- and high-frequency signals.
    - `LFREJ` -> Signals are DC-coupled to the trigger circuit and a low-pass filter attenuates high frequencies. Ideal for triggering on low frequencies.
    """

    AC = "AC"
    DC = "DC"
    HFREJ = "HFREJ"
    LFREJ = "LFREJ"

    def __str__(self):
        return self.value


class TriggerMode(Enum):
    """Enum of possible trigger modes.

    - `AUTO` -> auto TODO add more detail
    - `NORMAL` -> normal TODO add more detail
    - `SINGLE` -> manual trigger to take one acquisition
    - `STOP` -> stop the trigger
    """

    AUTO = "AUTO"
    NORMAL = "NORMAL"
    SINGLE = "SINGLE"
    STOP = "STOP"

    def __str__(self):
        return self.value
