from time import time

from hak.many.dicts.get_all_keys import f as get_field_names
from hak.many.dicts.get_datatypes import f as get_field_datatypes
from hak.many.dicts.get_keys_with_none_or_zero_vals import f as get_empty_fields
from hak.one.dict.cell.make import f as make_cell
from hak.one.dict.custom_order.apply import f as apply_custom_order
from hak.one.dict.header.to_str import f as make_head
from hak.one.dict.hidden_fields.hide import f as hide_fields
from hak.one.dict.table.get_field_widths import f as get_field_widths
from hak.one.string.colour.bright.green import f as g
from hak.one.string.colour.bright.red import f as r
from hak.one.string.colour.tgfr import f as tgfr
from hak.one.string.print_and_return_false import f as pf
from hak.one.string.table.bar.make import f as make_bar
from hak.one.dict.quantity.make import f as make_quantity
from hak.one.dict.quantity.is_a import f as is_quantity
from hak.one.dict.get_or_default import f as get_or_default

def _make_unit_row(x):
  names = x['names']
  _widths = x['widths']
  sp = ' '
  # return '\n'.join([
  #   "| "+' | '.join([
  #     f"{_f.split('_')[i]:>{_widths[_f]}}" if len(_f.split('_')) > i else
  #     f"{sp:>{_widths[_f]}}"
  #     for _f in names
  #   ])+" |"
  #   for i in range(max([len(_f.split('_')) for _f in names]))
  # ])

# src.list.dicts.to_table
def f(x):
  records = x['records']
  order = x['field_order'] if 'field_order' in x else []
  hidden = x['hidden_fields'] if 'hidden_fields' in x else []
  empty = get_empty_fields(x['records']+[{k: None for k in order}])
  for k in empty: hidden.append(k)
  names = hide_fields({
    'field_names': apply_custom_order({
      'field_names': get_field_names(records),
      'field_order': order
    }),
    'hidden_fields': hidden
  })
  field_widths = get_field_widths({'records': records, 'field_names': names})
  bar = make_bar({'field_widths': field_widths, 'field_names': names})

  field_units = {
    k: (
      get_or_default(records[-1], k, {})['unit']
      if is_quantity(get_or_default(records[-1], k, {}))
      else
      ''
    )
    for k in names
  }

  obj = {
    'field_widths': field_widths,
    'field_names': names,
    'field_units': field_units
  }

  if all([field_units[k] == '' for k in field_units]):
    del obj['field_units']

  head = make_head(obj)

  field_datatypes_by_key = get_field_datatypes(records)
  rows = [
    "| "+' | '.join([(
      make_cell(
        {
          'value': r[k] if k in r else None,
          'field_name': k,
          'width': field_widths[k],
          'type': (
            field_datatypes_by_key[k] if k in field_datatypes_by_key else None
          )
        }
      )
    ) for k in names])+" |"
    for r in records
  ]
  return '\n'.join([
    bar,
    head,
    bar,
    *rows,
    bar
  ])

def t_0():
  x = {'records': [{'a': 0, 'b': 1}, {'a': 2, 'b': 3}]}
  y = '\n'.join([
    "|---|---|",
    "| a | b |",
    "|---|---|",
    "|   | 1 |",
    "| 2 | 3 |",
    "|---|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_1():
  x = {'records': [{'a': 0, 'b': 1, 'c': 2}, {'a': 2, 'b': 3}]}
  y = '\n'.join([
    "|---|---|---|",
    "| a | b | c |",
    "|---|---|---|",
    "|   | 1 | 2 |",
    "| 2 | 3 |   |",
    "|---|---|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_2():
  x = {'records': [{'a': 0, 'b': 1}, {'a': 2, 'b': 3, 'c': 4}]}
  y = '\n'.join([
    "|---|---|---|",
    "| a | b | c |",
    "|---|---|---|",
    "|   | 1 |   |",
    "| 2 | 3 | 4 |",
    "|---|---|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_3():
  x = {'records': [{'aa': 0, 'b': 1}, {'aa': 2, 'b': 3}]}
  y = '\n'.join([
    "|----|---|",
    "| aa | b |",
    "|----|---|",
    "|    | 1 |",
    "|  2 | 3 |",
    "|----|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_4():
  x = {'records': [{'a': 10, 'b': 11}, {'a': 12, 'b': 13}]}
  y = '\n'.join([
    "|----|----|",
    "|  a |  b |",
    "|----|----|",
    "| 10 | 11 |",
    "| 12 | 13 |",
    "|----|----|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_5():
  x = {'records': [{'a': 10, 'b': 1}, {'a': 2, 'b': 13}]}
  y = '\n'.join([
    "|----|----|",
    "|  a |  b |",
    "|----|----|",
    "| 10 |  1 |",
    "|  2 | 13 |",
    "|----|----|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_6():
  x = {
    'records': [
      {'a': 10, 'b': 1},
      {'a': 2, 'b': 13},
      {'a': 3, 'b': 12, 'c': 15}
    ],
    'field_order': ['c', 'b']
  }
  y = '\n'.join([
    "|----|----|----|",
    "|  c |  b |  a |",
    "|----|----|----|",
    "|    |  1 | 10 |",
    "|    | 13 |  2 |",
    "| 15 | 12 |  3 |",
    "|----|----|----|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_7():
  x = {}
  x['records'] = [{'a': 10 }, {'a': 2}, {'a': 3, 'c': 15}]
  x['field_order'] = ['c', 'b']
  y = '\n'.join([
    "|----|----|",
    "|  c |  a |",
    "|----|----|",
    "|    | 10 |",
    "|    |  2 |",
    "| 15 |  3 |",
    "|----|----|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_8():
  x = {}
  x['records'] = [
    {'a': 10, 'b': 1},
    {'a': 2, 'b': 13},
    {'a': 3, 'b': 12, 'c': 15}
  ]
  x['field_order'] = ['c', 'b']
  x['hidden_fields'] = ['c']
  y = '\n'.join([
    "|----|----|",
    "|  b |  a |",
    "|----|----|",
    "|  1 | 10 |",
    "| 13 |  2 |",
    "| 12 |  3 |",
    "|----|----|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_9():
  x = {}
  x['records'] = [
    {'a': True, 'b': 1},
    {'a': False, 'b': 13},
    {'a': False, 'b': 12, 'c': 15}
  ]
  x['field_order'] = ['c', 'b']
  x['hidden_fields'] = ['c']
  y = '\n'.join([
    "|----|---|",
    "|  b | a |",
    "|----|---|",
    f"|  1 | {g('Y')} |",
    f"| 13 | {r('N')} |",
    f"| 12 | {r('N')} |",
    "|----|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_a():
  x = {}
  x['records'] = [
    {'is_revenue': True, 'b': 1},
    {'is_revenue': False, 'b': 13},
    {'is_revenue': False, 'b': 12, 'c': 15}
  ]
  x['field_order'] = ['c', 'b']
  x['hidden_fields'] = ['c']
  y = '\n'.join([
    "|----|---------|",
    "|  b |      is |",
    "|    | revenue |",
    "|----|---------|",
    f"|  1 |       {g('Y')} |",
    f"| 13 |       {r('N')} |",
    f"| 12 |       {r('N')} |",
    "|----|---------|"
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_b():
  x = {}
  x['records'] = [
    {'balance_a': 1.0, 'b': 13},
    {'balance_a': 1.1, 'b': 12, 'c': 15}
  ]
  x['field_order'] = ['c', 'b']
  x['hidden_fields'] = ['c']
  y = '\n'.join([
    "|----|---------|",
    "|  b | balance |",
    "|    |       a |",
    "|----|---------|",
    "| 13 |    1.00 |",
    "| 12 |    1.10 |",
    "|----|---------|"
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_c():
  x = {
    'records': [
      {'description': 'Opening transaction'},
      {
        'description': 'Deposit 1000 AUD',
        'flow_AUD': 1000.0,
        'flag_asset_aud_cash': 1,
        'flag_equity_retained_earnings': 1
      },
      {
        'description': 'Exchanged 1000 AUD for 100 USD',
        'flow_AUD': -1000.0,
        'flow_USD': 100.0,
        'flag_asset_aud_cash': -1,
        'flag_asset_usd_cash_as_aud': 1
      }
    ],
    'field_order': [
      'description', 'rate_USD_per_AUD', 'flow_AUD', 'flow_USD', 'total_AUD',
      'total_USD', 'equiv_AUD', 'flag_asset_aud_cash',
      'flag_asset_usd_cash_as_aud', 'flag_equity_retained_earnings',
      'balance_asset_aud_cash', 'balance_asset_usd_cash_as_aud',
      'balance_equity_retained_earnings'
    ],
    'hidden_fields': [
      'flag_liability', 'balance_liability', 'flow_USD', 'total_USD',
      'flag_asset_usd_cash_as_aud', 'balance_asset_usd_cash_as_aud',
      'rate_USD_per_AUD'
    ]
  }
  y = '\n'.join([
    "|--------------------------------|----------|-------|----------|",
    "|                    description |     flow |  flag |     flag |",
    "|                                |      AUD | asset |   equity |",
    "|                                |          |   aud | retained |",
    "|                                |          |  cash | earnings |",
    "|--------------------------------|----------|-------|----------|",
    "|            Opening transaction |          |       |          |",
    "|               Deposit 1000 AUD |  1000.00 |     1 |        1 |",
    "| Exchanged 1000 AUD for 100 USD | -1000.00 |    -1 |          |",
    "|--------------------------------|----------|-------|----------|"
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_quantity():
  x = {
    'records': [
      {'a': make_quantity(0, 'm'), 'b': make_quantity(1, '$')},
      {'a': make_quantity(2, 'm'), 'b': make_quantity(3, '$')}
    ]
  }
  y = '\n'.join([
    "|---|---|",
    "| a | b |",
    "|---|---|",
    "| m | $ |",
    "|---|---|",
    "|   | 1 |",
    "| 2 | 3 |",
    "|---|---|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  if not t_3(): return pf('t_3 failed')
  if not t_4(): return pf('t_4 failed')
  if not t_5(): return pf('t_5 failed')
  if not t_6(): return pf('t_6 failed')
  if not t_7(): return pf('t_7 failed')
  if not t_8(): return pf('t_8 failed')
  if not t_9(): return pf('t_9 failed')
  if not t_a(): return pf('t_a failed')
  if not t_b(): return pf('t_b failed')
  if not t_c(): return pf('t_c failed')
  if not t_quantity(): return pf('t_quantity failed')
  return True

if __name__ == '__main__':
  print(tgfr(t()))
  print(time())
