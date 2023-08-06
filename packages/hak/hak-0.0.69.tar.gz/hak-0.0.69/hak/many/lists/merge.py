f = lambda _L_a, _L_b: _L_a + [_l_b for _l_b in _L_b if _l_b not in set(_L_a)]

t = lambda: all([
  [] == f([], []),
  list('abcdef') == f(list('abc'), list('def')),
  list('abcd') == f(list('abc'), list('bcd')),
])
