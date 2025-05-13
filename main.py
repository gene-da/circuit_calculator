from modules.transformer import *

N1 = '100u'
N2 = '200u'
V1 = '10m'

ratio = turns_ratio(CoilType.inductor, N1, N2, Output.print)

V2 = voltage_transformation(Winding.secondary, ratio, V1, Output.print)
V1 = voltage_transformation(Winding.primary, ratio, V2, Output.print)


print(V2)