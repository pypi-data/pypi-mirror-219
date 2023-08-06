from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

def f(u, v):
  if not isinstance(u, dict):
    print(f'u: {u}')
    print(f'v: {v}')
    raise ValueError(f'u: {u} is not a dict')
  
  if not isinstance(v, dict):
    print(f'u: {u}')
    print(f'v: {v}')
    raise ValueError(f'v: {v} is not a dict')
  
  if u['unit'] != v['unit']:
    raise ValueError(f"u['unit']: {u['unit']} != v['unit']: {v['unit']}")

  return make_rate(
    (
      u['numerator'] * v['denominator'] -
      v['numerator'] * u['denominator']
    ),
    u['denominator'] * v['denominator'],
    u['unit']
  )

def t_a():
  u = make_rate(1, 2, 'a')
  v = make_rate(1, 3, 'a')
  y = make_rate(1, 6, 'a')
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t_b():
  u = make_rate(  2,  5, 'b')
  v = make_rate(  7,  9, 'b')
  y = make_rate(-17, 45, 'b')
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t_different_units():
  u = make_rate( 2,  5, 'a')
  v = make_rate( 7,  9, 'b')
  y = "u['unit']: a != v['unit']: b"
  try:
    z = f(u, v)
  except ValueError as ve:
    z = str(ve)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_different_units(): return pf('!t_different_units')
  return True
