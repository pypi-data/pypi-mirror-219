import numpy as np
from scipy import special
from matplotlib import pyplot as plt

import lsqfitgp as lgp

fig, ax = plt.subplots(num='exp1', clear=True)

x = np.linspace(1e-3, 20, 1000)
y1 = lgp._patch_jax.exp1_imag(x)
y2 = special.exp1(-1j * x)
ax.plot(x, y1.real, label=f'lgp real')
ax.plot(x, y2.real, label=f'scipy real', linestyle='--')
ax.plot(x, y1.imag, label=f'lgp imag')
ax.plot(x, y2.imag, label=f'scipy imag', linestyle='--')
ax.legend()

fig.show()
