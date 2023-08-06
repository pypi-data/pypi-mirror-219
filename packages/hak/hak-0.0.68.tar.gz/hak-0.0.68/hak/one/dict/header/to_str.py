from hak.one.string.print_and_return_false import f as pf
from hak.one.string.table.bar.make import f as make_bar

# src.table.header.make
def f(x):
  field_units = None
  if 'field_units' in x:
    field_units = x['field_units']

  field_names = x['field_names']
  _widths = x['field_widths']

  sp = ' '
  
  result = '\n'.join([
    "| "+' | '.join([
      f"{_f.split('_')[i]:>{_widths[_f]}}" if len(_f.split('_')) > i else
      f"{sp:>{_widths[_f]}}"
      for _f in field_names
    ])+" |"
    for i in range(max([len(_f.split('_')) for _f in field_names]))
  ])

  unit_section = ''

  if field_units:
    bar = make_bar({'field_widths': _widths, 'field_names': field_names})
    unit_section += '\n'+bar+'\n'
    unit_section += '\n'.join([
      "| "+
      ' | '.join([f'{field_units[n]:>{_widths[n]}}' for n in field_names]) +
      " |"
    ])
  
  return result + unit_section

def t_0():
  x = {'field_names': list('abcde')}
  x['field_widths'] = {k: 2 for k in x['field_names']}
  y = '|  a |  b |  c |  d |  e |'
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])

def t_1():
  x = {
    'field_widths': {
      'a': 2,
      'is_revenue': len('revenue'),
      'balance_equity_retained_earnings': 8,
    },
    'field_names': [
      'a',
      'is_revenue',
      'balance_equity_retained_earnings',
    ],
  }

  y = '\n'.join([
    '|  a |      is |  balance |',
    '|    | revenue |   equity |',
    '|    |         | retained |',
    '|    |         | earnings |',
  ])
  z = f(x)
  return y == z or pf([f"x: {x}", f'y:\n{y}', f'z:\n{z}'])

def t_2():
  x = {
    'field_widths': {
      'a': len('lightyear'),
      'is_revenue': len('revenue'),
      'balance_equity_retained_earnings': 8,
    },
    'field_names': [
      'a',
      'is_revenue',
      'balance_equity_retained_earnings',
    ],
    'field_units': {
      'a': 'lightyear',
      'is_revenue': 'boolean',
      'balance_equity_retained_earnings': 'AUD'
    }
  }

  y = '\n'.join([
    '|         a |      is |  balance |',
    '|           | revenue |   equity |',
    '|           |         | retained |',
    '|           |         | earnings |',
    '|-----------|---------|----------|',
    '| lightyear | boolean |      AUD |',
  ])
  z = f(x)
  return y == z or pf([f"x: {x}", f'y:\n{y}', f'z:\n{z}'])

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  return True
