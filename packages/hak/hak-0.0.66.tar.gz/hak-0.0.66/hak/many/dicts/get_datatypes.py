from hak.many.dicts.get_all_keys import f as get_field_names
from hak.many.values.get_datatype import f as detect_datatype_from_values
from hak.one.string.print_and_return_false import f as pf

# src.table.fields.datatypes.get
f = lambda x: {
  k: detect_datatype_from_values([d[k] if k in d else None for d in x])
  for k in get_field_names(x)
}

def t():
  x = [
    {'a': True, 'b': 'abc'},
    {'a': True, 'b': 'def'},
    {'a': False, 'b': 'ghi'},
  ]
  y = {'a': 'bool', 'b': 'str'}
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
