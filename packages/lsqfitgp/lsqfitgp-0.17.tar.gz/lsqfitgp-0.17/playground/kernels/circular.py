import numpy as np
from matplotlib import pyplot as plt

def f(d):
    x = d % (2 * np.pi)
    return np.minimum(x, 2 * np.pi - x)

fig, ax = plt.subplots(num='circular', clear=True)

x = np.linspace(-20, 20, 1000)
y = f(x)

ax.plot(x, y)

fig.show()
