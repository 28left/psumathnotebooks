import cyllene
from cyllene import *
import sympy as sp
from sympy import plot


f = expression('x+2')

g = expression('x^2')
G_g = plot(g, (x, -3, 3), show=False)
line = plot(4, (x, -5, 5), line_color='red',show=False)
G_g.extend(line)

G_h = plot(g, (x, 0, 3), show=False)
line = plot(4, (x, 0, 4), line_color='red',show=False)
G_h.extend(line)

f_exp = function('2^x')
P_1 = pp.ExpressionProblem('1',
                        'Compute the following values of $f(x) = 2^x$:', 
                        5,
                        ['$f(-2)$', '$f(-1)$', '$f(0)$', '$f(1)$', '$f(2)$'],
                        'numerical',
                        [f_exp(-2), f_exp(-1), f_exp(0), f_exp(1), f_exp(2)]
                       )
ProbStack.add(P_1)

P_2 = pp.TrueFalse('2', "The function $f(x) = 2^x$ is one-to-one", True)
ProbStack.add(P_2)

f_log = function('log(x,2)')
P_3 = pp.ExpressionProblem('3',
                        'Compute the following values of $f(x) = \\log_2(x)$:', 
                        3,
                        ['$f(2)$', '$f(1)$', '$f(1/2)$'],
                        'numerical',
                        [f_log(2), f_log(1), sp.N(f_log(1/2))]
                       )
ProbStack.add(P_3)