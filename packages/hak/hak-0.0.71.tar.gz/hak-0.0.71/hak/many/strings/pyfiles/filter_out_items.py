f = lambda pyfiles, items: [p for p in pyfiles if p not in items]

t = lambda: all([
  [] == f([], []),
  ['./a.py', './b.py'] == f(
    ['./a.py', './b.py'],
    [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  ),
  ['./a.py', './b.py'] == f(
    ['./a.py', './hak/hak.py', './b.py'],
    [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  ),
  ['./a.py', './b.py'] == f(
    ['./a.py', './hak/get_file_lines.py', './b.py'],
    [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  ),
  ['./a.py', './b.py'] == f(
    ['./a.py', './hak/terminal.py', './b.py'],
    [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  ),
  ['./a.py', './b.py'] == f(
    [
      './a.py',
      './hak/refactor_recommender.py',
      './b.py'
    ],[
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  ),
  ['./a.py', './b.py'] == f(
    [
      './a.py',
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
      './b.py'
    ],[
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  )
])
