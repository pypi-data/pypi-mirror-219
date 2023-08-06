from hak.other.pip.version.to_str import f as make_v_str
from hak.one.string.contains.version import f as k

f = lambda v, _L: [
  (f"  version='{make_v_str(v)}'," if k(_l) else _l) for _l in _L
]

v = {'major': 4, 'minor': 5, 'patch': 6}

t = lambda: all([
  [] == f({}, []),
  [] == f(v, []),
  ["  version='4.5.6',", '.\n'] == f(v, ["version = '1.2.3'\n", '.\n']),
  ['.\n', "  version='4.5.6',"] == f(v, ['.\n', "version = '1.2.3'\n"]),
])
