import bisection
import math

def f(x):
    return math.sin(x)
    
root=bisection.findAllRoots(f,0,9,1e-15)
print(root)