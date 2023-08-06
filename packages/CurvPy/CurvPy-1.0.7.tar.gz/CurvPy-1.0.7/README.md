# CurvPy

Welcome to the CurvPy documentation! CurvPy is a powerful data analysis tool for performing regression analysis and optimization on datasets. This library is designed to simplify the process of analyzing and optimizing data, making it accessible to beginners and experienced data scientists. CurvPy also has a UI-based repository, which has more utilities. (CurvPy is still under development)

## Installation

You can install CurvPy using pip:

```shell
pip install curvpy
```
# Usage
## Regression Analysis
CurvPy provides a simple interface for performing regression analysis on your data. Here's an example of how to use CurvPy for regression analysis:
```shell
import numpy as np
from curvpy import datasleuth

# Example usage
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Perform regression analysis
results = datasleuth(x, y)
print(results)
```
### Result:

##### Linear Regression
Equation: y = 2.00x + 0.00
R-squared value: 1.0

##### Polynomial Regression (Degree 2)
Equation: y = 0.00x^0 + 2.00x^1 + 0.00x^2 + 0.00
R-squared value: 1.0

##### Logarithmic Regression
Equation: y = 1.36 + 4.84 * log(x)
R-squared value: 0.9473245635652926

##### Exponential Regression
Equation: y = 2.08 * exp(0.32 * x)
R-squared value: 0.9644977818927202

##### Power Law Regression
Equation: y = 2.00 * x^1.00
R-squared value: 1.0

##### Sinusoidal Regression
Equation: y = -733.82 * sin(3.14 * x + -3.14) + 6.00
R-squared value: 0.35999948635426393

# Optimization
In addition to regression analysis, CurvPy also offers an optimization module for fitting functions to your data. Here's an example of how to use CurvPy for optimization:
```shell
import numpy as np
from curvpy import optifit

# Define the function to fit
def func(x, a, b, c):
    return a * np.sin(b * x) + c

# Generate some example data
x_data = ....
y_data = ....

# Initial guess for parameters
guess_params = [1.0, 1.0, 1.0]

# Perform curve fitting and display results
fit_results = optifit(func, x_data, y_data, guess_params)
print(fit_results)
```


### Fitting results:
#### Parameters: [2.48839764 1.29229271 0.52824961]
#### Number of data points: 100
#### Number of parameters: 3
#### SSE: 20.494621282703033
#### RMSE: 0.4527098550142578
#### R-squared: 0.9358824257496368
#### Chi-square: 100.72107882471406
#### KS Test - Statistic: 0.20081623125615902
#### KS Test - p-value: 0.0005191873072093909
#### AD Test - Statistic: 0.4611616085587116
#### AD Test - Critical Values: [0.555 0.632 0.759 0.885 1.053]
#### AD Test - Significance Levels: [15. 10. 5. 2.5 1. ]

PS: (Graph will also be there)
# OptiFit_v2
In addition to OptiFit, we have another version called OptiFit_v2, which also offers an optimization module for fitting functions to your data but with some additional utilities. Here's an example of how to use CurvPy for optimization:
```shell
from curvpy import optifit_v2
import numpy as np

def func(x, a, b, c, d):
    return a * np.power(x, b) * np.exp(c * x + d)

x = np.array([10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270])
y = np.array([4823, 6402, 6186, 5551, 5073, 4773, 4353, 4017, 3779, 3480, 3132])
initial_parameters = [0.0599344694, -0.0136083382, -0.0025016990, 11.5658504714]

result = optifit_v2(func, initial_parameters, x, y)
print("Optimal parameters:", result)
```
### Result:

#### Enter the lower bounds (optional):
#### Enter the upper bounds (optional):
#### Enter the number of function evaluations (optional):
#### Optimal parameters: [5.99839516e-02, -1.36091352e-02, -2.50169054e-03, 1.15650314e+01]

# New update!
## Number of evaluations

The number of function evaluations determines the maximum number of times the model function is called during the optimization process. The optimization algorithm iteratively adjusts the parameters of the model function to minimize the difference between the predicted values and the actual data. The purpose of it is to set an upper limit on the computational time for the optimization process. If the algorithm reaches the maximum number of function evaluations specified by "maximum evaluation" before converging to a solution, it will terminate and return the current best estimate of the parameters.
## Bound parameters

The bounds parameter allows you to set lower and upper bounds for the parameters of the model function. It helps restrict the parameter search space during the optimization process. By setting bounds, you can constrain the parameters to specific ranges that make sense for your problem. The bounds parameter is a tuple of two arrays: the lower bounds and the upper bounds. For each parameter, specify the lower and upper bounds in the corresponding arrays. Setting a lower bound to -np.inf (negative infinity) means there is no lower constraint, while setting an upper bound to np.inf (positive infinity) means there is no upper constraint. Using bounds can help prevent unrealistic or invalid parameter values during optimization, improving the stability and reliability of the results.


# UI-based version of CurvPy
### CurvPy also have a UI based repository-[https://github.com/sidhu2690/CurvPy]
### More details about curvpy can be found here- [https://sidhu2690.github.io/curvpy_v2/]