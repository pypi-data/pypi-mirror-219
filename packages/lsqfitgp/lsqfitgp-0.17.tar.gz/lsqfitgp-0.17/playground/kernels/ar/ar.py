import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial import polynomial

import lsqfitgp as lgp

root = 1.5
mu = 2

root = float(root)
roots = np.repeat(root, mu)
pol = polynomial.polyfromroots(roots)
phi = -pol[1:] / pol[0]
acf = lgp._kernels._yule_walker_inv(phi)

fig, ax = plt.subplots(num='ar', clear=True)

x = np.arange(30)
y1 = root ** -x
ext = lgp._kernels._ar_evolve(phi, acf[1:], np.zeros(len(x) - len(acf)))
y2 = np.concatenate([acf, ext])

ax.plot(x, y1, label='power')
ax.plot(x, y2, label='YW')

ax.legend()
ax.set_yscale('log')

fig.show()
