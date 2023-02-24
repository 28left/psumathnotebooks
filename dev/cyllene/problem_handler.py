from cyllene.p_Problems import BaseProblem, ExpressionProblem


class ProblemHandler:

    def __init__(self):
        self.stack = {}

    def add_problem(self, problem: BaseProblem):
    
        self.stack[problem.problem_name] = \
            [problem, 
             'undecided',   # initial status
             1,             # initial number attempts
             1              # times generated
            ]


    def display_problem(self):


        self.statement_area = widgets.Output()
        self.statement_widget = widgets.HTMLMath(self.problem.statement)

        display(self.statement_area)

        with self.statement_area:
            display(self.statement_widget)


        if self.has_answer_button:
            self.answer_button = widgets.Button(
                description='Show Answer',
                disabled=False,
                button_style='info', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to show answer',
                icon='' # (FontAwesome names without the `fa-` prefix)
            )
            self.answer_button.on_click(self.on_show_answer)
            self.answer_area = widgets.Output()
            self.answer_widget = widgets.HTMLMath(self.problem.correct_answer)

            display(self.answer_button)
            display(self.answer_area)


    def on_show_answer(self, bt):

        with self.answer_area:
            display(self.answer_widget)




    # def state_multiple_choice_problem(self, problem: MultipleChoice, input_widget=False, output_widget=False):

    #     problem_type = problem.problem_type
    #     problem_statement = problem.problem_statement

    #     input_widget = input_widget

    #     solutions = list(problem.solutions.values())

    #     # shuffle answers
    #     num_choice = len(solutions)
    #     indices = [i for i in range(num_choice)]
    #     random.shuffle(indices)

    #     # get the number of the correct answer
    #     correct_answer = int(indices.index(0) + 1)
    #     # print(correct_answer)

    #     # output jupyter cells
    #     title = '## ' + problem_type
    #     problem_statement = '#### ' + problem_statement
    #     display(Markdown(title))
    #     display(Markdown(problem_statement))
    #     display(Markdown(" Choose the Correct Answer"))

    #     for i in range(num_choice):
    #         display(Markdown('**(' + str(i + 1) + ')**  &nbsp;&nbsp;  ' + solutions[indices[i]]))
    #     display(Markdown(" Enter the **NUMBER** of the Correct Answer Below."))

    #     if input_widget:

    #         self.choice_buttons = [
    #             widgets.Button(
    #                 description='( ' + str(i + 1) + ' )',
    #                 disabled=False,
    #                 button_style='warning',  # 'success', 'info', 'warning', 'danger' or ''
    #                 tooltip='Answer choice ' + str(i + 1))
    #             for i in range(num_choice)]

    #         # Activate handler for every button
    #         for button in self.choice_buttons:
    #             # button.on_click(self.on_button_clicked,  ) # link to a click event function
    #             button.on_click(functools.partial(self.on_button_clicked, correct_answer))
    #         display(widgets.Box(self.choice_buttons))


    #     else:
    #         # Input Answer
    #         print("Your Answer")
    #         current_answer = int(input())

    #         return MultipleChoice.check_answer(correct_answer, current_answer)

    # def check_multiple_choice_answer(correct_answer, current_answer):
    #     if int(correct_answer) == int(current_answer):

    #         t = "<span style=color:green>============================================</span>"
    #         # display(Markdown(t))
    #         u = "<div class=\"alert alert-block alert-success\">Answer is CORRECT!</div>"
    #         display(Markdown(u))
    #     else:

    #         t = "<span style=color:red>============================================</span>"
    #         # display(Markdown(t))
    #         u = "<div class=\"alert alert-block alert-danger\">Answer is WRONG!</div>"
    #         display(Markdown(u))
    #         print('Correct Answer is {0}'.format(correct_answer))

    # def on_button_clicked(self, correct_answer, bt):
    #     correct_answer = correct_answer
    #     current_answer = bt.description[2:-2]
    #     # print(correct_answer)
    #     # print(current_answer)
    #     Display_Problem.check_multiple_choice_answer(correct_answer=correct_answer, current_answer=current_answer)
