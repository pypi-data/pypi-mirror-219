from hak.one.string.print_and_return_false import f as pf

f = lambda x: sorted(list(set([k for d in x for k in d.keys()])))

def t():
  x = [
    {'a': True, 'b': True},
    {'a': True, 'b': False},
    {'a': False, 'b': False},
    {'a': False, 'b': True, 'c': None}
  ]
  y = ['a', 'b', 'c']
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
