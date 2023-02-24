import sympy as sp
import random
import matplotlib.pyplot as mpl
from numpy import linspace
from sympy import functions
import math

import cyllene
from cyllene import *

# constants
from cyllene.constants import *

# aux parsing libraries
import cyllene.a_mathstring as ms
import cyllene.a_listform as lf

# import other modules
import cyllene.f_aux as fa
import cyllene.f_define as fd


"""
Valid arguments
- a string
- a constant
- a sympy expression
"""

class LazyFunction:
    
    """
    Class to represent a generator of functions (single-variable, real-valued
    functions). LazyFunctions are stored as trees.
    """ 

    def __init__(self, expr):
        self.string = expr
        # [new_expr, self.issues] = fd.define_expression(expr)
        # if new_expr != None:
        #     # input ok
        #     self.is_defined = True
        # else:
        #     # Initialize zero function and set flag
        #     self.is_defined = False
        #     expr = sp.sympify(0)
        new_expr = sp.sympify(expr, locals=MYLOCALS_SYMPIFY, evaluate=False)

        # Initialize all basic function attributes
        self.sym_form = new_expr
        self.str_form = str(new_expr).replace('**', '^')
        self.list_form = lf.string_to_list(self.str_form)
        self.tex_form = sp.latex(self.sym_form)
        self.table_form = {}

        # # initialize further attributes of a function
        self.variables = {'x'}

    @staticmethod
    def explore_and_replace(expr_list):
        new_list = []
        for i in range(len(expr_list)):
            if(isinstance(expr_list[i], list)):
                new_list.append(LazyFunction.explore_and_replace(expr_list[i]))
            else:
                print(expr_list[i])
                new_list.append(expr_list[i]) # change later
                

    def produce(self):
        from cyllene.f_functionclass import Function
        # idea is to instantiate a function object as defined in f_functionclass
        # return Function(explore_and_replace(self.list_form))
        new_list_form = LazyFunction.explore_and_replace(self.list_form)
        return None