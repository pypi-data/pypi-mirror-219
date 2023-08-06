from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.to_float import f as to_float
from hak.pxyz import f as pxyz

# __str__
f = lambda x: f"{x['numerator']}/{x['denominator']}"

def t():
  x = {'numerator': 710, 'denominator': 113}
  y = '710/113'
  z = f(make_rate(x['numerator'], x['denominator'], '1'))
  return pxyz(x, y, z)
