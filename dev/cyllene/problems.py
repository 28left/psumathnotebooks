import random
import string
from sympy import latex, simplify

# define and compare methods
import cyllene.f_define as fd
import cyllene.f_compare as fc


NoneType = type(None)



"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""


class BaseProblem():
    # """
    # attributes:
    #     name (string): problem name
    #     statement (string): general statement of the problem, such as
    #         "Find the derivative of the following function."
    #     answer_type (string): 
    #         'expression' | 'numerical' | 'multchoice' | 'truefalse' | 'text'
    #     regen (Boolean): can problem auto-generate new instances?
    # """

    def __init__(self,
                 name: string,
                 statement: string, 
                 answer_type: string,
                 correct_answer,
                ):

        self.name = name
        self.statement = statement
        self.answer_type = answer_type
        self.correct_answer = correct_answer


class GeneratorProblem(BaseProblem):


    def __init__(self,
                 name,
                 answer_type,
                 generator,
                 statement='',
                 correct_answer=None
                 ):

        # First call init of parent class
        super().__init__(name, statement, answer_type, correct_answer)

        # now call generate to generate real problem
        self.generator = generator
        self.generate()

    def generate(self):
        [self.statement, 
         self.correct_answer] = self.generator()


class ExpressionProblem(BaseProblem):
    """
    additional attributes:
        answer_type: type of answer expected
            possible: 'expression' | 'numerical'
        correct_answer: sympy expression
        eval_mode: how to check answer
    """


    def __init__(self,
                 name,
                 statement,
                 correct_answer,
                 num_inputs=1,
                 regen=False,
                 func=[],
                 table=[],
                 graph=[],
                 eval_mode='full',
                ):

        # call the parent constructor 
        super().__init__(
            name, 
            statement, 
            'expression',
            correct_answer, 
            num_inputs, 
            regen,
            func=[],
            table=[],
            graph=[],
        )

        if type(correct_answer) != list:
            correct_answer = [correct_answer]
        self.correct_answer = correct_answer
        
        self.eval_mode = eval_mode


    def check_answer(self, answer):
        """
        Checks whether answer is a correct expression
        and if so, compare answer to correct_answer depending on answer_type
        """
        self.check = []
        
        if not isinstance(answer, list):
            answer = [answer]

        if len(answer) < self.num_inputs:
            for i in range(self.num_inputs-len(answer)):
                answer.append('') 

        self.current_answer = [fd.define_expression(answer[i], eval_mode=False)
                            for i in range(self.num_inputs)]

        for i in range(self.num_inputs):
            """
            Check which inputs are syntax ok
            If ok, check answer
            """
            if self.current_answer[i][0] != None:
                
                if self.answer_type == 'expression':
                    self.check.append(
                        fc.compare_functions(self.current_answer[i][0], self.correct_answer[i], mode=self.eval_mode))
                else:
                    self.check.append( not 
                        bool(simplify(self.current_answer[i][0] - self.correct_answer[i])))
            else:
                self.check.append(False)



