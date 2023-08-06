import itertools

from matplotlib import pyplot as plt
import numpy as np
from scipy import special

def covfun(theta, tau, alpha, v):
    norm = special.beta(alpha, v + tau) / special.beta(alpha, v)
    return norm * special.hyp2f1(tau, alpha, alpha + v + tau, np.cos(theta))

fig, ax = plt.subplots(clear=True, num='hyp2f1')

taulist = [0.1, 1]
alphalist = [0.1, 1]
vlist = [0.5, 1]

theta = np.linspace(0, np.pi, 1000)

for tau, alpha, v in itertools.product(taulist, alphalist, vlist):
    y = covfun(theta, tau, alpha, v)
    ax.plot(theta, y, label=f'$\\tau={tau}, \\alpha={alpha}, \\nu={v}$')

ax.set_xlabel('$\\theta$ (geodesic distance)')
ax.set_ylabel('covariance')
ax.set_title('F-family covariance function on a sphere')
ax.legend()

fig.show()
