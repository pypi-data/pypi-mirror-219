import numpy as np
import math
from basic_electronic import inductor_parallel

def freq_hartley(Lt,C,roundNumber=2):
    l = inductor_parallel(Lt)
    return round(1/(2*np.pi*math.sqrt(l*C)),roundNumber)

