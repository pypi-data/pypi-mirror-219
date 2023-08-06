import numpy as np
import math
from basic_electronic import capasitor_parallel

def freq_coppitts(L,Ct,roundNumber=2):
    c = capasitor_parallel(Ct)
    return round(1/(2*np.pi*math.sqrt(L*c)),roundNumber)

