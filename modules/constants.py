from enum import Enum, auto

omega = 'Ω'

class Output(Enum):
    raw =       auto()
    metric =    auto()
    print =     auto()
    table =     auto()
    
class Winding(Enum):
    primary =   auto()
    secondary = auto()
    
class CoilType(Enum):
    inductor = auto()
    windings = auto()