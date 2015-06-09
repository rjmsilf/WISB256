from lorenz import *
L1=Lorenz([-1,1,0])
u1=L1.solve(50,.01)
print(u1[0,0])
print(u1[-1,0])