from math import sqrt
from hak.one.string.colour.bright.cyan import f as cy
from hak.one.string.print_and_return_false import f as pf

f = lambda x: all([x%i for i in range(2, x)])

def t():
  for (x, y) in [
    *[(_, False) for _ in [4, 6, 8, 9, 10, 12, 14, 15, 16, 180]],
    *[(_, True) for _ in [2, 3, 5, 7, 11, 13, 17]]
  ]:
    z = f(x)
    if z != y: return pf([cy(f'x: {x}'), cy(f'y: {y}'), cy(f'z: {z}'), ''])
  return True
