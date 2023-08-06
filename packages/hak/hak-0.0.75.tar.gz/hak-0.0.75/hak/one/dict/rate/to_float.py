from hak.one.string.print_and_return_false import f as pf

def f(x):
  if not isinstance(x, dict): raise ValueError(f'{x} is not a dict')
  if 'numerator' not in x: raise KeyError(f'{x} is missing numerator key')
  if 'denominator' not in x: raise KeyError(f'{x} is missing denominator key')
  return (
    0 if (x == 0 or (x['numerator'] == 0 and x['denominator'] == 0)) else
    x['numerator']/x['denominator']
  )

def t_a():
  x = {'numerator': 1, 'denominator': 2}
  y = 0.5
  z = f(x)
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  return True
