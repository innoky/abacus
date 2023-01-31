
from sympy.solvers import solve
from sympy import Symbol, diff, symbols, cos, sin, tan, sqrt
x, y = symbols("x y") 

result = (diff(x))
with open("diff_result.txt", "w") as file:
    file.write(str(result))