from hak.one.string.print_and_return_false import f as pf
from hak.one.number.int.primes.prime_factors.get import f as get_prime_factors
from hak.pxyz import f as pxyz

# __init__
def f(numerator, denominator):
  if isinstance(numerator, dict):
    numerator = numerator['numerator']/numerator['denominator']

  if isinstance(numerator, float):
    decimal_place_count = len(str(numerator).split('.')[1].rstrip('0'))
    numerator *= 10**decimal_place_count
    denominator *= 10**decimal_place_count
    numerator = int(numerator)
    denominator = int(denominator)

  npf = get_prime_factors(numerator)
  dpf = get_prime_factors(denominator)

  common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  while common_factors:
    common_factor = common_factors.pop()
    numerator //= common_factor
    denominator //= common_factor
    npf = get_prime_factors(numerator)
    dpf = get_prime_factors(denominator)
    common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  return {'numerator': numerator, 'denominator': denominator}

def t_a():
  x = {'numerator': 10, 'denominator': 20}
  y = {'numerator':  1, 'denominator':  2}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t_b():
  x = {'numerator': 0.1, 'denominator': 0.2}
  y = {'numerator': 1, 'denominator': 2}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t_c():
  x = {'numerator': 100, 'denominator': 4}
  y = {'numerator':  25, 'denominator': 1}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t_d():
  x = {'numerator': 25.0, 'denominator': 1}
  y = {'numerator': 25, 'denominator': 1}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t_e():
  x = {'numerator': 80, 'denominator': 4}
  y = {'numerator': 20, 'denominator': 1}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t_f():
  x = {'numerator': 0.7093094658085993, 'denominator': 1}
  y = {'numerator': 7093094658085993, 'denominator': 10**16}
  z = f(x['numerator'], x['denominator'])
  return pxyz(x, y, z)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  return True
