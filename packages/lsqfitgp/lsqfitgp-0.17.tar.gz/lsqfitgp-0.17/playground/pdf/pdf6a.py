"""Fit of parton distributions functions (PDFs)

Version of pdf6 to do a test with JAX"""

from jax.config import config
config.update("jax_enable_x64", True)

import lsqfitgp as lgp
import jax
from jax import numpy as jnp
from autograd import numpy as anp
import numpy as np
from matplotlib import pyplot as plt
import gvar
import lsqfit

np.random.seed(20220416)

gvar._bufferdict.numpy = anp

#### SETTINGS ####

flavor = np.array([
    ( 1, 'd'    ), # 0
    (-1, 'dbar' ), # 1
    ( 2, 'u'    ), # 2
    (-2, 'ubar' ), # 3
    ( 3, 's'    ), # 4
    (-3, 'sbar' ), # 5
    ( 4, 'c'    ), # 6
    (-4, 'cbar' ), # 7
    (21, 'gluon'), # 8
], 'i8, U16')

indices = dict(
    # quark, antiquark
    d = [0, 1],
    u = [2, 3],
    s = [4, 5],
    c = [6, 7],
)

pid  = flavor['f0']
name = flavor['f1']

nflav  = len(flavor)

# linear data
nx        = 30 # number of PDF points used for the transformation
ndata     = 10 # number of datapoints
rankmcov  =  9 # rank of the covariance matrix of the theory error

# quadratic data
nx2       = 30 # must be <= nx
ndata2    = 10
rankmcov2 =  9

#### MODEL ####
# for each PDF:
# h ~ GP
# f = h''  (f is the PDF)
# for the momentum sum rule:
# int_0^1 dx x f(x) = [xh'(x) - h(x)]_0^1
# for the flavor sum rules:
# int_0^1 dx (f_i(x) - f_j(x)) = [h_i'(x) - h_j'(x)]_0^1

xtype = np.dtype([
    ('x'  , float),
    ('pid', int  ),
])

kernel = lgp.ExpQuad(dim='x') * lgp.White(dim='pid')

# grid of points to which we apply the transformation
xdata = np.empty((nflav, nx), xtype)
xdata['pid'] = pid[:, None]
xdata[  'x'] = np.linspace(0, 1, nx)

# linear map PDF(xdata) -> data
Mcomps = np.random.randn(rankmcov, ndata, nflav, nx)
Mcomps /= np.sqrt(Mcomps.size / ndata)
Mparams = gvar.gvar(np.random.randn(rankmcov), np.full(rankmcov, 0.1))
M = lambda params: jnp.tensordot(params, Mcomps, 1)

# quadratic map PDF(xdata) -> data2
M2comps = np.random.randn(rankmcov2, ndata2, nflav, nx2, nx2)
M2comps /= 2 * np.sqrt(M2comps.size / ndata2)
M2comps = (M2comps + np.swapaxes(M2comps, -1, -2)) / 2
M2params = gvar.gvar(np.random.randn(rankmcov2), np.full(rankmcov2, 0.1))
M2 = lambda params: jnp.tensordot(params, M2comps, 1)

# endpoints of the integral for each PDF
xinteg = np.empty((nflav, 2), xtype)
xinteg['pid'] = pid[:, None]
xinteg[  'x'] = [0, 1]

# matrix to subtract the endpoints
suminteg = np.empty(xinteg.shape)
suminteg[:, 0] = -1
suminteg[:, 1] =  1

constraints = {
    'momrule': 1,
    'uubar'  : 2,
    'ddbar'  : 1,
    'ccbar'  : 0,
    'ssbar'  : 0,
}

#### GP OBJECT ####

gp = lgp.GP()

gp.addproc(kernel, 'h')
gp.addproctransf({'h': 1}, 'primitive', deriv='x'     )
gp.addproctransf({'h': 1}, 'f'        , deriv=(2, 'x'))
gp.addproctransf({
    'primitive': lambda x: x['x'],
    'h'        : -1,
}, 'primitive of xf(x)')

gp.addx(xdata, 'xdata', proc='f')

# linear data (used for warmup fit)
gp.addtransf({'xdata': M(gvar.mean(Mparams))}, 'data', axes=2)

# total momentum rule
gp.addx(xinteg, 'xmomrule', proc='primitive of xf(x)')
gp.addtransf({'xmomrule': suminteg}, 'momrule', axes=2)

# quark sum rules
qdiff = np.array([1, -1])[:, None] # vector to subtract two quarks
for quark in 'ducs':
    idx = indices[quark] # [quark, antiquark] indices
    label = f'{quark}{quark}bar' # the one appearing in `constraints`
    xlabel = f'x{label}'
    gp.addx(xinteg[idx], xlabel, proc='primitive')
    gp.addtransf({xlabel: suminteg[idx] * qdiff}, label, axes=2)
    
#### NONLINEAR FUNCTION ####

def fcn(params):
    
    xdata = params['xdata']
    Mparams = params['Mparams']
    M2params = params['M2params']
    
    data = jnp.tensordot(M(Mparams), xdata, 2)
    
    # data2 = np.einsum('dfxy,fx,fy->d', M2, xdata, xdata)
    # np.einsum does not work with gvar
    xdata2 = xdata[:, None, :nx2] * xdata[:, :nx2, None]
    data2 = jnp.tensordot(M2(M2params), xdata2, 3)
    
    return jnp.concatenate([data, data2])

prior = gp.predfromdata(constraints, ['xdata'])
prior['Mparams'] = Mparams
prior['M2params'] = M2params

gvar._bufferdict.numpy = jnp

inp = gvar.mean(prior).buf

hackfcn = lambda x: fcn(gvar.BufferDict(prior, buf=x))
jacf = jax.jit(jax.jacfwd(hackfcn))
jacr = jax.jit(jax.jacrev(hackfcn))

jacf(inp)
jacr(inp)
