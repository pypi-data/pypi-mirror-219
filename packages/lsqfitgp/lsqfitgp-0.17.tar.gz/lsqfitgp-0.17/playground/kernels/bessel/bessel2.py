from scipy import special
import numpy as np
from matplotlib import pyplot as plt

fig, ax = plt.subplots(num='bessel2', clear=True)

nu = np.linspace(-10, 0, 10)
x = np.linspace(0, 5, 100)

for v in nu:
    y = (x / 2) ** -v * special.jv(v, x) * special.gamma(v + 1)
    ax.plot(x, y, label=f'$\\nu$={v:.2g}')

ax.legend()
ax.set_xlabel('$x$')
ax.set_ylabel('$J_\\nu(x)$')
ax.grid()

fig.show()
