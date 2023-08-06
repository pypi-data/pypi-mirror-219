from string import printable
from hak.one.string.print_and_return_false import f as pf

# replace_unprintable

f = lambda ζ: ''.join([z if z in printable else '*' for z in ζ])

def t():
  x = [''.join([chr(x) for x in range(128)])][0]
  y = ''.join([
    '*********\t\n\x0b\x0c\r****************** !"#$%&\'()*+,-./0123456789:;',
    '<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~*'
  ])
  z = f(x)
  return y == z or pf(['y != z', f'[y]: {[y]}', f'[z]: {[z]}'])
