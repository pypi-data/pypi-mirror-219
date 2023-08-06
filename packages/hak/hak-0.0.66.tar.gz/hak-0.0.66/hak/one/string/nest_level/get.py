from hak.one.string.print_and_return_false import f as pf

def f(x):
  result = []
  nest_level = 0
  for c in x:
    if c == '{':
      result.append(nest_level)
      nest_level += 1
    elif c == '}':
      nest_level -= 1
      result.append(nest_level)
    else:
      result.append(nest_level)
  return result

def t():
  x = str({'a': 0, 'b': 1, 'c': {'d': 0, 'e': 1}})
  # x: "{'a': 0, 'b': 1, 'c': {'d': 0, 'e': 1}}"
  # y:  011111111111111111111112222222222222210
  y = [
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0
  ]
  z = f(x)
  return y == z or pf(['y != z', f'x: {x}', f'y: {y}', f'z: {z}'])
