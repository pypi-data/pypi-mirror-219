from hak.one.string.print_and_return_false import f as pf

def f(durations, name, δt_ms):
  durations[name] = (
    (durations[name] + δt_ms)/2
    if name
    in durations
    else δt_ms
  )
  return durations

def t_value_update():
  x = {
    'durations': {'a': 0, 'b': 1},
    'name': 'b',
    'δt_ms': 2
  }
  y = {'a': 0, 'b': 1.5}
  z = f(**x)
  return y == z or pf([
    'Value update test failed',
    f'x: {x}',
    f'y: {y}',
    f'z: {z}',
  ])

def t_value_create():
  x = {
    'durations': {'a': 0, 'b': 1},
    'name': 'c',
    'δt_ms': 2
  }
  y = {'a': 0, 'b': 1, 'c': 2}
  z = f(**x)
  return y == z or pf([
    'Value create test failed',
    f'x: {x}',
    f'y: {y}',
    f'z: {z}',
  ])

t = lambda: all([t_value_update(), t_value_create()])
