from hak.one.dict.is_a import f as is_dict
from hak.pxyz import f as pxyz
from hak.one.string.print_and_return_false import f as pf
from hak.one.string.is_a import f as is_str
from hak.one.number.is_a import f as is_num

# is_quantity
def f(x):
  if not is_dict(x): return False
  if 'value' not in x: return False
  if 'unit' not in x: return False
  if len(x.keys()) != 2: return False
  if not is_str(x['unit']): return False
  if not is_num(x['value']): return False
  return True

def t_true():
  x = {'value': 1, 'unit': 'm'}
  y = True
  z = f(x)
  return pxyz(x, y, z)

def t_false_too_many_keys():
  x = {'value': 1, 'unit': 'm', 'boo': '...'}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_too_few_keys():
  x = {'value': 1}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_wrong_keys():
  x = {'value': 1, 'boo': 'm'}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_unit_not_string():
  x = {'value': 1, 'unit': 1}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_not_dict():
  x = 1
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_value_not_number():
  x = {'value': '1', 'unit': 'm'}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_true(): return pf('!t_true')
  if not t_false_too_many_keys(): return pf('!t_false_too_many_keys')
  if not t_false_too_few_keys(): return pf('!t_false_too_few_keys')
  if not t_wrong_keys(): return pf('!t_wrong_keys')
  if not t_false_unit_not_string(): return pf('!t_false_unit_not_string')
  if not t_false_not_dict(): return pf('!t_false_not_dict')
  if not t_false_value_not_number(): return pf('!t_false_value_not_number')
  return True
