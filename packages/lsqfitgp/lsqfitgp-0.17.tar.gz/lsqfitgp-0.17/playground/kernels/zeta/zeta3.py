import numpy as np
from matplotlib import pyplot as plt
import mpmath
from scipy import special

import lsqfitgp as lgp

zeta = np.vectorize(lambda *args: float(mpmath.zeta(*args)))

fig, ax = plt.subplots(num='zeta3', clear=True)

s = -1 + 1e-4 * np.linspace(-1, 1, 1001)
z = special.zeta(s)
zsure = zeta(s)
ax.plot(s, np.abs(z - zsure) / np.max(np.abs(zsure)))

ax.set_yscale('log')
ax.set_xlabel('s')
ax.set_title('$|\\zeta_\\mathrm{scipy}(s) - \\zeta(s)|\\,/\\,|\\zeta(s)|$')
ax.axhline(100 * np.finfo(float).eps, linestyle='--', color='red', label='100 ULP')
ax.axhline(np.finfo(float).eps, linestyle='--', color='black', label='1 ULP')
ax.legend()

fig.show()
