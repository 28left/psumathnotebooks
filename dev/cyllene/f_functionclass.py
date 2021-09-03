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

class Function:

    """
    Basic class to represent a single-variable, real-valued
    function. Every function has four basic attributes:
    - sympy expression
    - tree form
    - table
    - graph
    """

    def __init__(self, expr):
        
        [new_expr, self.issues] = fd.define_expression(expr)
        
        if new_expr != None:
            # input ok
            self.is_defined = True
        else:
            # Initialize zero function and set flag
            self.is_defined = False
            expr = sp.sympify(0)

        # Initialize all basic function attributes
        self.sym_form = new_expr
        self.str_form = str(new_expr).replace('**', '^')
        self.list_form = lf.string_to_list(self.str_form)
        self.tex_form = sp.latex(self.sym_form)
        self.table_form = {}
        # self.graph_form = plt.figure()

        # initialize further attributes of a function
        variables = fa.get_variables(self.sym_form)
        string_variables = [str(var) for var in variables]
        string_variables.sort()
        self.variables = [MYLOCALS_LAMBDA[var_string] for var_string in string_variables] # do this to sort variables alphabetically

        # self.variables = fa.get_variables(self.sym_form)
        self.lambda_form = sp.lambdify(self.variables, self.str_form, MYLOCALS_LAMBDA)

        self.breakpoints = {}
        self.functions = {}
        self.right_endpoints = {}

        # get the domain
        """
        get_domain method from sympy does not seem stable currently
        (as of Nov 15, 2020) -- disabled for now
        """
        # self.domain = fa.get_domain(self.sym_form)

    # def eval_at(self, vals):
        #################
        # THIS ONE IS DEPRECATED, BECAUSE IT WAS WRITTEN WITHOUT CUSTOM EVALUATION FUNCTIONS IN MIND
        # 
        # May evaluate the Function at any of its variables. May pass a dictionary
        # of variable assignments (e.g. {x: 2, y: 3}), an array of values following
        # the same order as the variables in self.variables, or a singular value with
        # which to substitute into the first variable in self.variables
        # 
        # Desired improvements: more error checking/resiliency.
        #################
        # if self.variables:
        #     if isinstance(vals, list):
        #         # return self.sym_form.subs(self.variables, vals)
        #         # need list of tuples like [(x, 2), (y, 4), (z, 1)]
        #         num = min(len(vals), len(self.variables))
        #         substitution = []
        #         for i in range(num):
        #             substitution.append((self.variables[i], vals[i]))
        #         return self.sym_form.subs(substitution)
        #     elif isinstance(vals, dict):
        #         return self.sym_form.subs(vals)
        #     else: 
        #         return self.sym_form.subs(self.variables[0], vals)
        # else: 
        #     return self.sym_form.subs(x, vals)

    def compute_at_non_piecewise(self, *argv):
        if self.variables:
            if isinstance(argv[0], dict):
                return self.sym_form.subs(argv[0])
            elif(len(argv) > 0):
                # need list of tuples like [(x, 2), (y, 4), (z, 1)]
                num = min(len(argv), len(self.variables))
                substitution = []
                for i in range(num):
                    substitution.append((self.variables[i], argv[i]))
                return self.sym_form.subs(substitution)
        elif(len(argv) > 0):
            return self.sym_form.subs(x, argv[0])
        else:
            return self.sym_form

    # my attempt to avoid the problems of the eval_at function below.
    def compute_at(self, *argv):
        # Works either for piecewise of 1 variable, or non-piecewise for any number of vars

        # non-piecewise functions, any number of vars
        if(len(self.breakpoints) == 0):
            return self.compute_at_non_piecewise(*argv)

        # otherwise, want to only consider 1D piecewise functions
        if(self.variables is None):
            return self.sym_form
        elif(len(self.variables) != 1):
            return self.sym_form
        
        # abbreviate number of breakpoints in this piecewise function to be n
        n = len(self.breakpoints)
        
        # decide the input, check some cases that would prevent us from proceeding
        input = 0
        if(isinstance(argv[0], dict)):
            if(not self.variables[0] in argv[0]):
                return self.sym_form
            else: input = float(argv[0][self.variables[0]])
        else: 
            if(len(argv) > 0):
                input = float(argv[0])
            else:
                return self.sym_form
        
        # if not piecewise
        if(n == 0):
            return self.compute_at_non_piecewise(input)

        # figure out which Function from this piecewise function to pass
        breakpoint_index = 0
        for i in range(n):
            if(self.right_endpoints[i] and input == self.breakpoints[i] or input < self.breakpoints[i]):
                break
            breakpoint_index += 1
        passedFunction = self.Functions[breakpoint_index]

        return passedFunction.compute_at_non_piecewise(input)
        
            
    # The reason I don't like this is you have to return a number back, not a sympy expression.
    # Therefore, constants like "e" and "pi" cannot be left unevaluated 
    def eval_at(self, *argv):
        ################# 
        # I'm going to try to make something smarter here. We need all variables to be assigned, but we'll 
        # ask for a dictionary where each variable in self.variables is assigned a value.
        # The downside to doing it straight-up is that the self.variables may be in a weird order.
        # Instead, a dictionary lets us have a nice order. This method will take care of ordering correctly. 
        # 
        # Desired improvements: more error checking/resiliency.
        #################
        if(len(argv) == 0 and len(self.variables) == 0):
            return self.sym_form
        if(isinstance(argv[0], dict)):
            if(self.variables and e in self.variables):
                argv[0][e] = math.e
            try:
                # treat like a dictionary
                values_in_order = []
                for var in self.variables:
                    values_in_order.append(float(argv[0][var]))
                return self.lambda_form(*values_in_order)
            except KeyError:
                return "Haven't defined the correct variables. Variables should appear as " + str(self.variables)
        else:
            if(len(argv) < len(self.variables)):
                return "Too few arguments passed. Variables should appear as " + str(self.variables)
            elif(len(argv) > len(self.variables)):
                return "Too many arguments passed. Variables should appear as " + str(self.variables)
            else: return self.lambda_form(*argv) # the scenario where user knows the order of the variables

# # This is new, do we need to merge this with the previous eval function?
#     def eval_np(self,npx):
#         return sp.lambdify(self.variables[0], self.sym_form)(npx)
    
    @staticmethod
    def piecewise(breakpoints, Functions, right_endpoints):
        #########################
        # Returns a (1D) piecewise function of the class type Function. User provides where breakpoints
        # (dividing one piece from another) are as a list of floats, a list of Function objects along 
        # describing each piece, and a list of Boolean values answering "Is the right endpoint included
        # along this piece?" The piecewise function returned will be expressed via two standard functions
        # denoted by H(x) and T(x). H(x) = 0 for x < 0, otherwise 1. T(x) = 0 if x < 0 or x >= 1, otherwise 1.
        # Together, H and T can describe a piecewise function in a "single line."
        #########################
        n = len(breakpoints)
        breakpoints = [float(breakpoint) for breakpoint in breakpoints] # ensure all breakpoints are floats
        if(len(Functions) != n + 1 or len(right_endpoints) != n):
            return None
        elif(n == 0):
            return Functions[0]
        else: 
            piecewise_string = "({0}) *".format(str(Functions[0].sym_form)) + ("H({0} - x)".format(str(breakpoints[0])) if right_endpoints[0] else "(1 - H(x - {0}))".format(str(breakpoints[0])))
            for i in range(1, n):
                piecewise_string += " + ({0}) * ".format(str(Functions[i].sym_form))
                if(right_endpoints[i-1]):
                    piecewise_string += "T(({1} - x)/({1} - {0}))".format(str(breakpoints[i-1]), str(breakpoints[i])) if right_endpoints[i] else "T((x - {0})/({1} - {0})) * T(({1} - x)/({1} - {0}))".format(str(breakpoints[i-1]), str(breakpoints[i])) 
                else: # right_endpoints[i-1] == False
                    piecewise_string += "(1 - H(-(T((x - {0})/({1} - {0})) + T(({1} - x)/({1} - {0})))))".format(str(breakpoints[i-1]), str(breakpoints[i])) if right_endpoints[i] else "T((x - {0})/({1} - {0}))".format(str(breakpoints[i-1]), str(breakpoints[i]))

            piecewise_string += " + ({0}) *".format(str(Functions[n].sym_form)) + ("(1 - H({0} - x))".format(str(breakpoints[n-1])) if right_endpoints[n-1] else "H(x - {0})".format(str(breakpoints[n-1])))
            piecewise_sympify = sp.sympify(piecewise_string, locals=MYLOCALS_SYMPIFY, evaluate=False)
            piecewise_function = Function(piecewise_sympify)
            piecewise_function.breakpoints = breakpoints
            piecewise_function.Functions = Functions
            piecewise_function.right_endpoints = right_endpoints
            piecewise_function.breakpoints.sort() # make sure in increasing order
            return piecewise_function
        
    def plot(self, min, max):
        # Plotter for a Function of one variable.
        if(len(self.variables) > 1):
            return None
        n = len(self.breakpoints)
        if(n == 0):
            x_vals = linspace(min, max)
            y_vals = list(map(self.lambda_form, x_vals))
            mpl.plot(x_vals, y_vals)
        else:
            x_vals = linspace(min, self.breakpoints[0], 500)
            y_vals = list(map(self.lambda_form, x_vals))
            mpl.plot(x_vals, y_vals, '.')
            for i in range(0, n - 1):
                x_vals = linspace(self.breakpoints[i], self.breakpoints[i+1], 500)
                y_vals = list(map(self.lambda_form, x_vals))
                mpl.plot(x_vals, y_vals, '.')
            x_vals = linspace(self.breakpoints[n - 1], max, 500)
            y_vals = list(map(self.lambda_form, x_vals))
            mpl.plot(x_vals, y_vals, '.')
        mpl.show()
    
 ####################################BehaviourMethod##################################


#Helper functions for the behavior method.   
    def Increasing(self):
        if self.variables == []:
            return sp.EmptySet
        else:
            x = self.variables[0]
            p = sp.diff(self.sym_form,x)
            return sp.solveset(p>0, x, sp.Reals)

    def Decreasing(self):
        if self.variables==[]:
            return sp.EmptySet
        else:
            x = self.variables[0]
            p = sp.diff(self.sym_form,x)
            return sp.solveset(p<0, x, sp.Reals)

   
    def Concave_Up(self):
        if self.variables==[]:
            return sp.EmptySet
        else:
            x = self.variables[0]
            p = sp.diff(self.sym_form,x)
            q = sp.diff(p,x)
            CU = sp.solveset(q>0, x, sp.Reals)
            return CU

    def Concave_Down(self):
        if self.variables==[]:
            return sp.EmptySet
        else:
            x = self.variables[0]
            p = sp.diff(self.sym_form,x)
            q = sp.diff(p,x)
            CD = sp.solveset(q<0, x, sp.Reals)
            return CD

    def inflection_points(self):
        if self.variables==[]:
            return sp.EmptySet
        else:
            x = self.variables[0] 
            p = sp.diff(self.sym_form,x)
            q = sp.diff(p,x)
            if q==0:
                return sp.EmptySet
            else:
                A = sp.solveset(q,x, sp.Reals)
                return A


    def zeros(self):
        if self.variables:
            x =self.variables[0]
            S = sp.solveset(self.sym_form, x, sp.Reals)
            return S 
        else:
            return sp.EmptySet

    def extrema(self):
        if self.variables==[]:
            return sp.EmptySet
        else:       
            x = self.variables[0]
            df = self.derv()
            S = df.zeros()
            return S 

 


    def singularities(self):
        return sp.Complement(sp.Reals, self.domain)


    def Inflection_Interval(self):
        I=self.inflection_points()
        if len(I)>1:
            a=min(I)
            b=max(I)
            return sp.Interval(a,b)
        else:

            return sp.Interval(-10,10)
        
        
    def Largest_Interval(self):
        zeros = self.zeros()
        extrema = self.extrema()
        inflection_points = self.inflection_points()
        zero = 0


        left_zero, right_zero = self.boundries(zeros)
        left_extrem, right_extrem  = self.boundries(extrema)
        left_infliction,right_infliction = self.boundries(inflection_points)

        left_boundry = min(left_zero,left_extrem,left_infliction,zero) -1 
        right_boundry= min(right_zero,right_extrem,right_infliction,zero) + 1

    
        I = sp.Interval(left_boundry, right_boundry)
        return I

    
    def range(self,I):
        left_point, right_point = float(I.args[0]), float(I.args[1])

        extrme_floats = [left_point,right_point]
        for p in self.extrema():
            extrme_floats.append(float(p))

        max = self.eval_np(extrme_floats[0])
        min = self.eval_np(extrme_floats[0])

        for p in extrme_floats:
            fp = self.eval_np(p)

            if(fp > max):
                max = fp
            elif(fp < min):
                min = fp

        I = sp.Interval(min,max)
        return I


    def intersect_intervals(self,Intervals):
        I = Intervals[0]
        for J in Intervals:
            I = I.intersect(J)
        return I

    def union_intervals(self,Intervals):
        I = Intervals[0]
        for J in Intervals:
            I = I.union(J)
        return J

    def boundries(self,S):
        if(S == sp.EmptySet):
            return 0, 0
        else:
            return float(S.args[0]), float(S.args[-1])



    def behaviour(self, *pars):
        #The Behavior Dictionary
        behaviour_dict ={"increasing":self.Increasing() ,
        "decreasing":self.Decreasing() , 
        "concaveup":self.Concave_Up() , 
        "concavedown":self.Concave_Down(),
        "largestinterval":self.Largest_Interval()} 

        #Build a list of Intervals from the parameters
        Intervals = [] 
        for par in pars:
            try: 
                Intervals.append(behaviour_dict[par.lower().replace(" ", "")])
            except KeyError:
                print("Check the parameter {}".format(par))
                return

        #Intersect the Intervals 
        return self.intersect_intervals(Intervals) 


# ###################################END of the Behaviour ######################################## 

   #Derivative: This function returns the derevative, of function class
    def derv(self):
        return Function(sp.diff(self.sym_form))

    def average(self,x1,x2):
        return (self.eval_at(x2) - self.eval_at(x1))/(x2-x1)

    #the following functions returns a linear function, corresponding to the secant or tangent
    def secant_line(self,x1,x2):
        x = self.variables[0]
        m = self.average(x1,x2)
        fx1 = self.eval_at(x1)

        return Function("{}(x-{}) +{} ".format(m,x1,fx1))

    def tangent_line(self,x1):
        x = self.variables[0]
        m = self.derv().eval_at(x1)
        fx1 = self.eval_at(x1)

        return Function("{}(x-{}) +{} ".format(m,x1,fx1))

    #Transformation of Functions : Need to decide, return a new function or modify the current one? 

    def shift_x(self,a):
        x = self.variables[0]
        expr = self.sym_form.subs(x, x-a)
        return Function(expr)

    def shift_y(self, a):
        expr = self.sym_form
        return Function(expr + a)


    def scale_x(self,a):
        x = self.variables[0]
        expr = self.sym_form.subs(x, x/a)
        return Function(expr)


    def scale_y(self,a):
        expr = a * self.sym_form
        return Function(expr)
    
    def __eq__(self, other):
        pass
