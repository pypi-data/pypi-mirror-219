from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate

# __eq__
f = lambda u, v: make_rate(**u) == make_rate(**v)

def t_true_a():
  x_u = {'numerator': 1, 'denominator': 2}
  x_v = {'numerator': 1.0, 'denominator': 2.0}
  y = True
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t_true_b():
  x_u = {'numerator': 0.25, 'denominator': 0.5}
  x_v = {'numerator': 10, 'denominator': 20}
  y = True
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t_false():
  x_u = {'numerator': 1, 'denominator': 2}
  x_v = {'numerator': 2, 'denominator': 3}
  y = False
  z = f(x_u, x_v)
  return y == z or pf([f"x_u: {x_u}", f"x_v: {x_v}", f"y: {y}", f"z: {z}"])

def t():
  if not t_true_a(): return pf('!t_true()')
  if not t_true_b(): return pf('!t_true()')
  if not t_false(): return pf('!t_false()')
  return True
