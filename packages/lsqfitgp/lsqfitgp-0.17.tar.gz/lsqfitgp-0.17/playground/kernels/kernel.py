import lsqfitgp as lgp
from matplotlib import pyplot as plt
import numpy as np
import gvar

fig, ax = plt.subplots(num='kernel', clear=True)

kernels = [
    # ['expquad', lgp.ExpQuad()],
    # ['cos', lgp.ExpQuad(scale=3) * lgp.Cos()],
    # ['wiener', lgp.Wiener()],
    # ['fb1/2', lgp.FracBrownian()],
    # ['fb1/10', lgp.FracBrownian(H=1/10)],
    # ['fb9/10', lgp.FracBrownian(H=9/10)],
    # ['fb0.99', lgp.FracBrownian(H=99/100)],
    # ['NN', lgp.NNKernel(loc=10)],
    # ['Fourier(n=1)', lgp.Fourier(n=1, scale=10)],
    # ['Fourier(n=2)', lgp.Fourier(n=2, scale=10)],
    # ['Celerite', lgp.Celerite(gamma=0.1)],
    # ['Harmonic', lgp.Harmonic(Q=10)],
    # ['BrownianBridge', lgp.BrownianBridge()],
    # ['Taylor', lgp.Taylor()],
    ['Pink', lgp.Pink(dw=1e20)],
]

for label, kernel in kernels:
    gp = lgp.GP(kernel)
    x = np.linspace(0, 20, 2000)
    gp.addx(x, 'x', deriv=0)
    y = gp.prior('x')
    samples = np.transpose(list(gvar.raniter(y, 1, eps=1e-12)))
    ax.plot(x, samples, label=label)

ax.legend(loc='best')
fig.show()
