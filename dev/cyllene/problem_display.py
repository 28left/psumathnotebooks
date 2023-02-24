from IPython.display import display, clear_output
import ipywidgets as widgets
from ipywidgets import Button, GridBox, Layout


class ProblemWidget:

    def __init__(self, problem):
        self.problem = problem

        self.DisplayProblemBox = widgets.Output(layout=Layout(width='auto', grid_area='display_box'))
        self.DisplayAnswerBox = widgets.Output(layout=Layout(width='auto', grid_area='answer_box'))

        self.ShowAnswerButton = widgets.Button(description='Show Answer',
                                          layout=Layout(width='auto', height='auto', grid_area='answer_bt'),
                                          tooltip='Click to show answer',
                                          button_style='success')
        self.ShowAnswerButton.style.font_weight = 'bold'
        self.ShowAnswerButton.on_click(self.on_show_answer)
        self.show_answer_status = False

        self.StatementContainer = widgets.HTMLMath(self.problem.statement)
        self.AnswerContainer = widgets.HTMLMath(self.problem.correct_answer)

        with self.DisplayProblemBox:
            display(self.StatementContainer)

        self.Grid = GridBox(
            children=[self.DisplayProblemBox, self.ShowAnswerButton, self.DisplayAnswerBox],
            layout=Layout(
                width='70%',
                grid_template_rows='auto 50px auto',
                grid_template_columns='50% 50%',
                grid_template_areas='''
                "display_box display_box"
                "answer_bt answer_bt"
                "answer_box answer_box"
                ''')
        )

    def display_problem(self):

        display(self.Grid)

    def on_show_answer(self, bt):

        with self.DisplayAnswerBox:
            if self.show_answer_status:
                self.ShowAnswerButton.description = 'Show Answer'
                self.show_answer_status = False
                clear_output()

            else:
                # what happens when we press the button
                self.ShowAnswerButton.description = 'Hide Answer'
                self.show_answer_status = True
                display(self.AnswerContainer)

            # clear_output(wait=True)


class RegenProblemWidget(ProblemWidget):


    def __init__(self, problem):

        super().__init__(problem)

        self.NewButton = Button(description='New Problem',
                           layout=Layout(width='auto', height='auto', grid_area='new_bt'),
                           tooltip='Click to generate a new problem',
                           button_style='info')
        self.NewButton.style.font_weight = 'bold'
        self.NewButton.on_click(self.generate_new_problem)

        self.Grid = GridBox(
            children=[self.DisplayProblemBox, self.ShowAnswerButton, self.NewButton, self.DisplayAnswerBox],
            layout=Layout(
                width='80%',
                grid_template_rows='auto 50px auto',
                grid_template_columns='50% 50%',
                grid_template_areas='''
                "display_box display_box"
                "answer_bt new_bt"
                "answer_box answer_box"
                ''')
        )


    def generate_new_problem(self, bt):

        self.problem.generate()
        self.StatementContainer = widgets.HTMLMath(self.problem.statement)
        self.AnswerContainer = widgets.HTMLMath(self.problem.correct_answer)

        with self.DisplayProblemBox:
            clear_output()
            display(self.StatementContainer)
        
        with self.DisplayAnswerBox:
            if self.show_answer_status:
                self.ShowAnswerButton.description = 'Show Answer'
                self.show_answer_status = False
                clear_output()



def show_on_click(arg):
    """
    Shows or hides argument on click
    """

    def show_on_button_clicked(expr):

        with arg_out:
            clear_output()

            if expr['new'] == True:
                # what happens when we press the button
                show_button.description = 'Hide solution'
                display(arg)

            else:
                show_button.description = 'Show solution'

    show_button = widgets.ToggleButton(
        value=False,
        description='Show solution',
        disabled=False,
        button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Show solution',
    )
    show_button.observe(show_on_button_clicked, names='value')

    arg_out = widgets.Output()

    show_arg = widgets.HBox([show_button, arg_out])
    display(show_arg)

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
