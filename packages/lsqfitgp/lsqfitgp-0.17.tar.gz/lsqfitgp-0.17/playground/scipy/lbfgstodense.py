from scipy import optimize
import numpy as np

sk, yk = np.random.randn(2, 10, 1000)
invh = optimize.LbfgsInvHessProduct(sk, yk)

def todense(self):
    """ Rewrite LbfgsInvHessProduct.todense avoiding matrix @ matrix """
    s, y, n_corrs, rho = self.sk, self.yk, self.n_corrs, self.rho
    Hk = np.eye(*self.shape, dtype=self.dtype)

    for i in range(n_corrs):
        # H  <--  (I - rho sy') H (I - rho ys') + rho ss' =
        #       = H - rho Hys' - rho sy'H + rho^2 sy'Hys' + rho ss' =
        #       = H - rho Hys' - rho sy'H + rho(1 + rho y'Hy) ss'
        rhoHys = -rho[i] * np.outer(Hk @ y[i], s[i])
        Hk += (rho[i] * (1 + rho[i] * (y[i] @ Hk @ y[i]))) * np.outer(s[i], s[i])
        Hk += rhoHys
        Hk += rhoHys.T

    return Hk

def _matmat(self, X):
    """ Rewrite LbfgsInvHessProduct._matvec broadcasting on columns of X """
    s, y, n_corrs, rho = self.sk, self.yk, self.n_corrs, self.rho
    Q = np.array(X, dtype=self.dtype, copy=True)
    assert Q.ndim == 2

    alpha = np.empty((n_corrs, Q.shape[1]))

    for i in range(n_corrs-1, -1, -1):
        alpha[i] = rho[i] * np.dot(s[i], Q)
        Q = Q - alpha[i]*y[i][:, np.newaxis]

    R = Q
    for i in range(n_corrs):
        beta = rho[i] * np.dot(y[i], R)
        R = R + s[i][:, np.newaxis] * (alpha[i] - beta)

    return R

inv1 = invh.todense()
inv2 = todense(invh)
inv3 = _matmat(invh, np.eye(*invh.shape))
np.testing.assert_allclose(inv1, inv2, atol=0, rtol=1e-5)
np.testing.assert_allclose(inv1, inv3, atol=0, rtol=1e-5)

%timeit -r1 invh.todense()
%timeit -r1 todense(invh)
%timeit -r1 _matmat(invh, np.eye(*invh.shape))
%timeit -r1 invh.matmat(np.eye(*invh.shape))
