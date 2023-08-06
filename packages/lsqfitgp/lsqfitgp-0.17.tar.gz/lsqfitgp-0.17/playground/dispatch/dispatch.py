import functools
import typing

@functools.singledispatch
def f(_):
    print('not dispatched')

@f.register
def _(_: typing.Union[str, int]):
    print('dispatched')

f(None)
f('')
f(0)
