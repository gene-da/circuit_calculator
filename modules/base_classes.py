from enum import Enum, auto

class BaseReadingTypes(Enum):
    peak        = auto()
    pkpk        = auto()
    true_rms    = auto()
    pk_rms      = auto()
    pkpk_rms    = auto()
    average     = auto()

class BaseReadingSelectionType(Enum):
    AC = auto()
    DC = auto()