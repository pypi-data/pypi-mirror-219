from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

def f(x):
  if x['denominator'] == 0: raise ZeroDivisionError('denominator must not be 0')
  return x['numerator']/x['denominator']

def t_int_as_float():
  x = make_rate(2, 1, '1')
  y = type(2.0)
  z = type(f(x))
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_float():
  x = make_rate(1, 2, '1')
  y = type(0.5)
  z = type(f(x))
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t():
  if not t_int_as_float(): return pf('!t_int_as_float')
  if not t_float(): return pf('!t_float')
  return True
