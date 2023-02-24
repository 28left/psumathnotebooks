---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
import cyllene
# import cyllene.widgets.vue_problem_basic as v
# import cyllene.widgets.vue_problem_parameter as vp
```

# Review Problems from Exam 2

+++

## Problem 1

```{code-cell} ipython3
%%makeproblem -wa 3418886
Question
<eqn>
A = randnum(3,5,1);
B = A*randnum(2,4,1) + randnum(-1,1,2);
if A == 3:
    n = pickone(4,5,7,8);
if A == 4:
    n = pickone(3,5,7,9);
if A == 5:
    n = pickone(3,4,6,7);
nn = n - 1;
m = randnum(3,6,1,n); 
mm = m - 1; 
mmm = m+1;
ERRS = pick(7,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10);
EQNS = [A, n, m*A, 2*m, A*n, n*B, A*(n - m), n*B + ERRS[0], A*(n - m) + ERRS[1], n*B + ERRS[2], A*(n - m) + ERRS[3], n*B + ERRS[4], A*(n - m) + ERRS[6]];
''</eqn>

<watex>
Given the function \[f(x) = \dfrac{x^{$n}}{(${A}x + $B)^{$m}},\] find its derivative \[f'(x)\].
</watex>

<_>

Answer
<watex>\[\dfrac{x^{$nn}($EQNS[6]x + $EQNS[5])}{($EQNS[0]x + $B)^{$mmm}}\]</watex>
<watex>\[\dfrac{$EQNS[5]x^{$nn}}{($EQNS[0]x + $B)^{$mmm}}\]</watex>
<watex>\[\dfrac{x^{$nn}($EQNS[8]x + $EQNS[7])}{($EQNS[0]x + $B)^{$mmm}}\]</watex>
<watex>\[\dfrac{$EQNS[10]x + $EQNS[9]}{($EQNS[0]x + $B)^{$mmm}}\]</watex>
<watex>\[\dfrac{x^{$nn}($EQNS[12]x + $EQNS[11])}{($EQNS[0]x + $B)^{$mmm}}\]</watex>


Solution
<watex>
Start by using the quotient rule to compute the derivative of \[f(x) = \dfrac{x^{$n}}{($EQNS[0]x + $B)^{$m}}\]:
<br><br>
<center>\[ 
f'(x)   = \dfrac{$EQNS[1]x^{$nn}($EQNS[0]x + $B)^{$m} - x^{$n}\cdot$m($EQNS[0]x + $B)^{$mm}\cdot$EQNS[0]}{[($EQNS[0]x + $B)^{$m}]^2} 
 = \dfrac{$EQNS[1]x^{$nn}($EQNS[0]x + $B)^{$m} - $EQNS[2]x^{$n}($EQNS[0]x + $B)^{$mm}}{($EQNS[0]x+$B)^{$EQNS[3]}} 
\]</center> 
<br>
Note the factor of \[$A\], which is the derivative of \[${A}x + $B\], that shows up in the second term of the numerator as a result of applying the chain rule.  Now simplify the numerator by pulling out the common factors of \[x^{$nn}\] and \[(${A}x + $B)^{$mm}\]:
<br><br>
<center>\[
f'(x)  = \dfrac{x^{$nn}($EQNS[0]x + $B)^{$mm}[$EQNS[1]($EQNS[0]x + $B) - $EQNS[2]x]}{($EQNS[0]x + $B)^{$EQNS[3]}}
= \dfrac{x^{$nn}($EQNS[0]x + $B)^{$mm}[$EQNS[4]x + $EQNS[5] - $EQNS[2]x]}{($EQNS[0]x + $B)^{$EQNS[3]}}
= \dfrac{x^{$nn}($EQNS[6]x + $EQNS[5])}{($EQNS[0]x + $B)^{$mmm}}
\]</center> 
</watex>

Info
'tags': ["derivative", "chain rule"],
'title': "Find derivative",
'id': "3418886"
```

```{code-cell} ipython3
%showproblem 3418886
```

---

+++

## Problem 2

```{code-cell} ipython3
%%makeproblem -wa 5200357
Question
<eqn>
A = randnum(2,9,1);
B = randnum(2,5,1,A);
SLOPE = fraction(A*B - 1,B);
EQNS = [A*B, A*B + 1, A*B + 2, A*B - 1, A*B + 1 - B, A, B];
''</eqn>

<watex>
Find an equation for the tangent line to the curve \[y = ${A}x + \dfrac{$B}{x}\] at the point \[($B,$EQNS[1])\].
</watex>

<_>

Answer
<watex>\[y = \dfrac{$EQNS[3]}{$B}x + 2\]</watex>
<watex>\[y = \dfrac{$EQNS[1]}{$B}x\]</watex>
<watex>\[y = \dfrac{1}{$B}x + $EQNS[0]\]</watex>
<watex>\[y = -\dfrac{1}{$B}x + $EQNS[2]\]</watex>
<watex>\[y = x + $EQNS[4]\]</watex>

Solution
<watex>
If we rewrite \[y = $EQNS[5]x + \dfrac{$B}{x}\] as \[ y = $EQNS[5]x + $EQNS[6]x^{-1}\], then we can compute its derivative as follows.
<br><br>
<center>\[
y' = $A + $B(-1)x^{-2} = $A - \dfrac{$B}{x^2}
\]</center>
<br>
Now plug in \[x = $B\].
<br><br>
<center>\[
y'($B) = $A - \dfrac{$B}{$B^2} = $A - \dfrac{1}{$B} = \dfrac{$A*$B - 1}{$B} = \dfrac{$EQNS[3]}{$B}
\]</center>
<br>
We now know that the slope of the tangent line is \[\dfrac{$EQNS[3]}{$B}\].  Using the point-slope equation of a line (i.e., \[y - b = m(x - a)\] where \[m\] is the slope of the line that goes through the point \[(a,b)\]), the equation of the tangent line is given by the following.
<br><br>
<center>\[
y - $EQNS[1] = \dfrac{$EQNS[3]}{$B}(x - $B) = \dfrac{$EQNS[3]}{$B}x - $EQNS[3]
\]</center>
<br>
Adding \[$EQNS[1]\] to both sides yields
<br><br>
<center>\[y  = \dfrac{$EQNS[3]}{$B}x + 2\]</center>
</watex>

Info
'tags': ["derivative", "tangent line"],
'title': "Find equation of tangent line",
'id': "5200357"
```

```{code-cell} ipython3
%showproblem 5200357
```

```{code-cell} ipython3

```
