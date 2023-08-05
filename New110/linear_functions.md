---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import cyllene
from cyllene.MathProblems.problem_handler import ProblemHandler
from cyllene.user.problem_cmds import make_problem
from cyllene.widgets.widgets_problem_basic import MultipleChoiceWidget

import pandas as pd

from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import FormatStrFormatter

import numpy as np
import math
from random import shuffle

import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown

plt.close("all")
```

```python
%matplotlib inline
```

## Linear growth

```python
data = pd.read_csv("life-expectancy_US_Worlds.csv", index_col=0)
```

```python
x_data = data.index[2:].to_list()
y_data = data.iloc[2:,0].to_list()
```

```python
x_array = np.array(x_data).reshape((-1, 1))
y_array = np.array(y_data)
```

```python
model = LinearRegression().fit(x_array, y_array)
```

### Modeling the data using a linear function 

The graph below shows average US life expectancy for every year between 1901 and 2021 (the red dots). The $x$-axis corresponds to year $1900+x$.

Looking at the red dots, you notice that they **follow a linear trend**: with a few exceptions, the points closely follow a straight line. 

(What are the exceptions (*outliers*) and how would you explain them? In other words, what happened in the US in 1918 and in 2020-21 that had a negative impact on life expectancy?)

__*Use the sliders below the graph to match the blue line with the red dots as closely as possible.*__





```python
# Define the linear function
def linear_function(x, slope, intercept):
    return slope * x + (intercept)

# Create the interactive widget
def plot_linear_function(slope, intercept):
    x = np.linspace(0,150, 150)
    y = linear_function(x, slope, intercept)

    plt.figure(figsize=(8, 6))
    plt.scatter(range(1,len(y_data)+1),y_data,label="Real data",color="red", s=2)
    plt.plot(x, y)
    plt.xlim(0,150)
    plt.ylim(0, 100)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)

slope_slider = widgets.FloatSlider(value=(100*model.coef_[0]-15)/100, min=(100*model.coef_[0]-15)/100, max=(100*model.coef_[0]+15)/100, step=0.01, description='Slope:')
intercept_slider = widgets.FloatSlider(value=40, min=40, max=70, step=0.1, description='Intercept:')

interactive_plot = widgets.interactive_output(plot_linear_function, {'slope': slope_slider, 'intercept': intercept_slider})
display(interactive_plot, widgets.HBox([intercept_slider, slope_slider]))

```

The blue line now represents a linear function, determined by its **slope** and its **y-intercept**, that **models the data**.


---

```python
%%makeproblem P1

<<Statement>>
What does the y-intercept of the line above represent in this context?

<<Choices>>
- The average life expectancy (in years) of a US citizen in the year 1900
- The average life expectancy (in years) of a US citizen in the year 0
- The number of US citizens in 1900 (in millions)  
- The number of US citizens 56 or older in 1900 (in millions)

<<Solution>>
The value of the function at $x$ represents average US life expectancy in year $1900+x$. <br>
For the y-intercept, we set $x=0$.

<<Info>>
'tags': ["linear functions", "modeling"],
'title': "Understanding intercept",
'id': "linear functions 1",
'solution_title': "Show Hint"
```

```python
%showproblem P1
```

---

```python
%%makeproblem P2

<<Statement>>
Which about the following statements abouyt the slope $m$ of the function is true?

<<Choices>>
- Every year, US life expectancy increases by $m$ years.
- Every twenty years, US life expectancy increases by $m$ years.
- Every year, the total US population grows by $m$ million people.   
- Every twenty years, the number of US citizens older than 50 increases by $m$ million people.

<<Solution>>
The slope of a line corresponds directly to its **rate of change**: if $x$ changes by 1 year, the value of the function changes by $m$. The value of the function represents US life expectancy.

<<Info>>
'tags': ["linear functions", "modeling"],
'title': "Understanding slope",
'id': "linear functions 2",
'solution_title': "Show Hint"
```

```python
%showproblem P2
```

---


### Applying the model

Now consider the linear model alone, without the actual data. We want to use it to make predictions about the future average life expectancy of the US population.


For example, we would like to estimate the average life expectancy in 2030. For this purpose, we use the value of our model at $x=130$ (keep in mind that $x=0$ corresponds to the year 1900).

```python
def plot_linear_w_grid(slope, intercept):
    
    DP = 2
    
    x = np.linspace(0,160, 160)
    y = linear_function(x, slope, intercept)

    fig = plt.figure(figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
    fig.canvas.draw()
    ax = plt.gca()
    
    # set up axis
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # draw curve
    line, = ax.plot(x, y)
    
    # mark point
    ax.plot(x[129], y[129] , 'ro')

    # set bounds
    ax.set_xbound(0,160)
    ax.set_ybound(0,100)
    
    # format axes and grid
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.grid(True,'major',linewidth=2/DP,linestyle='-',color='#d7d7d7',zorder=0)
    ax.yaxis.grid(True,'major',linewidth=2/DP,linestyle='-',color='#d7d7d7')

    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.xaxis.grid(True,'minor',linewidth=0.5/DP,linestyle='-',color='#d7d7d7')
    ax.yaxis.grid(True,'minor',linewidth=0.5/DP,linestyle='-',color='#d7d7d7')

    ax.set_axisbelow(True)
    ax.set_aspect('equal')

#     ax.xaxis.set_major_formatter(FormatStrFormatter('%i'))
#     xticks = ax.xaxis.get_major_ticks()
#     for i,l in enumerate(xticks):
#         if not (i - 1) % 4 == 0:
#             xticks[i].label1.set_visible(False)
#         else:
#             xticks[i].label1.set_fontsize(_fontsize)

#     ax.yaxis.set_major_formatter(FormatStrFormatter('%i'))
#     yticks = ax.yaxis.get_major_ticks()
#     for i,l in enumerate(yticks):
#         if not (i - 1) % 4 == 0:
#             yticks[i].label1.set_visible(False)
#         else:
#             yticks[i].label1.set_fontsize(_fontsize)    
    
        
        
#     plt.figure(figsize=(10, 6))

#     plt.plot(x, y)
#     plt.plot(x[129], y[129] , 'ro')
#     plt.xlim(0,150)
#     plt.ylim(0, 100)
#     plt.xticks(np.arange(0, 150, step=10))
#     plt.yticks(np.arange(0, 100, step=10))
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.grid(True)
    
    
interactive_solo_plot = widgets.interactive_output(plot_linear_w_grid, {'slope': slope_slider, 'intercept': intercept_slider})
display(interactive_solo_plot)

# estimate = widgets.Label(value="Estimated US life expectancy in 1930 = " + str(linear_function(129,slope,intercept)))
    
def print_estimate(slope, intercept):
    display(Markdown("Estimated US life expectancy in 2030: **" + str(round(linear_function(130,slope,intercept),2)) + " years**"))
    
interactive_estimate = widgets.interactive_output(print_estimate, {'slope': slope_slider, 'intercept': intercept_slider})
display(interactive_estimate)
                                                  
                                                  
# user_model = widgets.Output()

# with user_model:

#     plot_linear_w_grid(ax1, slope_slider.value, intercept_slider.value)
    
# display(user_model)

# def handle_slope_slider_change(change):
    
#     with user_model:
#         fig1, ax1 = plt.subplots()
#         plot_linear_w_grid(ax1, change['new'], intercept_slider.value)
        
# slope_slider.observe(handle_slope_slider_change, names='value')



```

```python
%%makeproblem P3
<<Parameters>>

<<Statement>>
*According to the model, what is the estimated US life expectancy in 2040?*

<<Choices>>
- @{round(140*slope_slider.value+intercept_slider.value,2)}
- @{round(140*slope_slider.value+intercept_slider.value-5,2)}
- @{round(140*slope_slider.value+intercept_slider.value+15,2)}
- 140

<<Solution>>
The slope of a line corresponds directly to its **rate of change**: if $x$ changes by 1 year, the value of the function changes by $m$. The value of the function represents US life expectancy.

<<Info>>
'tags': ["linear functions", "modeling"],
'title': "Estimating future life expectancy",
'id': "linear functions 3",
'solution_title': "Show Hint"
```

```python
P3 = cyllene.ProbStack.stack["P3"]
M3 = MultipleChoiceWidget(P3.get_problem())
M3.show()
```

```python
def update_p3_choices(*args):
    choices = [str(round(linear_function(140,slope_slider.value,intercept_slider.value),2)),
               str(round(linear_function(140,slope_slider.value,intercept_slider.value),2)-5),
               str(round(linear_function(140,slope_slider.value,intercept_slider.value),2)+15),
               str(140)]
    M3.update_choices(choices)
    
intercept_slider.observe(update_p3_choices, 'value')
slope_slider.observe(update_p3_choices, 'value')
```

---


Similary, we can use the model to approximate when life expectancy crosses a certain threshold. For example, to estimate how long it will take life expectancy to reach 80 years, we have to find $x$ for which the model assumes the value $80$. 


**In the graph**, that corresponds to finding the $x$ at which the line intersection the horizontal line at $y=80$.




```python
eq = widgets.Output()
with eq:
    clear_output()
    display(widgets.HTMLMath('<p style="font-size:1.08em;"><b>Algebraically</b>, it means solving $80 = ' + str(round(slope_slider.value,2)) + 'x + ' + str(intercept_slider.value) +'$,'
                     + ' which yields $x \\approx ' 
                     + str(round((80-intercept_slider.value)/slope_slider.value,2))
                     + '$. In other words, your linear model estimates that US life expectancy first reaches 80 years in the year ' 
                     + str(math.floor((80-intercept_slider.value)/slope_slider.value)+1900) 
                     + '. Compare this to the graph above.</p>'))

display(eq)

def eq_string(*args):
    with eq:
        clear_output()
        display(widgets.HTMLMath('<p style="font-size:1.08em;"><b>Algebraically</b>, it means solving $80 = ' + str(round(slope_slider.value,2)) + 'x + ' + str(intercept_slider.value) +'$,'
                     + ' which yields $x \\approx ' 
                     + str(round((80-intercept_slider.value)/slope_slider.value,2))
                     + '$. In other words, your linear model estimates that US life expectancy first reaches 80 years in the year ' 
                     + str(math.floor((80-intercept_slider.value)/slope_slider.value)+1900) 
                     + '. Compare this to the graph above.</p>'))

intercept_slider.observe(eq_string, 'value')
slope_slider.observe(eq_string, 'value')
```

```python
%%makeproblem P4
<<Parameters>>

<<Statement>>
*According to the model, when will US life expectancy reach 90 years?*

<<Choices>>
- @{math.floor((90-intercept_slider.value)/slope_slider.value)+1900}
- @{math.floor((100-intercept_slider.value)/slope_slider.value)+1900}
- @{math.floor(90*slope_slider.value+intercept_slider.value)+1900}
- @{math.floor(150*slope_slider.value+intercept_slider.value)+1900}

<<Solution>>
You need to solve $90 = \text{slope}*x + \text{intercept}$ for $x$.

<<Info>>
'tags': ["linear functions", "modeling"],
'title': "Estimating life expectancy milestones",
'id': "linear functions 4",
'solution_title': "Show Hint"
```

```python
P4 = cyllene.ProbStack.stack["P4"]
M4 = MultipleChoiceWidget(P4.get_problem())
M4.show()
```

```python
def update_p4_choices(*args):
    choices = [str(math.floor((90-intercept_slider.value)/slope_slider.value)+1900),
               str(math.floor((100-intercept_slider.value)/slope_slider.value)+1900),
               str(math.floor(90*slope_slider.value+intercept_slider.value)+1900),
               str(math.floor(150*slope_slider.value+intercept_slider.value)+1900)]
    M4.update_choices(choices)
    
intercept_slider.observe(update_p4_choices, 'value')
slope_slider.observe(update_p4_choices, 'value')
```

---
## Outline


Brief review linear functions


Question: What does the y-intercept (value) represent here?


Multiple choice

(Explanation on submit; hint if they miss)


Question: What does the slope represent?


Application: Use model to estimate (extrapolate etc)

- 1 example for each question
- then student tries the other cases (multiple choice) 
- feedback graph on submit


Now encourage to go back and change the model, and and do the estimates again

- show graph again (restrict data set)
- keep flow linear


Finish with average rate of change

- quick summary quiz
