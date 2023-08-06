from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

# __eq__
f = lambda u, v: make_rate(**u) == make_rate(**v)

def t_true_a():
  x_u = make_rate(  1,   2, {'1': 0})
  x_v = make_rate(1.0, 2.0, {'1': 0})
  y = True
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t_true_b():
  x_u = make_rate( 0.25, 0.5, {'1': 0})
  x_v = make_rate(10, 20, {'1': 0})
  y = True
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t_false():
  x_u = make_rate(1, 2, {'1': 0})
  x_v = make_rate(2, 3, {'1': 0})
  y = False
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t_false_different_units():
  x_u = make_rate(1, 2, {'a': 1})
  x_v = make_rate(2, 3, {'b': 1})
  y = False
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t():
  if not t_true_a(): return pf('!t_true()')
  if not t_true_b(): return pf('!t_true()')
  if not t_false(): return pf('!t_false()')
  if not t_false_different_units(): return pf('!t_false_different_units')
  return True
