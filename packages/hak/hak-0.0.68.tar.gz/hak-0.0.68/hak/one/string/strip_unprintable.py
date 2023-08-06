from string import printable
# strip_unprintable

f = lambda ζ: ''.join(filter(lambda z: z in printable, ζ))

def t():
  x = [''.join([chr(x) for x in range(128)])][0]
  y = ''.join([
    '\t\n\x0b\x0c\r !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL',
    'MNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
  ])
  z = f(x)
  return y == z
