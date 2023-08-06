from hak.one.dict.cell.to_str import f as to_str
from hak.one.string.colour.bright.red import f as red
from hak.one.string.colour.decolour import f as decol
from hak.one.string.print_and_return_false import f as pf

def f(x): return max([
  *[len(i) for i in x['field_name'].split('_')],
  len(decol(to_str(x['value'])))
])

def t_0():
  x = {'value': False, 'field_name': 'a'}
  y = 1
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t_1():
  x = {'value': 'a', 'field_name': 'aa'}
  y = 2
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t_2():
  x = {'value': red('-'), 'field_name': 'is_revenue'}
  y = len('revenue')
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  return True
