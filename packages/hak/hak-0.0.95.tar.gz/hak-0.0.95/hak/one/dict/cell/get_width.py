from hak.one.dict.cell.to_str import f as to_str
from hak.one.string.colour.bright.red import f as red
from hak.one.string.colour.decolour import f as decol
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.is_a import f as is_rate
from hak.one.dict.rate.to_float import f as to_float
from hak.one.dict.rate.to_str_frac import f as to_str_frac
from hak.pxyz import f as pxyz
from hak.one.dict.unit.to_str import f as unit_to_str

def f(x):
  val = x['value']
  unit_width = len(unit_to_str(val['unit'])) if is_rate(val) else 0
  header_word_widths = [len(i) for i in x['field_name'].split('_')]

  if x['field_name'].startswith('rate_'):
    val_str = to_str_frac(val) if is_rate(val) else ''
  else:
    val_str = to_str(to_float(val) if is_rate(val) else val)
  
  value_str_width = len(decol(val_str))

  return max([*header_word_widths, value_str_width, unit_width])

def t_0():
  x = {'value': False, 'field_name': 'a'}
  y = 1
  z = f(x)
  return pxyz(x, y, z)

def t_1():
  x = {'value': 'a', 'field_name': 'aa'}
  y = 2
  z = f(x)
  return pxyz(x, y, z)

def t_2():
  x = {'value': red('-'), 'field_name': 'is_revenue'}
  y = len('revenue')
  z = f(x)
  return pxyz(x, y, z)

def t_quantity_short_unit():
  x = {'value': make_rate(12.34, 1, {'m': 1}), 'field_name': 'length'}
  y = len('length')
  z = f(x)
  return pxyz(x, y, z)

def t_quantity_long_unit():
  x = {
    'value': make_rate(
      12.34,
      1,
      {'lightyear': 1}
    ),
    'field_name': 'length'
  }
  y = len('lightyear')
  z = f(x)
  return pxyz(x, y, z)

def t_k_starts_with_rate():
  x = {
    'value': make_rate(547200, 735089, {'USD': 1, 'AUD': -1}),
    'field_name': 'rate_USD_per_AUD'
  }
  y = len('547200/735089')
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  if not t_quantity_short_unit(): return pf('!t_quantity_short_unit')
  if not t_quantity_long_unit(): return pf('!t_quantity_long_unit')
  if not t_k_starts_with_rate(): return pf('!t_k_starts_with_rate')
  return True
