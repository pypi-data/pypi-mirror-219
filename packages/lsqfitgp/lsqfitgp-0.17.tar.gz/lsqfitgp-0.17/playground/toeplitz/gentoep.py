from scipy import linalg
import numpy as np

gen = np.random.default_rng(20230130003)

n = 10
rank = 5

freqs = np.linspace(0, 1, 2 + n)[1 - rank % 2:1 + rank // 2]
ampl = gen.gamma(1, 1, rank // 2 + rank % 2)
i = np.arange(n)[:, None]
j = np.arange(n)[None, :]
T_comps = np.cos(2 * np.pi * (i - j) * freqs[:, None, None]) * ampl[:, None, None]
T = np.sum(T_comps, axis=0)

assert np.allclose(T, T.T.conj())
assert np.allclose(T, linalg.toeplitz(T[:, 0]))
w = linalg.eigvalsh(T)
assert np.all(w[n - rank:] >= 0)
Tp, r = linalg.pinvh(T, return_rank=True)
assert r == rank
