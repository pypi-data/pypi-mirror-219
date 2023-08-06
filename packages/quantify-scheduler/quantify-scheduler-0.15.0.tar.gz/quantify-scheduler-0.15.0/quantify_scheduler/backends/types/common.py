# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch
"""Common python dataclasses for multiple backends."""

from dataclasses import dataclass
from typing import Literal, Optional

from dataclasses_json import DataClassJsonMixin

from quantify_scheduler import enums
from quantify_scheduler.structure.model import DataStructure


@dataclass
class MixerCorrections(DataClassJsonMixin):
    """
    The mixer corrections record type.

    Parameters
    ----------

    amp_ratio: float
        The amplitude ratio between the real and imaginary
        paths for correcting the imbalance
        in the IQ mixer. (default = 1.0)
    phase_error: float
        The phase shift error used to compensate
        for quadrature errors. (default = .0)
    dc_offset_I: float
        The DC offset off the real(I)
        path for lo feed-through compensation
        in Volts(V). (default = .0)
    dc_offset_Q: float
        The DC offset off the imaginary(Q)
        path for lo feed-through compensation
        in Volts(V). (default = .0)
    """

    amp_ratio: float = 1.0
    phase_error: float = 0.0
    dc_offset_I: float = 0.0  # pylint: disable=invalid-name
    dc_offset_Q: float = 0.0  # pylint: disable=invalid-name


@dataclass
class Modulation(DataClassJsonMixin):
    """
    The backend Modulation record type.

    Parameters
    ----------
    type :
        The modulation mode type select. Allows
        to choose between. (default = ModulationModeType.NONE)

        1. no modulation. ('none')
        2. Software premodulation applied in the numerical waveforms. ('premod')
        3. Hardware real-time modulation. ('modulate')
    interm_freq :
        The inter-modulation frequency (IF) in Hz. (default = 0.0).
    phase_shift :
        The IQ modulation phase shift in Degrees. (default = 0.0).
    """

    type: enums.ModulationModeType = enums.ModulationModeType.NONE
    interm_freq: float = 0.0
    phase_shift: float = 0.0


@dataclass
class LocalOscillator(DataClassJsonMixin):
    """
    The backend LocalOscillator record type.

    Parameters
    ----------
    unique_name :
        The unique name identifying the combination of instrument and
        channel/parameters.
    instrument_name :
        The QCodes name of the LocalOscillator.
    generic_icc_name :
        The name of the GenericInstrumentCoordinatorComponent attached to this device.
    frequency :
        A dict which tells the generic icc what parameter maps to the local oscillator
        (LO) frequency in Hz.
    frequency_param
        The parameter on the LO instrument used to control the frequency.
    power :
        A dict which tells the generic icc what parameter maps to the local oscillator
        (LO) power in dBm.
    phase :
        A dict which tells the generic icc what parameter maps to the local oscillator
        (LO) phase in radians.
    parameters :
        A dict which allows setting of channel specific parameters of the device. Cannot
        be used together with frequency and power.
    """

    unique_name: str
    instrument_name: str
    generic_icc_name: Optional[str] = None
    frequency: Optional[dict] = None
    frequency_param: Optional[str] = None
    power: Optional[dict] = None
    phase: Optional[dict] = None
    parameters: Optional[dict] = None


class LocalOscillatorDescription(DataStructure):
    """Information needed to specify a Local Oscillator in the :class:`~.CompilationConfig`."""

    hardware_type: Literal["LocalOscillator"]
    """The field discriminator for this HardwareDescription datastructure."""
    instrument_name: Optional[str]
    """The QCoDeS instrument name corresponding to this Local Oscillator."""
    generic_icc_name: Optional[str]
    """The name of the :class:`~.GenericInstrumentCoordinatorComponent` corresponding to this Local Oscillator."""
    frequency_param: str = "frequency"
    """The QCoDeS parameter that is used to set the LO frequency."""
    power_param: str = "power"
    """The QCoDeS parameter that is used to set the LO power."""
    power: Optional[int]
    """The power setting for this Local Oscillator."""
