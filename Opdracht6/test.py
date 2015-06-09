from lorenz import *
L1=Lorenz([-1,1,0])
u1=L1.solve(50,.01)
L2=Lorenz([-1.001,1.001,.001])
u2=L2.solve(50,.01)
print(u1[0,0],u2[0,0])
print(u1[-1,0],u2[-1,0])