import itertools

import numpy as np
from matplotlib import pyplot as plt
import gvar

import lsqfitgp as lgp

fig, ax = plt.subplots(num='zeta6', clear=True)

x = np.linspace(0, 1, 1001)
f = lgp.Zeta(nu=0.3, derivable=True).diff(0, 1)
y = f(0, x)
ax.plot(x, y)

ax.legend()

fig.show()
