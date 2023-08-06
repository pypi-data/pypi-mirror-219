from hak.one.dict.cell.to_str import f as to_str
from hak.one.string.colour.bright.red import f as red
from hak.one.string.colour.decolour import f as decol
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.quantity.make import f as make_quantity
from hak.one.dict.quantity.is_a import f as is_quantity

def f(x):
  val = x['value']
  
  unit_width = len(val['unit']) if is_quantity(val) else 0

  if is_quantity(val):
    val = val['value']

  return max([
    *[len(i) for i in x['field_name'].split('_')],
    len(decol(to_str(val))),
    unit_width
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

def t_quantity_short_unit():
  x = {'value': make_quantity(12.34, 'm'), 'field_name': 'length'}
  y = len('length')
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t_quantity_long_unit():
  x = {'value': make_quantity(12.34, 'lightyear'), 'field_name': 'length'}
  y = len('lightyear')
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  if not t_quantity_short_unit(): return pf('t_quantity_short_unit failed')
  if not t_quantity_long_unit(): return pf('t_quantity_long_unit failed')
  return True
