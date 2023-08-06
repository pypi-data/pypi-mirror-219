<!-- #region -->
# Numerical methods
Implementation of methods for solving mathematical problems in numerical form

### Integrals
Let's try calculate integral $\int_{-1}^{4} \! (2x^2-3) \, \mathrm{d}x = \frac {85} 3$

The whole code avialable in [notebook](examples_numerical_methods.ipynb) in this repo

At first, we will find analytical (exact) solution:
```bash
$ pip install sympy
```
```python 
from sympy import symbols, integrate
x = symbols('x')
f = (2*x**2 - 3)
display(integrate(f, (x, -1, 4)))
```
$\frac{85}{3}$
```python
exact_solution = 85/3
print(f"exact solution = {exact_solution}")
```
<pre>
>>> exact solution = 28.333333333333332
</pre>

Now we will calculate it numerically by rectangle method with 10 rectangles:

$I = \int_{a}^b f(x) \mathrm dx \approx \sum_{i=0}^{n-1}f(x_i)(x_{i+1}-x_i)$
```python
from integrate import rectangle_method
def f(x):
    return 2*x**2 - 3
integral = rectangle_method(-1, 4, 10)
print("Approximate integral:", integral[0])
print('Difference between exact and approximate solutions equals', abs(exact_solution - integral[0]))
```
<pre >>>> Approximate integral: 28.125
>>> Difference between exact and approximate solutions equals 0.20833333333333215 </pre>
After increasing number of rectangles (from 10 to 100) difference between exact and approximate solutions is less significant:
```python
integral = rectangle_method(-1, 4, 100)
print('Exact solution = ', exact_solution)
print("Approximate integral:", integral[0])
print(f'Difference between exact and approximate solutions equals {abs(exact_solution - integral[0]):.15f}')
```
<pre > >>> Exact solution =  28.333333333333332
 >>> Approximate integral: 28.331249999999958
 >>> Difference between exact and approximate solutions equals 0.002083333333374
</pre>

### to be continued in close times
<!-- #endregion -->
