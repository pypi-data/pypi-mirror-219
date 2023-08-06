from datetime import date

f = lambda x: x.weekday() >= 5

t = lambda: all([
  not any([
    *[f(date(*_)) for _ in [
      (2022, 12, 26), # 2022-12-26 0  Monday
      (2022, 12, 27), # 2022-12-27 1  Tuesday
      (2022, 12, 28), # 2022-12-28 2  Wednesday
      (2022, 12, 29), # 2022-12-29 3  Thursday
      (2022, 12, 30), # 2022-12-30 4  Friday
    ]]
  ]),
  f(date(2022, 12, 31)),   # 2022-12-31 5  Saturday
  f(date(2023,  1,  1)),   # 2023-01-01 6  Sunday
])
