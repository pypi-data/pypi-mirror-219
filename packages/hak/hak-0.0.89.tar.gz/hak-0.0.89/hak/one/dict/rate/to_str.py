from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.to_float import f as to_float
from hak.pxyz import f as pxyz
from hak.one.dict.rate.make import f as make_rate

# __str__
f = lambda x: f"{to_float(x):.2f}"

def t():
  x = make_rate(710, 113, '1')
  y = '6.28'
  z = f(make_rate(x['numerator'], x['denominator'], '1'))
  return pxyz(x, y, z)
