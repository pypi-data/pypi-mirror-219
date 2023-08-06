from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.period.financial_year.make import f as mkfy

# gt
f = lambda u, v: u['start_year'] > v['start_year']

def t():
  u = mkfy({'start_year': 2023})
  v = mkfy({'final_year': 2023})
  y = True
  z = f(u, v)
  return y == z or pf([f'u: {u}', f'v: {v}', f'y: {y}', f'z: {z}'])
