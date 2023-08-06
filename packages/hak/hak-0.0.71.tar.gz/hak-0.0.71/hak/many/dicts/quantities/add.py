from hak.one.dict.quantity.make import f as make_quantity
from hak.pxyz import f as pxyz

def f(u, v):
  if u['unit'] == v['unit']:
    return make_quantity(value=u['value']+v['value'], unit=u['unit'])
  else:
    ValueError(f"mismatched units: u['unit']:{u['unit']} v['unit']:{v['unit']}")

def t():
  x = {'u': make_quantity(1, 'm'), 'v': make_quantity(2, 'm')}
  y = make_quantity(3, 'm')
  z = f(**x)
  return pxyz(x, y, z)
