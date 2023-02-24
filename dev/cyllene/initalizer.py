# import sympy as sp

e, const, step, exp, trig, poly, linear, quadratic, cubic, sqrt, cbrt, H, S = sp.symbols(
    'e const step exp trig poly linear quadratic cubic sqrt cbrt H S', cls=sp.Function
)
a, b, c, d, p, q, r, s, t, w, x, y, z = sp.symbols(
    'a b c d p q r s t w x y z', real=True)

MYLOCALS = {'a': a, 'b': b, 'c': c, 'd': d, 'p': p, 'q': q, 'r': r,
    's': s, 't': t, 'w': w, 'x': x, 'y': y, 'z': z, 'e': e,
    'const': const, 'step': step, 'exp': exp, 'trig': trig,
    'poly': poly, 'linear': linear, 'quadratic': quadratic,
    'cubic': cubic, 'sqrt': sqrt, 'cbrt': cbrt, 'H': H, 'S': S
    }