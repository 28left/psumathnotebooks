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

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}}
import cyllene
from cyllene.MathProblems.problem_handler import ProblemHandler
from cyllene.user.problem_cmds import make_problem
from cyllene.widgets.widgets_problem_basic import MultipleChoiceWidget
from cyllene.widgets.widgets_problem_param import MultipleChoiceParameterWidget
from cyllene.widgets.vue_problem_basic import VueMultipleChoiceWidget
from cyllene.widgets.vue_problem_parameter import VueParameterMultipleChoiceWidget



import pandas as pd

from sklearn.linear_model import LinearRegression

import bqplot.pyplot as plt

# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator, FormatStrFormatter
# from matplotlib.ticker import FormatStrFormatter

import numpy as np
import math
from random import shuffle
import markdown as md

import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown, Math

plt.close("all")
# plt.set_loglevel("info") 

# suppress debug logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
```

<!-- #region extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": 0, "height": 3, "hidden": false, "locked": false, "row": 0, "width": 12}}}} -->
## Linear growth
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}}
data = pd.read_csv("life-expectancy_US_Worlds.csv", index_col=0)
```

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}}
x_data = data.index[2:].to_list()
y_data = data.iloc[2:,0].to_list()
```

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}}
x_array = np.array(x_data).reshape((-1, 1))
y_array = np.array(y_data)
```

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}}
model = LinearRegression().fit(x_array, y_array)
```

<!-- #region extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": 8, "height": 3, "hidden": false, "locked": false, "row": 3, "width": 4}}}} -->
### Modeling the data using a linear function 
<!-- #endregion -->

<!-- #region extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": 8, "height": 11, "hidden": false, "locked": false, "row": 6, "width": 4}}}} -->
The graph below shows average US life expectancy for every year between 1901 and 2021 (the red dots). The $x$-axis corresponds to year $1900+x$.

Looking at the red dots, you notice that they **follow a linear trend**: with a few exceptions, the points closely follow a straight line. 

(What are the exceptions (*outliers*) and how would you explain them? In other words, what happened in the US in 1918 and in 2020-21 that had a negative impact on life expectancy?)

__*Use the sliders below the graph to match the blue line with the red dots as closely as possible.*__




<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"hidden": false, "col": 0, "row": 3, "width": 8, "height": 18, "locked": false}}}}
# Define the linear function
def linear_function(x, slope, intercept):
    return slope * x + (intercept)

x = np.linspace(0,150, 150)
y = linear_function(x, (100*model.coef_[0]-15)/100, 40)
fig = plt.figure(layout=dict(height="500px", width="1000px"))
plt.scatter(range(1,len(y_data)+1),y_data,stroke="red")
plt.xlim(0,150)
plt.ylim(0,100)
plt.xlabel('x')
plt.ylabel('y')

curve = plt.plot(x=x, y=y, colors=["green"], stroke_width=3)
   
# update plot
def plot_linear_function(slope, intercept):
        
    with curve.hold_sync():
        curve.y = linear_function(x, slope, intercept)

slope_slider = widgets.FloatSlider(value=(100*model.coef_[0]-15)/100, min=(100*model.coef_[0]-15)/100, max=(100*model.coef_[0]+15)/100, step=0.01, description='Slope:')
intercept_slider = widgets.FloatSlider(value=40, min=40, max=70, step=0.1, description='Intercept:')

interactive_plot = widgets.interactive_output(plot_linear_function, {'slope': slope_slider, 'intercept': intercept_slider})
output = widgets.Output()

with output:
    plt.show()
    
display(output, widgets.HBox([intercept_slider, slope_slider]))

```

<!-- #region extensions={"jupyter_dashboards": {"version": 1, "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "locked": true, "row": null, "width": 2}}}} -->
The blue line now represents a linear function, determined by its **slope** and its **y-intercept**, that **models the data**.
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"hidden": true, "row": null, "col": null, "width": 2, "height": 2, "locked": true}}}}

```
