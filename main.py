from pyproj import Transformer, Geod #–азобратьс€ с библиотекой, возможно реализовать несколько систем координат?
from typing import  Type

from Classes import Transmitter 

def Calculate_distance_antenna_to_sattelite(ant1, ant2):
    pos1 = ant1.pos1
    pos2 = ant1.pos2
    pos3 = ant1.pos3
    x = ant2.pos1
    y = ant2.pos2
    z = ant2.pos3

    return 0;

