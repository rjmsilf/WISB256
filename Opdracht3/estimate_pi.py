import random
import math
import sys

if len(sys.argv)==4:
    seed=int(sys.argv[3])
    random.seed(seed)
    

def naald(L):
    x=random.random()
    a=random.vonmisesvariate(0,0)
    eind=x+L*math.cos(a)
    if eind <= 1 and eind >= 0:
        return False
    else:
        return True


def dropnaald(N,L):
    if L<=0:
        return 'AssertionError: L should be positive'
    if L<=1 and L>0:
        a=0
        for i in range(1,N+1):
            if naald(L) == True:
                a=a+1
        pi=(2*L*N)/a
        return str(a)+' hits in '+str(N)+' tries \nPi = '+str(pi)
    elif L>1:
        b=0
        for j in range(1,N+1):
            if naald(L) == True:
                b=b+1
        pi2=(2*N*(L-(L**2-1)**0.5 - math.asin(1/L)))/(b-N)
        return str(b)+' hits in '+str(N)+' tries \nPi = '+str(pi2)

def checkinput():
    if len(sys.argv)<3:
        return 'Use: estimate_pi.py N L'
    else:
        N=int(sys.argv[1])
        L=float(sys.argv[2])
        return dropnaald(N,L)

print(checkinput())