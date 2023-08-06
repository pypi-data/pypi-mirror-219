import lsqfitgp as lgp
from matplotlib import pyplot as plt
import numpy as np

alpha = 1

gp = lgp.GP()
gp.addproc(lgp.Gibbs(scalefun=lambda x: x + 1e-16), 'f')
gp.addprocrescale(lambda x: x ** (alpha + 1) / (alpha + 2), 'g', 'f')
gp.addprocderiv(1, 'h', 'g')

x = np.linspace(0, 1, 100)[1:]
gp.addx(x, 'x', proc='h')
cov = gp.prior('x', raw=True)
sdev = np.sqrt(np.diag(cov))

fig, ax = plt.subplots(num='priortest', clear=True)

ax.plot(x, sdev, label='prior sdev')
ax.plot(x, x ** alpha, label=f'$x^{{{alpha}}}$')
ax.legend()

fig.show()
