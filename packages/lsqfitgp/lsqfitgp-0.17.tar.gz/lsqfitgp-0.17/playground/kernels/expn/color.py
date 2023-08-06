import numpy as np
from matplotlib import pyplot as plt

import lsqfitgp as lgp

fig, ax = plt.subplots(num='color', clear=True)

s = 0
x = np.linspace(s, s + 100, 10000)
for n in range(2, 30, 3):
    y = lgp.Color(n=n)(0, x)
    ax.plot(x, y, label=f'$n = {n}$')
ax.legend()

fig.show()
