from hak.one.dict.cell.to_str import f as to_str
from hak.one.string.colour.decolour import f as decol
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# make_cell
# src.cell.make
def f(x):
  # r, k, widths, field_datatypes_by_key
  
  # field_name = k
  _field_name = x['field_name']
  
  # value = r[field_name]
  _val_str = to_str(x['value'])
  
  # _width = widths[_field_name]
  _width = x['width']
  
  _ = _width - len(decol(f'{_val_str:>{_width}}'))
  left_pad = ' '*_

  return left_pad + f'{_val_str:>{_width}}'

def t_0():
  # cell_dict
  x = {
    'value': 'a',
    'field_name': 'A',
    # 'type': 'str',
    'width': 1
  }
  y = 'a'
  z = f(x)
  return pxyz(x, y, z)

def t_1():
  x = {
    'value': 'a',
    'field_name': 'A',
    # 'type': 'str',
    'width': 1
  }
  y = 'a'
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  return True
