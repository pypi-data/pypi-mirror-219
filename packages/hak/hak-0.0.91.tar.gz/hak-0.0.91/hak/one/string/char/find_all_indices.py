from hak.one.string.print_and_return_false import f as pf

f = lambda x_str, x_char: [i for (i, c) in enumerate(x_str) if c == x_char]

def t():
  x_str = 'a,b,c,defg'
  x_char = ','
  y = [1, 3, 5]
  z = f(x_str, x_char)
  return y == z or pf([
    'y != z', f'x_str: {x_str}', f'x_char: {x_char}', f'y: {y}', f'z: {z}'
  ])
