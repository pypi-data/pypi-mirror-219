f = lambda module_names: ['src.haks.'+m for m in module_names]

t = lambda: ['src.haks.abc', 'src.haks.xyz'] == f(['abc', 'xyz'])
