__version__ = "0.2"

import cyllene.problems as pp
import cyllene.problem_display as pd

# from dev.cyllene.p_problem import ProbStack

# import dev.cyllene.m_input_tweaks
# import dev.cyllene.m_magics

from cyllene.m_user_cmd import function, expression, graph

import sympy as sp
import numpy as np

# from cyllene.f_sheets import function_to_sheet
from cyllene.f_table import function_to_table, output_table
from cyllene.f_aux import sign
from cyllene.f_functionclass import Function

from cyllene.constants import *