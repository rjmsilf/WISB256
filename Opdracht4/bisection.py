def findRoot(f,a,b,epsilon):
    m=(a+b)/2
    if f(a)*f(b)>0:
        return 'fietsbandventieldopje'
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
    n=100000
    for i in range(0,n):
        roots=findRoot(f,c+i*(d-c)/n,c+(i+1)*(d-c)/n,epsilon)
        rootslist2.append(roots)
    rootslist3=[]
    for j in rootslist2:
        if j != 'fietsbandventieldopje':
            rootslist3.append(j)
    rootslist=list(set(rootslist3))
    return rootslist
    
    

