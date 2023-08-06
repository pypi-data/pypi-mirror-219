from hak.one.bool.is_a import f as is_bool
from hak.one.dict.rate.is_a import f as is_a_rate
from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.to_str import f as rate_to_str
from hak.one.number.float.is_a import f as is_float
from hak.one.string.colour.bright.green import f as g
from hak.one.string.colour.bright.red import f as r
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# src.cell.to_str
def f(x):
  if is_a_rate(x): return rate_to_str(x)
  if is_bool(x): return g('Y') if x else r('N')
  if x is None: return ' '
  if x == 0: return ' '
  if is_float(x): return f'{x:.2f}'
  return str(x)

def t_0():
  x = 0
  y = ' '
  z = f(x)
  return pxyz(x, y, z)

def t_1():
  x = 'a'
  y = str(x)
  z = f(x)
  return pxyz(x, y, z)

def t_2():
  x = False
  y = r('N')
  z = f(x)
  return pxyz(x, y, z)

def t_3():
  x = True
  y = g('Y')
  z = f(x)
  return pxyz(x, y, z)

def t_4():
  x = None
  y = ' '
  z = f(x)
  return pxyz(x, y, z)

def t_5():
  x = 1.0
  y = '1.00'
  z = f(x)
  return pxyz(x, y, z)

def t_6():
  x = make_rate(710, 113)
  y = '6.283186'
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  if not t_3(): return pf('t_3 failed')
  if not t_4(): return pf('t_4 failed')
  if not t_5(): return pf('t_5 failed')
  if not t_6(): return pf('t_6 failed')
  return True
