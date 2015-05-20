import math
aantal=input()
opplist=[]
n=100


def f(a,b,x):
    return (1-(a+b*x)*math.sin(2*math.pi*x))*math.exp(-(x**2))

def RiemannL(a,b,h,n):
    RL=[]
    for i in range(0,n):
        RLi=(h/n)*math.pi*(f(a,b,(i*h/n)))**2
        RL.append(RLi)
    RLsum=sum(RL)
    return RLsum

def RiemannR(a,b,h,n):
    RR=[]
    for i in range(1,n+1):
        RRi=(h/n)*math.pi*(f(a,b,(i*h/n)))**2
        RR.append(RRi)
    RRsum=sum(RR)
    return RRsum

for i in range(0,int(aantal)):
    var=input()
    varlist=var.split()
    a=float(varlist[0])
    b=float(varlist[1])
    h=float(varlist[2])
    opp=(RiemannL(a,b,h,n)+RiemannR(a,b,h,n))/2
    opplist.append(opp)
groot=max(opplist)
print(opplist.index(groot)+1)
