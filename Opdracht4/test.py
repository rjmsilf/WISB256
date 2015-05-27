import bisection
import math

def f(x):
    return math.sin(x)
    
antwoord=bisection.findAllRoots(f,-2,2,1e-15)
print(antwoord)