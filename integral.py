import numpy as np
from numpy import sqrt, sin, cos, pi
with open("int_get.txt", "r") as file:
    for line in file:
        text = str(line)
text_fin = text.replace("y=", "")
divided = text_fin.split()
f = divided[0]
a = float(divided[1])
b = float(divided[2])
dx = 0.0001
x=a
def g(x):
    global f
    return eval(f)
sum= g(x) * dx
while x<=b:
    x+=dx
    sum+=g(x)*dx
summ = str(sum)
with open("int_out.txt", "w") as file:
    file.write(summ)
