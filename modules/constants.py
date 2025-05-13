from enum import Enum, auto

omega = 'Ω'

class Output(Enum):
    raw = auto()
    metric = auto()
    print = auto()
    
class Winding(Enum):
    primary = auto()
    secondary = auto()