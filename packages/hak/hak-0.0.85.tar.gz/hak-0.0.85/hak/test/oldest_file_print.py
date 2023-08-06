from hak.many.strings.filepaths.py.testables.get import f as list_testables
from os.path import getmtime
from hak.one.file.pickle.load_if_exists import f as load_pickle
from hak.one.file.remove import f as remove
from hak.one.file.pickle.save import f as save
from hak.many.strings.filepaths.py.testables.get import f as make_Pi_t
from hak.one.dict.durations.to_tuple_list_sorted_by_duration import f as srt

def f(_Pi=None):
  _Pi = list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in _Pi}
  save(last_mods, './last_modified.pickle')
  _Pi_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Pi_t(_Pi, True, prev, last_mods) + list(_Pi_fail))
  _Pi_t = [a for a in _A if a in _B]
  print(f'Oldest file: {_Pi_t[-1]}')

def t(): return True # TODO
