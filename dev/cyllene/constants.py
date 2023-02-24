# Place this in any function in this package referencing these constants

import sympy as sp
from sympy.utilities.lambdify import lambdify, implemented_function

# Reserve some (real-valued) symbols in Sympy
a, b, c, d, e, p, q, r, s, t, w, x, y, z = \
    sp.symbols('a b c d e p q r s t w x y z', real=True)

# Reserving some function symbols in Sympy
const, step, exp, trig, poly, linear, quadratic, cubic, sqrt, cbrt, H, T = \
    sp.symbols('const step exp trig poly linear quadratic cubic sqrt cbrt H T', cls=sp.Function)

FUNCTIONS = ['const', 'step', 'exp', 'trig', 'poly', 'linear', 'quadratic', 'cubic', 'sqrt', 'cbrt']

imp_H = implemented_function('H', lambda x: (0 if x < 0 else 1))
hH = lambdify(x, imp_H(x))
imp_T = implemented_function('T', lambda x: (0 if (x < 0 or x >= 1) else 1))
tT = lambdify(x, imp_T(x))

MYLOCALS_LAMBDA = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'p': p, 'q': q, 'r': r,
            's': s, 't': t, 'w': w, 'x': x, 'y': y, 'z': z,
            'const': const, 'step': step, 'exp': exp, 'trig': trig,
            'poly': poly, 'linear': linear, 'quadratic': quadratic,
            'cubic': cubic, 'sqrt': sqrt, 'cbrt': cbrt, 'H': hH, 'T': tT}

MYLOCALS_SYMPIFY = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'p': p, 'q': q, 'r': r,
            's': s, 't': t, 'w': w, 'x': x, 'y': y, 'z': z,
            'const': const, 'step': step, 'exp': exp, 'trig': trig,
            'poly': poly, 'linear': linear, 'quadratic': quadratic,
            'cubic': cubic, 'sqrt': sqrt, 'cbrt': cbrt, 'H': H, 'T': T}

FUNCTION_LIST = ['const', 'linear', 'quadratic', 'cubic', 'squareroot',
                'cubicroot', 'rational', 'exp', 'tri', 'log', 'comp',
                'random']

# Basic library of specific functions
RANDOM_FUNCTION_LIST = [
    ['2x+1', 'linear'], ['3x-1', 'linear'], ['(1/2)*x+3', 'linear'],
    ['x+5', 'linear'], ['x-3', 'linear'], ['-x+4', 'linear'],
    ['(1/4)*x-1', 'linear'],
    ['6t', 'linear'], ['2-6t', 'linear'], ['(1/3)*x+2', 'linear'],
    ['(1/4)*x+3', 'linear'], ['(1/5)*x+4', 'linear'], ['(1/6)*x+5', 'linear'],
    ['(1/7)*x+6', 'linear'], ['(1/8)*x+7', 'linear'], ['(1/9)*x+8', 'linear'],
    ['(1/2)*(t**2)', 'quadratic'], ['3*(t**2)+7*t+1', 'quadratic'],
    ['6*(x**2)-8*x+3', 'quadratic'], ['3*(x**2)+5', 'quadratic'],
    ['(2*x+1)^2', 'quadratic'],
    ['(x+3)^2', 'quadratic'], ['(1/6)*(x**2)+1/2', 'quadratic'],
    ['(1/3)*x^2 +2x+1', 'quadratic'], ['(1/4)*(x**2)+2*x+1', 'quadratic'],
    ['(1/5)*(x**2)+4*x', 'quadratic'], ['(1/7)*x^2+3x-2', 'quadratic'],
    ['t**3 + 5*t -12 ', 'cubic'], ['x**3-3*(x**2)+5*x', 'cubic'],
    ['4*(x**3)-2', 'cubic'],
    ['2*(x**3)-3*(x**2)+1', 'cubic'], ['t**3+t', 'cubic'],
    ['t**3-8', 'cubic'], ['-2*x^3-3', 'cubic'], ['-4*x^3+1', 'cubic'],
    ['4*(x**3)+2*x+1', 'cubic'], ['-8*x^3+3*x^2+1', 'cubic'],
    ['y**3-4*y+2', 'cubic'], ['-2*y^3+3', 'cubic'],
    ['7*(x**3)+2*(x**2)', 'cubic'],
    ['x+5', 'increasing'], ['x**3+5', 'increasing'],
    ['2*(x**3)-8', 'increasing'],
    ['2*log(x)', 'increasing'], ['2*x^5-9', 'increasing'],
    ['3*x-3', 'increasing'],
    ['12*x^3-12', 'increasing'], ['7*x-2', 'increasing'],
    ['(1/4)*x-1/2', 'increasing'],
    ['(x-3)^3', 'increasing'], ['-x-2', 'decreasing'],
    ['-x^3+5', 'decreasing'],
    ['-2*log(x)+1', 'decreasing'], ['-2*x-4', 'decreasing'],
    ['-x^7+3', 'decreasing']
]