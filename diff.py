
from sympy.solvers import solve
from sympy import Symbol, diff, symbols, cos, sin, tan, sqrt
x, y = symbols("x y") 

result = (diff(5*sin(6*x)-3))
with open("diff_result.txt", "w") as file:
    file.write(str(result))