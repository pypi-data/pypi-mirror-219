from copy import deepcopy
from hak.pxyz import f as pxyz

# apply_custom_order
def f(x):
  field_order = deepcopy(x['field_order'])
  field_names = [n for n in x['field_names'] if n not in field_order]
  return field_order + field_names

def t():
  x = {'field_order': list('cba'), 'field_names': list('abcdef')}
  y = ['c', 'b', 'a', 'd', 'e', 'f']
  z = f(x)
  return pxyz(x, y, z)
