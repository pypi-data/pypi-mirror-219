from hak.one.string.colour.bright.magenta import f as mg
from hak.one.string.colour.bright.cyan import f as cy
from hak.one.string.print_and_return_false import f as pf

_f = lambda u_i, v_i, i: {'u_i': u_i, 'v_i': v_i, 'i': i}

def f(u, v):
  if u == v: return None
  if len(u) < len(v): return f(u, v[:len(u)]) or _f(None, v[len(u)], len(u))
  if len(u) > len(v): return f(u[:len(v)], v) or _f(u[len(v)], None, len(v))
  return [_f(u[i], v[i], i) for i in range(len(u)) if u[i] != v[i]][0]

def t_diff_strs_same_length():
  x_u = 'abcde'
  x_v = 'abxde'
  y = {'u_i': 'c', 'v_i': 'x', 'i': 2}
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t_matching_strs():
  x_u = 'abcde'
  x_v = 'abcde'
  y = None
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t_isoprefix_u_len_lt_v_len():
  x_u = 'abcd'
  x_v = 'abcdxfg'
  y = {'u_i': None, 'v_i': 'x', 'i': 4}
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t_isoprefix_u_len_gt_v_len():
  x_u = 'abcdxfg'
  x_v = 'abcd'
  y = {'u_i': 'x', 'v_i': None, 'i': 4}
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t_diff_str_u_len_lt_v_len():
  x_u = 'abcd'
  x_v = 'axcdefg'
  y = {'u_i': 'b', 'v_i': 'x', 'i': 1}
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t_diff_str_u_len_gt_v_len():
  x_u = 'axcdefg'
  x_v = 'abcd'
  y = {'u_i': 'x', 'v_i': 'b', 'i': 1}
  z = f(x_u, x_v)
  return y == z or pf([
    'y != z', f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z: {z}'
  ])

def t():
  if not t_matching_strs(): return pf('!t_matching_strs')
  if not t_diff_strs_same_length(): return pf('!t_diff_strs_same_length')
  if not t_isoprefix_u_len_lt_v_len(): return pf('!t_isoprefix_u_len_lt_v_len')
  if not t_isoprefix_u_len_gt_v_len(): return pf('!t_isoprefix_u_len_gt_v_len')
  if not t_diff_str_u_len_lt_v_len(): return pf('!t_diff_str_u_len_lt_v_len')
  if not t_diff_str_u_len_gt_v_len(): return pf('!t_diff_str_u_len_gt_v_len')
  return True
