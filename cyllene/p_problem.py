import random
from sympy import latex, simplify

# get output methods for IPython
from IPython.display import display, Markdown, Latex, Math, clear_output


import cyllene.f_define as fd
import cyllene.f_compare as fc



"""
Add answer cells for problems
"""
def add_answer_cell(problem):
    my_ipython = get_ipython()
    input_frame = "%%answer Problem " + problem.name + "\n"
    if problem.num_inputs > 1:
        for i in range(problem.num_inputs):
            input_frame += "("+str(i+1)+"): \n"
        input_frame = input_frame[:len(input_frame)-1]
    my_ipython.set_next_input(input_frame, replace=False)


            
"""
ProblemStack: class to keep a dictionary of problems used in the current notebook
"""
class ProblemStack():
    """
    attributes:
        stack: dict
    """
    def __init__(self):
        self.stack = {}

    def add(self, problem, state_problem=False, answer_cell=False):
        self.stack[problem.name] = problem

        if state_problem:
            problem.state_problem()

        if answer_cell:
            add_answer_cell(problem)



# create problem stack
ProbStack = ProblemStack()




"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""
class BaseProblem():
    """
    attributes:
        name (string): problem name
        statement (string): general statement of the problem, such as
            "Find the derivative of the following function."
        type (string): 'expression' | 'multchoice' | 'truefalse' | 'text'
        status (const string): current status of the problem
            'correct' | 'incorrect' | 'undecided'
        regen (Boolean): can problem auto-generate new instances?
    """

    def __init__(self,
                 name,
                 statement, 
                 type,
                 num_inputs=1,
                 regen=False
                ):

        self.name = name
        self.statement = statement
        self.type = type
        self.num_inputs = num_inputs
        self.regen = regen
        self.status = 'undecided'
        self.check = []

    def state_problem(self):

        # Show just title and statement
        if self.regen:
            title = '### <font color=\'SteelBlue\'>! Problem' + self.name + '</font>'
        else:
            title = '### Problem ' + self.name 
        display(Markdown(title))
        display(Markdown(self.statement))

    def add_problem_to_stack(self):
        ProbStack.add(self)


class ExpressionProblem(BaseProblem):
    """
    attributes:
        name (string): problem name
        statement (string): general statement of the problem, such as
            "Find the derivative of the following function."
        expression (Function, or array of): mathematical expression to 
            be used in problem. 
            Example: 3x^2-1
            (array of) string(s) containing the problem description
        answer_type: type of answer expected
            possible: 'expression' | 'numerical'
        correct_answer: sympy expression
        current_answer: current answer on record
        status (const string): current status of the problem
            'correct', 'incorrect', 'undecided'
    """

    def __init__(self,
                 name,
                 statement, 
                 num_inputs,
                 expression, 
                 answer_type, 
                 correct_answer,
                 eval_mode='full',
                 regen=False
                ):

        # call the parent constructor 
        super().__init__(name, statement, 'expression', num_inputs, regen)

        if type(expression) != list:
            expression = [expression]
        self.expression = expression

        self.answer_type = answer_type

        if type(correct_answer) != list:
            correct_answer = [correct_answer]
        self.correct_answer = correct_answer
        
        self.eval_mode = eval_mode

        self.current_answer = ['']

    
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

        self.show_result()


    def state_problem(self):

        # show title and statement
        super().state_problem()

        # show expressions used in problem
        if len(self.expression) == 1:
            if type(self.expression[0] == str):
                display(Markdown(self.expression[0]))
            else:
                display(Math(latex(self.expression[0])))
        if len(self.expression) > 1:
            for i in range(len(self.expression)):
                if type(self.expression[i] == str):
                    display(Markdown("**("+str(i+1)+")** $\quad$"+self.expression[i]))
                else:
                    display(Math("**("+str(i+1)+")** \quad" + latex(self.expression[i])))

                

        # instructions 
        display(Markdown("*Enter the answer(s) in the cell below.*"))

    # def show_result(self):
    #     jpr.show_result(self.current_answer, self.check)

    def show_result(self):

        result_string = "You entered: <br>"
        for i, answer in enumerate(self.current_answer):
            line = ''
            if self.num_inputs > 1:
                line += '**('+  str(i+1) + ')** &nbsp;' 

            if answer[0] != None:
                line +=  '$\displaystyle '+latex(answer[0])+'$'
                if self.check[i]: 
                    line = '&#9989; &nbsp;' + line + ' &nbsp;&nbsp; (*Correct*) <br>'
                else:
                    line = '&#10060; &nbsp;' + line + ' &nbsp;&nbsp; (*Incorrect*) <br>'

            else:
                line = '&#10060;  &nbsp;' + line + 'Invalid input. Problems encountered: <br>' 
                for j in range(len(answer[1])):
                    line += '&nbsp;&nbsp;&nbsp;&nbsp; - &nbsp;' + answer[1][j]+'<br>'
            result_string += line        
        
        display(Markdown(result_string))




# # Multiple choice widget
# 
#  Basic class to implement a multiple choice test element.
# 
#  - class name: `MultipleChoice`
#  - initialization: pass two arguments
#      - `question`: type `str`, Question text
#      - `choice_text`: list of `str`, where the first entry contains the correct answer

# In[ ]:


class MultipleChoice(BaseProblem):
    
    def __init__(self, name, statement, choices):

        # call the parent constructor 
        super().__init__(name, statement, 'multchoice')

        """
        get number of choices
        """
        self.num_choices = len(choices)     
        self.choices = choices
           
        """
        Shuffle answers
        """
        self.indices = [i for i in range(self.num_choices)]
        random.shuffle(self.indices)
        self.correct = self.indices.index(0)  
            

    def state_problem(self):

        # show title and statement
        super().state_problem()

        # list the choices
        for i in range(self.num_choices):
            display(Markdown('**(' + str(i+1) + ')**  &nbsp;&nbsp;  ' + self.choices[self.indices[i]]))
        display(Markdown("*Enter the number of the correct choice in the cell below.*"))

 
    def check_answer(self, answer):

        # reset current answer check
        self.check = []

        # Pre-process answer string to remove parantheses (if present)
        answer = answer[0]
        if len(answer)>0 and answer[0]=='(':
            answer = answer[1:]
        if len(answer)>0 and answer[-1]==')':
            answer = answer[:-1]
        
        try:
            if self.correct == int(answer)-1:
                self.check.append(True)
            else:
                self.check.append(False)
        except ValueError:
            self.check.append('Error')
        
        if self.check[0] == True:
            display(Markdown('&#9989; &nbsp; **Correct!**'))
            self.status = 'correct'
        elif self.check[0] == False:
            display(Markdown('&#10060; &nbsp; **Incorrect**'))
            self.status = 'incorrect'
        else:
            display(Markdown('Please enter an integer value.'))
            self.status = 'undecided'


class TrueFalse(BaseProblem):
    
    def __init__(self, name, statement, truth_value):

        # call the parent constructor 
        super().__init__(name, statement, 'truefalse')

        # save correct answer
        self.truth_value = truth_value
           

    def state_problem(self):

        # Show title and statement
        display(Markdown('### Problem ' + self.name))
        display(Markdown("**True or False?**"))
        display(Markdown(self.statement))

       # instructions 
        display(Markdown("*Enter `T` or `F` in the cell below.*"))

 
    def check_answer(self, answer):

        # reset current answer check
        self.check = []

        try:
            # Pre-process answer string
            if answer[0][0]=='T':
                answer = 'True'
            elif answer[0][0]=='F':
                answer = 'False'
            else:
                answer = 'Error'

            if answer == str(self.truth_value):
                self.check.append(True)
            else:
                self.check.append(False)
        except ValueError or IndexError:
            self.check.append('Error')
        
        if self.check[0] == True:
            display(Markdown('&#9989; &nbsp; **Correct!**'))
            self.status = 'correct'
        elif self.check[0] == False:
            display(Markdown('&#10060; &nbsp; **Incorrect**'))
            self.status = 'incorrect'
        else:
            display(Markdown('Please enter `T` or `F`.'))
            self.status = 'undecided'

                