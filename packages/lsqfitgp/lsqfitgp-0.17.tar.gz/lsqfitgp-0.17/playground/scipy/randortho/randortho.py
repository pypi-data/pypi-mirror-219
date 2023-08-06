from scipy import stats, linalg
import numpy as np
from matplotlib import pyplot as plt

def gen1(n, size=1):
    return stats.ortho_group.rvs(n, size)

def gen2(n, size=()):
    if not hasattr(size, '__len__'):
        size = (size,)
    a = np.random.randn(*size, n, n)
    q, r = np.linalg.qr(a)
    # q *= np.sign(np.diagonal(r, 0, -2, -1))[..., None, :]
    q *= 2 * np.random.randint(2, size=size + (1, n)) - 1
    return q 

def gen3(n, size=()):
    if not hasattr(size, '__len__'):
        size = (size,)
    a = np.random.randn(*size, n, n)
    at = np.swapaxes(a, -2, -1)
    a += at
    w, v = np.linalg.eigh(a)
    v *= 2 * np.random.randint(2, size=size + (1, n)) - 1
    return v

samples = [
    np.angle(np.linalg.eigvals(gen(3, 10000))).flat
    for gen in [gen1, gen2, gen3]
]

fig, ax = plt.subplots(num='randortho', clear=True)

ax.hist(samples, bins='auto', histtype='step')

plt.show()
