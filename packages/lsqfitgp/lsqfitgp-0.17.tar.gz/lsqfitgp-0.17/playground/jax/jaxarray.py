import jax

ArrayMeta = type(jax.numpy.ndarray)

class JaxArray(metaclass=ArrayMeta): pass

class ndarray(jax.numpy.ndarray, JaxArray):
    """replacement for jax.numpy.ndarray"""
    pass

jax.numpy.ndarray = ndarray
jax._src.numpy.lax_numpy.ndarray = ndarray

x = jax.numpy.zeros(5)

print(isinstance(x, JaxArray))
print(issubclass(type(x), JaxArray)) # -> False, not really working
