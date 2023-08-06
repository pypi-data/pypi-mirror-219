from matplotlib import pyplot as plt
import numpy as np

import lsqfitgp as lgp

fig, axs = plt.subplots(1, 2, clear=True, num='matern')

x = np.linspace(0, 10, 1000)
y0 = lgp.ExpQuad()(0, x)
axs[1].plot(x, y0, label='ExpQuad')

for v in range(1, 100, 10):
    x = np.logspace(-15, 15, 10000)
    y0 = lgp.ExpQuad()(0, x)
    y1 = lgp.Matern(nu=v)(0, x)
    diff = np.abs(y0 - y1)
    axs[0].plot(x, diff, label=f'$\\nu = {v}$')
    
    x = np.linspace(0, 10, 1000)
    y1 = lgp.Matern(nu=v)(0, x)
    axs[1].plot(x, y1, label=f'$\\nu = {v}$')    

ax = axs[0]
ax.set_xscale('log')
ax.set_yscale('log')

for ax in axs:
    ax.legend()
    ax.grid()

fig.show()
