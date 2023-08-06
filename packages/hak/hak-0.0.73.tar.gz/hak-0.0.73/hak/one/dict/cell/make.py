from hak.one.dict.cell.to_str import f as to_str
from hak.one.string.colour.decolour import f as decol
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.one.dict.quantity.make import f as make_quantity
from datetime import date
from hak.one.dict.get_or_default import f as get_or_default
from hak.one.dict.quantity.is_a import f as is_quantity

# make_cell
# src.cell.make
def f(x):
  val = x['value']['value'] if is_quantity(x['value']) else x['value']
  _val_str = to_str(val)
  
  _width = x['width']
  
  _ = _width - len(decol(f'{_val_str:>{_width}}'))
  left_pad = ' '*_

  return left_pad + f'{_val_str:>{_width}}'

def t_0():
  # cell_dict
  x = {'value': 'a', 'width': 1}
  y = 'a'
  z = f(x)
  return pxyz(x, y, z)

def t_quantity():
  x = {'value': make_quantity(1, 'm'), 'width': 1}
  y = '1'
  z = f(x)
  return pxyz(x, y, z)

def t_date():
  x = {'value': date(2022, 4, 5), 'width': len('2022-04-05')}
  y = '2022-04-05'
  z = f(x)
  return pxyz(x, y, z)

def t_description():
  x = {'value': 'Purchased USD with AUD'}
  x['width'] = len('Purchased USD with AUD')
  y = 'Purchased USD with AUD'
  z = f(x)
  return pxyz(x, y, z)

def t_USD_quantity():
  x = {'value': {'value': 5472.0, 'unit': 'USD'}, 'width': 8}
  y = ' 5472.00'
  z = f(x)
  return pxyz(x, y, z)

def t_asset_nabtrade_cash_AUD():
  x = {'value': {'value': -7350.89, 'unit': 'AUD'}, 'width': 8}
  y = '-7350.89'
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_quantity(): return pf('t_quantity failed')
  if not t_date(): return pf('!t_date')
  if not t_description(): return pf('!t_description')
  if not t_USD_quantity(): return pf('!t_USD_quantity')
  if not t_asset_nabtrade_cash_AUD(): return pf('!t_asset_nabtrade_cash_AUD')
  return True
