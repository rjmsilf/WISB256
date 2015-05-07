import random
import math
import sys

def naald(L):
    x=random.random()
    a=random.vonmisesvariate(0,0)
    eind=x+L*math.cos(a)
    if eind <= 1 and eind >= 0:
        return False
    else:
        return True

def dropnaald(N,L):
    if L>1 or L<0:
        print('L should be positive, and smaller than or equal to 1')
        return
    a = 0
    for i in range(1,N+1):
        if naald(L) == True:
            a=a+1
    pi=(2*L*N)/a
    print(str(a)+' hits in '+str(N)+' tries \nPi = '+str(pi))


L=int(sys.argv[2])
N=int(sys.argv[1])

print(dropnaald(N,L))