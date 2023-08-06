import lsqfitgp as lgp
import jax
import numpy as np

@jax.jit
def f():
	dec = lgp._linalg.Chol(np.array([[2]]))
	print('@@@@@@@@@@@@@@@@@@@', id(dec), '@@@@@@@@@@@@@@@@@@@')
	return dec.logdet()

with jax.checking_leaks():
	print(f())
