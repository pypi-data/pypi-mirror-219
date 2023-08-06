from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.to_float import f as to_float
from hak.pxyz import f as pxyz

# __str__
f = lambda x: f"{to_float(x):.6f}"

def t():
  x = {'numerator': 710, 'denominator': 113}
  y = '6.283186'
  z = f(make_rate(x['numerator'], x['denominator']))
  return pxyz(x, y, z)
