from scipy import special
import numpy as np
from matplotlib import pyplot as plt

fig, axs = plt.subplots(2, 1, num='bessel', clear=True, figsize=[6.4, 7])

n = np.arange(100)
zeros = np.vectorize(special.jn_zeros, signature='(),()->(n)')(n, 4)

ax = axs[0]

for i, y in enumerate(zeros.T):
    ax.plot(n, y, label=f'{i+1}-th zero')

ax.legend()
ax.set_xlabel('$\\nu$')
ax.set_ylabel('Zero of $J_\\nu$')
ax.grid()

@np.vectorize
def scale(nu):
    lnu = np.floor(nu)
    rnu = np.ceil(nu)
    zl, = special.jn_zeros(lnu, 1)
    if lnu == rnu:
        return zl
    else:
        zr, = special.jn_zeros(rnu, 1)
        return zl + (nu - lnu) * (zr - zl) / (rnu - lnu)

def kernel(x, nu):
    x = np.abs(x) * (2 + nu/2)# scale(nu)
    return special.gamma(nu + 1) * 2 ** nu * x ** -nu * special.jv(nu, x)

nu = np.linspace(0, 10, 10)
x = np.linspace(0, 5, 100)
k = kernel(x, nu[:, None])

ax = axs[1]

for y, n in zip(k, nu):
    ax.plot(x, y, label=f'$\\nu$={n:.2g}')

ax.legend()
ax.set_xlabel('$x$')
ax.set_ylabel('$J_\\nu(x)$')
ax.grid()

fig.show()

d = np.arange(10)
nu = np.arange(10)
yi = np.vectorize(special.jvp)(nu[:, None], 0, 2 * d)
print(yi)

nu = np.stack([nu - 1e-3, nu + 1e-3], 1).reshape(-1)
y = np.vectorize(special.jvp)(nu[:, None], 0, 2 * d)
print(y)
