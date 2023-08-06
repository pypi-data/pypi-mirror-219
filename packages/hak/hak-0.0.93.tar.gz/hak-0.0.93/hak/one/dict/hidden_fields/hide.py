from hak.pxyz import f as pxyz

f = lambda x: [k for k in x['field_names'] if k not in set(x['hidden_fields'])]

def t():
  x = {'hidden_fields': list('ace'), 'field_names': list('abcde')}
  y = list('bd')
  z = f(x)
  return pxyz(x, y, z)
