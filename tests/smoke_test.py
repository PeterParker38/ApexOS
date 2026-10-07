import importlib
for pkg in ['numpy', 'pandas', 'sklearn', 'fastf1', 'torch']:
    try:
        m = importlib.import_module(pkg)
        print('OK  ', pkg, getattr(m, '__version__', ''))
    except Exception as e:
        print('FAIL', pkg, e)
