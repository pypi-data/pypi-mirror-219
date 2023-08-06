from hak.one.string.colour.bright.cyan import f as cy
from hak.one.string.colour.bright.magenta import f as mg
from hak.one.string.colour.bright.yellow import f as yl
from hak.many.strings.find_first_diff import f as find_first_diff
from hak.one.string.print_and_return_false import f as pf

# show_diff

def f(u, v, w=64):
  u = str(u)
  v = str(v)
  i = find_first_diff(u, v)['i']
  return [
    str(i),
    cy(u[i-w:i]) + yl(u[i]) + cy(u[i+1:i+w]),
    mg(v[i-w:i]) + yl(v[i]) + mg(v[i+1:i+w]),
  ]

def t():
  x_u = 'abcdef'
  x_v = 'abxdef'
  y = [
    '2',
    '\x1b[1;36mab\x1b[0;0m\x1b[1;33mc\x1b[0;0m\x1b[1;36mdef\x1b[0;0m',
    '\x1b[1;35mab\x1b[0;0m\x1b[1;33mx\x1b[0;0m\x1b[1;35mdef\x1b[0;0m'
  ]
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}'])
