import numpy as np
from matplotlib import pyplot as plt
import mpmath

import lsqfitgp as lgp

zeta = np.vectorize(lambda *args: float(mpmath.zeta(*args)))

fig, ax = plt.subplots(num='zeta2', clear=True)

a = np.linspace(0, 1, 1000)
for s in [-0.5]:
    z = lgp._patch_jax.hurwitz_zeta(s, a)
    zsure = zeta(s, a)
    ax.plot(a, np.abs(z - zsure) / np.max(np.abs(zsure)), label=f's={s:.2g}')

ax.set_yscale('log')
ax.set_xlabel('a')
ax.set_title('$|\\zeta_\\mathrm{impl}(s,a) - \\zeta(s, a)|\\,/\\,\\max_a|\\zeta(s, a)|$')
ax.axhline(np.finfo(float).eps, linestyle='--', color='black', label='1 ULP')
ax.axhline(100 * np.finfo(float).eps, linestyle='--', color='black', label='100 ULP')
ax.legend()

fig.show()
