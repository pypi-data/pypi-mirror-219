from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# make_bar
f = lambda x: "|-"+'-|-'.join(['-'*x['widths'][k] for k in x['names']])+"-|"

def t():
  x = {
    'widths': {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6},
    'names': list('abcde'),
  }
  y = '|----|-----|------|-------|--------|'
  z = f(x)
  return pxyz(x, y, z)
