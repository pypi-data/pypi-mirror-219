from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

def f(x):
  if not isinstance(x, dict): raise ValueError(f'x: {x} is not a dict')
  return make_rate(abs(x['numerator']), abs(x['denominator']))

def t_a():
  x = {'numerator': -1, 'denominator': 3}
  y = {'numerator':  1, 'denominator': 3}
  z = f(x)
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_b():
  x = {'numerator': 45, 'denominator': -7}
  y = {'numerator': 45, 'denominator':  7}
  z = f(x)
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
