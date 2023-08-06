from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

def f(x):
  if not isinstance(x, dict): return False
  if not 'numerator' in x: return False
  if not 'denominator' in x: return False
  return True

def t_true():
  x = make_rate(1, 2)
  y = True
  z = f(x)
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_false():
  x = 'abc'
  y = False
  z = f(x)
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t():
  if not t_true(): return pf('!t_true()')
  if not t_false(): return pf('!t_false()')
  return True
