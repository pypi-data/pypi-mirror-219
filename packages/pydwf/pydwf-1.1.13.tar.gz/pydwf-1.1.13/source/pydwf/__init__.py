"""The |pydwf| package provides classes and types to control Digilent Waveforms devices."""

# The version number of the *pydwf* package.
__version__ = "1.1.13"

# The *DwfLibrary* type is the only type users need to access library functionality.
from pydwf.core.dwf_library import DwfLibrary

# Import the 27 enumeration types and make them available for import directly from the *pydwf* package.
from pydwf.core.auxiliary.enum_types import (DwfErrorCode, DwfEnumFilter, DwfEnumConfigInfo, DwfDeviceID,
                                             DwfDeviceVersion, DwfDeviceParameter, DwfWindow, DwfState,
                                             DwfTriggerSource, DwfTriggerSlope, DwfAcquisitionMode,
                                             DwfAnalogInFilter, DwfAnalogCoupling, DwfAnalogInTriggerType,
                                             DwfAnalogInTriggerLengthCondition, DwfAnalogOutFunction,
                                             DwfAnalogOutNode, DwfAnalogOutMode, DwfAnalogOutIdle,
                                             DwfDigitalInClockSource, DwfDigitalInSampleMode,
                                             DwfDigitalOutOutput, DwfDigitalOutType, DwfDigitalOutIdle,
                                             DwfAnalogIO, DwfAnalogImpedance, DwfDmm)

# Import the two exception classes and make them available for import directly from the *pydwf* package.
from pydwf.core.auxiliary.exceptions import PyDwfError, DwfLibraryError
