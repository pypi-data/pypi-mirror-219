from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.cell.get_width import f as get_w

f = lambda x: {
  k: max([
    get_w({'value': r[k] if k in r else None, 'field_name': k})
    for r in x['records']
  ])
  for k in x['field_names']
}

def t():
  x = {
    'field_names': list('abcde'),
    'records': [
      {'a':  0, 'b':  1, 'c':  2, 'd':  3, 'e':  4},
      {'a':  5, 'b':  6, 'c':  7, 'd':  8, 'e':  9},
      {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14},
    ]
  }
  y = {k: 2 for k in list('abcde')}
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
