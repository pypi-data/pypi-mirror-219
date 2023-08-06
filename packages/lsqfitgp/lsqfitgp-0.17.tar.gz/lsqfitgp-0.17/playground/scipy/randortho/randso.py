from scipy import stats, linalg
import numpy as np
from matplotlib import pyplot as plt

def gen1(n, size=1):
    return stats.special_ortho_group.rvs(n, size)

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
    s = a + at
    w, v = np.linalg.eigh(s)
    return v
    
def gen4(n, size=()):
    pass
    # TODO try to use the h, tau vectors returned by the mode='raw' option
    # of np.linalg.qr, following the last algorithm in Mezzadri (2006).

samples = [
    np.angle(np.linalg.eigvals(gen(3, 10000))).flat
    for gen in [gen1, gen2]
]

fig, ax = plt.subplots(num='randso', clear=True)

ax.hist(samples, bins='auto', histtype='step')

plt.show()
