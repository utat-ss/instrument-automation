import logging

from pyvisa.errors import VisaIOError

from autometrology.errors import ChannelError, InstrumentOpenError
from autometrology.lab.generic.dc_power_supply import DCPowerSupply
from autometrology.visa.utils import VISAUtils

# ! TODO: INCOMPLETE!!


class Keithley_2230_30_1(DCPowerSupply):
    # -- Constructor
    def __init__(self, resource_id: str = None):
        super().__init__("Keithley 2230-30-1", 0, 30.1, 0, 1.55)

        # Scan
        if resource_id is None:
            resource_id = VISAUtils.scan(self.visa, "*IDN?", "2230-30-1")

        # Open
        try:
            self.visa.open(resource_id)
        except VisaIOError as e:
            raise InstrumentOpenError(str(e))

        # Config
        self.visa.resource.read_termination = "\n"
        self.visa.resource.write_termination = "\n"

        logging.info(self.visa.query("*IDN?").replace("\n", " ") + "loaded!")

    # -- Methods
    def _set_voltage(self, v: float):
        raise NotImplementedError

    def _set_current(self, i: float):
        raise NotImplementedError

    def select_channel(self, channel: int):
        if channel not in [1, 2, 3]:
            raise ChannelError(f"Expecting channel 1, 2, or 3 but got {channel}")

        self.visa.write(f"INST:NSEL {channel}")

    def enable(self):
        self.visa.write("CHAN:OUTP ON")

    def disable(self):
        self.visa.write("CHAN:OUTP OFF")

    def close(self):
        self.visa.write("SYST:LOC")
        self.visa.close()
