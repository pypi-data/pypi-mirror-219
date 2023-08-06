from hak.one.directory.make import f as mkdir
from hak.one.file.save import f as save
from string import ascii_lowercase as az
from hak.one.directory.remove import f as rmdir
from os import listdir
from hak.one.file.remove import f as remove
from hak.one.string.print_and_return_false import f as pf
from os.path import isfile

up = lambda x: [mkdir(x), *[save(f'{x}/{_}.txt', _) for _ in az]]
dn = lambda x: rmdir(x)

f = lambda x: [remove(f'{x}/{n}') for n in listdir(x) if isfile(f'{x}/{n}')]
# f = lambda x: [remove(f'{x}/{n}') for n in listdir(x)]

def t():
  x = './temp'
  up(x)
  α = len(listdir(x))
  f(x)
  ω = len(listdir(x))
  result = all([α>ω, ω==0])
  dn(x)
  return result or pf([f'α: {α}', f'ω: {ω}'])
