from hak.one.string.print_and_return_false import f as pf

# make_bar
f = lambda x: (
  "|-"+'-|-'.join(['-'*x['field_widths'][k] for k in x['field_names']])+"-|"
)

def t():
  x = {
    'field_widths': {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6},
    'field_names': list('abcde'),
  }
  y = '|----|-----|------|-------|--------|'
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
