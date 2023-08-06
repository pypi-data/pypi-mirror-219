import gvar
import numpy as np

v = np.ones(2)
i = np.arange(2)
sv = gvar.svec(0)
sv._assign(v, i)

v.flags['WRITEABLE'] = False
sv._assign(v, i)
