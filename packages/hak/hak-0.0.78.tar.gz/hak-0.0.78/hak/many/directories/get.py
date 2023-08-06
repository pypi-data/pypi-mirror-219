from os.path import isdir

from hak.one.directory.filepaths.get import f as get_filepaths
from hak.one.directory.make import f as mkd
from hak.one.directory.remove import f as rmd
from hak.one.string.print_and_return_false import f as pf

f = lambda root: set([p for p in get_filepaths(root=root) if isdir(p)])

def up():
  x = {'root': mkd('./_temp')}
  x['created'] = set([mkd(d) for d in [f"{x['root']}/a", f"{x['root']}/b"]])
  return x

dn = lambda x: rmd(x['root'])

def t():
  x = up()
  y = x['created']
  z = f(x['root'])
  dn(x)
  return y == z or pf(['y != z', f'x: {x}', f'y: {y}', f'z: {z}'])
