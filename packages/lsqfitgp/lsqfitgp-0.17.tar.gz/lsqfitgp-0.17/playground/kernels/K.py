import numpy as np
from matplotlib import pyplot as plt

import lsqfitgp as lgp

fig, ax = plt.subplots(num='K', clear=True)

x = np.linspace(0, 1e-10, 1000)
nu = 0
for eps in 0.01 * np.arange(10)[::-1]:
    v = nu + eps
    y = lgp.Matern(nu=v)(0, x)
    ax.plot(x, y, label=f'$\\nu = {v}$')

ax.legend()

fig.show()
