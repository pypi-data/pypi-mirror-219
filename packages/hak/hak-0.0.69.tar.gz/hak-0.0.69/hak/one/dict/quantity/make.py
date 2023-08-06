from hak.pxyz import f as pxyz
from hak.one.string.print_and_return_false import f as pf

def f(value, unit): return {'value': value, 'unit': unit}

def t_true():
  x = {'value': 0, 'unit': 'm'}
  y = {'value': 0, 'unit': 'm'}
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_true(): return pf('!t_true')
  return True
