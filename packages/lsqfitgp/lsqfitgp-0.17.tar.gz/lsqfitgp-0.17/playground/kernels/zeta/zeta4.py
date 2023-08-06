import numpy as np
from matplotlib import pyplot as plt

import lsqfitgp as lgp

fig, ax = plt.subplots(num='zeta4', clear=True)

x = np.linspace(0, 2, 10001)
for s in [1.1, 1.5, 2, 3, 4]:
    y = lgp._patch_jax.periodic_zeta_real(x, s) / lgp._patch_jax.zeta(s)
    ax.plot(x, y, label=f's={s}')

ax.legend()

fig.show()
