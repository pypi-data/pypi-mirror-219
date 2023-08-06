# ignore_overlength_lines
from hak.one.string.print_and_return_false import f as pf
from hak.one.string.colour.bright.cyan import f as cy
from hak.one.string.colour.bright.blue import f as bl
from hak.one.string.colour.bright.magenta import f as mg
from hak.one.string.char.last.find import f as find_last

def t_short():
  x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
  y = "{'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}"
  z = f(x)
  return y == z or pf(['y != z', f'x: {x}', f'y: {y}', f'z: {z}'])

def t_w():
  x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
  y = "{'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}"
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x:   {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t_too_long_a():
  x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 10}
  y = '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 10",
    "}",
  ])
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t_too_long_b():
  x = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
    'j': 9, 'k': 10
  }
  y = '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10",
    "}",
  ])
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t_too_long_c():
  x = {chr(k+97): k for k in range(17)}
  y = '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16",
    "}",
  ])
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t_too_long_d():
  x = {chr(k+97): k for k in range(18)}
  y = '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
    "  'r': 17",
    "}",
  ])
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t_too_long_e():
  x = {chr(k+97): k for k in range(26)}
  y = '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
    "  'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,",
    "  'z': 25",
    "}",
  ])
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])

def t():
  if not t_short(): return pf('t_short() failed')
  if not t_w(): return pf('t_w() failed')
  if not t_too_long_a(): return pf('t_too_long_a() failed')
  if not t_too_long_b(): return pf('t_too_long_b() failed')
  if not t_too_long_c(): return pf('t_too_long_c() failed')
  if not t_too_long_d(): return pf('t_too_long_d() failed')
  if not t_too_long_e(): return pf('t_too_long_e() failed')
  return True

def get_last_line_width(x):
  return (len(x) - find_last(x, '\n')) if '\n' in x else len(x)

def insert_nl_at_best_location(x):
  last_new_line_index = (len(x) - x[::-1].find('\n') -1) if '\n' in x else 0
  raw_comma_indices = [x.find(', ', last_new_line_index+i) for i in range(80)]
  comma_indices = [
    _ for _ in raw_comma_indices if all([_ >= 0, _-last_new_line_index < 78])
  ]
  q = max(comma_indices)+1
  l = x[:q]
  r = x[q+1:]
  x = l+'\n  '+r
  return x

def f_d(x, w=80):
  _x = str(x)
  if len(_x) <= w: return _x

  result = ', '.join([f"'{k}': {x[k]}" for k in x])
  
  while get_last_line_width(result) > w-2:
    result = insert_nl_at_best_location(result)

  return '{\n  '+result+'\n}'

f = lambda x: f_d(x)
