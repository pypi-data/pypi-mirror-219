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

  return make_rate(
    (
      u['numerator'] * v['denominator'] -
      v['numerator'] * u['denominator']
    ),
    u['denominator'] * v['denominator']
  )

def t_a():
  u = {'numerator': 1, 'denominator': 2}
  v = {'numerator': 1, 'denominator': 3}
  y = {'numerator': 1, 'denominator': 6}
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t_b():
  u = {'numerator':   2, 'denominator':  5}
  v = {'numerator':   7, 'denominator':  9}
  y = {'numerator': -17, 'denominator': 45}
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
