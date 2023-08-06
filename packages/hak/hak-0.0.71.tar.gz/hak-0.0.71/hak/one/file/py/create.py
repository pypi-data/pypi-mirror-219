from hak.one.directory.make import f as mkdirine
from hak.one.directory.remove import f as rmdir
from hak.one.file.load import f as load
from hak.one.file.remove import f as remove
from hak.one.file.save import f as save

f = lambda filename, data: save(filename, data)
_dirname = './temp'
_filename = f'{_dirname}/foo.py'
_data = '\n'.join(["f = lambda: None", "t = lambda: False", ""])
up = lambda: mkdirine(_dirname)
dn = lambda: [remove(_filename), rmdir(_dirname)]

def t():
  up()
  y = _data
  f(_filename, _data)
  z = load(_filename)
  dn()
  return y == z
