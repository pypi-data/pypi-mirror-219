from copy import deepcopy
from hak.one.string.print_and_return_false import f as pf

# apply_custom_order
def f(x):
  field_order = deepcopy(x['field_order'])
  field_names = [n for n in x['field_names'] if n not in field_order]
  return field_order + field_names

def t():
  x = {'field_order': list('cba'), 'field_names': list('abcdef')}
  y = ['c', 'b', 'a', 'd', 'e', 'f']
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
