"""Autograd makes array.reshape behave like np.reshape(array) which has a
different signature, but only in a certain corner case I have not properly
figured out."""

import autograd
from autograd import numpy as anp

x = anp.arange(9)

def f(x):
    return (x ** 2).reshape(3, 3)

jac = autograd.jacobian(f)
hess = autograd.jacobian(jac)

J = jac(x)
H = hess(x)
