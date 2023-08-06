from hak.one.string.format import f as format_one

f = lambda _l, fn=format_one: [fn(_pi) for _pi in _l]

t = lambda: list('abc') == f(list('abc'), lambda x: x)
