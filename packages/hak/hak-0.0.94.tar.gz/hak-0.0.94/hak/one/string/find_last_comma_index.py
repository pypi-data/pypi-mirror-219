from hak.one.string.print_and_return_false import f as pf

f = lambda x: len(x)-x[::-1].find(',')-1

def t():
  x = 'a,b,c,de'
  y = 5
  z = f(x)
  return y == z or pf(['y != z', f'x: {x}', f'y: {y}', f'z: {z}'])
