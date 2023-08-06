import numpy as np
from scipy import special
from matplotlib import pyplot as plt

import lsqfitgp as lgp

fig, ax = plt.subplots(num='expn', clear=True)

nt = 20
eps = np.finfo(float).eps
d = 3
nrange = np.arange(2, 2 + 1 + 10 * d, d)[::-1]

x = np.logspace(0, 4, 10000)
for n in nrange:
    y1 = lgp._patch_jax.expn_imag_smallx(n, x).real
    y2 = lgp._patch_jax.expn_asymp(n, -1j * x, nt).real
    line, = ax.plot(x, np.abs(y1 - y2), label=f'n={n}')
    color = line.get_color()
    # knee = (1/eps) ** (1 / (2 * (n - 1)))
    # knee = (special.poch(n, nt) / eps) ** (1 / (n + nt - 1))
    kneex = (special.gamma(n + nt) / eps) ** (1 / (n + nt - 1))
    kneey = eps * kneex ** (n - 2) / special.gamma(n)
    kw = dict(color=color, linestyle='--')
    ax.axvline(kneex, 0, 1, **kw)
    ax.axhline(kneey, 0, 1, **kw)

ax.set_ylabel('|E_n direct - E_n asymp|')
ax.set_yscale('log')
ax.set_xscale('log')
ax.legend()

fig.show()


fig, ax = plt.subplots(num='expn2', clear=True)

nts = np.linspace(0, 100, 1000)
for n in nrange:
    kneex = (special.gamma(n + nts) / eps) ** (1 / (n + nts - 1))
    kneey = eps * kneex ** (n - 2) / special.gamma(n)
    ax.plot(nts, kneey, label=f'n={n}')

ax.legend()
ax.set_yscale('log')
ax.set_xlabel('number of terms in asymp series')
ax.set_ylabel('error at knee')

fig.show()


fig, ax = plt.subplots(num='expn3', clear=True)

nt = 20
n = np.arange(2, 21)
kneex = (special.gamma(n + nt) / eps) ** (1 / (n + nt - 1))
ax.plot(n, kneex)

ax.set_xlabel('n')
ax.set_ylabel('knee x')

fig.show()

# TODO find the minimum of kneey(nt) for float32 and float64, plot w.r.t. n,
# round to nearest integer, tabulate up to reasonable n (guess 30-40)
