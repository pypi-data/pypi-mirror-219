import numpy as np
from matplotlib import pyplot as plt

nd = 2
alpha = 1
beta = np.ones(nd)
nx = 20

def kernel(x, y, alpha, beta):
    bn2 = np.sum(beta ** 2)
    xyb = x + y + beta
    xybn2 = np.sum(xyb ** 2, axis=-1)
    return (bn2 / xybn2) ** (alpha / 2)

gen = np.random.default_rng(202206241555)
x = gen.uniform(0, 5, (nx, nd))
c = kernel(x[None, :, :], x[:, None, :], alpha, beta)
w = np.linalg.eigvalsh(c)
error = len(c) * np.finfo(float).eps * np.max(w)
if np.min(w) < -error:
    print('NOT POSITIVE!')

fig, ax = plt.subplots(num='decaying', clear=True)

ax.plot(w)

fig.show()
