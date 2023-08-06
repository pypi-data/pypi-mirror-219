import numpy as np
from matplotlib import pyplot as plt
import mpmath

import lsqfitgp as lgp

zeta = np.vectorize(lambda *args: float(mpmath.zeta(*args)))

def dlmf_25_11_7(s, a):
    # for integer s <= 0
    return a ** -s + (1 + a) ** -s * (1/2 + (1 + a) / (s - 1))

fig, ax = plt.subplots(num='zeta', clear=True)

a = np.linspace(0, 1, 1000)
for s in np.arange(0, -10, -1):
    z = dlmf_25_11_7(s, a)
    zsure = zeta(s, a)
    line, = ax.plot(a, zsure, label=f's={s}')
    ax.plot(a, z, color=line.get_color(), linestyle='--')

ax.legend()

fig.show()
