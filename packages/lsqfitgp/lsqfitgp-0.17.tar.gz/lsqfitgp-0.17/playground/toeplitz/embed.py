from scipy import linalg
import numpy as np
from matplotlib import pyplot as plt
import tqdm

# checks a symmetric nxn toeplitz matrix can be embedded in a circulant
# (2n-2)x(2n-2) matrix (its 2n-1 for non symmetric)

t = np.arange(6)[::-1]

c = np.concatenate([t, t[1:-1][::-1]])
# question: if t is positive definite, is c positive definite too? I think so
# because it's like we are stitching together repetitions of the process, but
# I'm not sure

m = linalg.toeplitz(c)
m2 = linalg.circulant(c)

np.testing.assert_equal(m2, m)

# check the fourier diagonalization of the circulant matrix (to be sure of
# the correct normalization)

d = np.diag(np.fft.fft(c, norm='backward'))
m3 = np.fft.fft(np.fft.fft(d, axis=0, norm='ortho').conj(), axis=1, norm='ortho')

np.testing.assert_allclose(m3, m, rtol=1e-14, atol=1e-14)

# try using rfft
# => doesn't work
#
# d = np.diag(np.fft.rfft(c, norm='backward'))
# m4 = np.fft.irfft(np.fft.irfft(d, axis=0, norm='ortho'), axis=1, norm='ortho')
#
# np.testing.assert_allclose(m4, m)

nmc = 10000
z = np.random.randn(len(c), nmc)
f = np.fft.fft(c, norm='backward')
y = np.fft.fft(np.sqrt(f)[:, None] * z, axis=0, norm='ortho')
x = y[:len(t), :]
x = x.real + x.imag # <-----
v = linalg.toeplitz(t)
v2 = np.cov(x)

a = np.linalg.norm(v2 - v, 2)
r = a / np.linalg.norm(v)
print(f'abs = {a:.2g}, relative = {r:.2g}')

# generate a random pos def toeplitz matrix
def randt_dumb(n):
    N = 2 * n
    m = np.random.randn(N, N)
    a = m @ m.T
    c = np.zeros_like(a)
    for i in range(N):
        # there is a faster way to generate only the first row
        c += np.roll(a, (i, i), (0, 1))
    t = c[:n, :n]
    return t[0]

def randt(n):
    N = 2 * n - 1
    x = np.random.randn(N)
    a = np.fft.ifft(np.abs(np.fft.fft(x)))
    assert np.allclose(a.imag, 0, atol=1e-15)
    t = a.real[:n]
    return t

def embed(t):
    c = np.concatenate([t, t[1:][::-1]])
    return c

eig = []
for i in tqdm.tqdm(range(100000)):
    t = randt(20)
    assert np.all(linalg.eigvalsh(linalg.toeplitz(t)) >= 0)
    c = embed(t)
    m = linalg.circulant(c)
    e = linalg.eigvalsh(m)
    assert np.all(e >= 0)
    eig.append(e)

fig, ax = plt.subplots(num='embed', clear=True)

e = np.concatenate(eig)
ax.hist(e, bins='auto', histtype='step')

fig.show()
