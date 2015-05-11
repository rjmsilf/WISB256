def findRoot(f,a,b,epsilon):
    m=(a+b)/2
    if f(a)*f(b)>0:
        return True
    elif f(a)==0:
        return a
    elif f(b)==0:
        return b
    elif abs(b-a)<=epsilon:
        return m
    elif f(m)*f(a)>0:
            return findRoot(f,m,b,epsilon)
    elif f(m)*f(b)>0:
            return findRoot(f,a,m,epsilon)

def findAllRoots(f,c,d,epsilon):
    rootslist2=[]
    for i in range(c,d):
        roots=findRoot(f,i,i+0.5,epsilon)
        roots2=findRoot(f,i+0.5,i+1,epsilon)
        rootslist2.append(roots)
        rootslist2.append(roots2)
    rootslist=[]
    for j in rootslist2:
        if j != True:
            rootslist.append(j)
    return rootslist
