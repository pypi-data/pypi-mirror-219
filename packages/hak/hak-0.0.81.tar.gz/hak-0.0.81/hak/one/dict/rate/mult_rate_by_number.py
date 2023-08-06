from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.is_a import f as is_rate
from hak.one.number.is_a import f as is_num

def f(u, v):
  if not is_rate(u): raise ValueError(f'u: {u} is not a rate')
  if not is_num(v): raise ValueError(f'v: {v} is not a number')
  return make_rate(u['numerator']*v, u['denominator'], '1')

def t_a():
  u = {'numerator': 1, 'denominator': 3, 'unit': '1'}
  v = 1
  y = {'numerator': 1, 'denominator': 3, 'unit': '1'}
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t_b():
  u = {'numerator':  9, 'denominator': 7, 'unit': '1'}
  v = 5
  y = {'numerator': 45, 'denominator': 7, 'unit': '1'}
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t_c():
  u = {'numerator': 1, 'denominator': 3, 'unit': '1'}
  v = 3
  y = {'numerator': 1, 'denominator': 1, 'unit': '1'}
  z = f(u, v)
  return y == z or pf([f"u: {u}", f"v: {v}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return True
