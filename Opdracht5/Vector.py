class Vector():

    def __init__(self,n,s=0):
        self.n=n
        self.start=s
        self.gramschmidt=[]
        if isinstance(self.start,int) or isinstance(self.start,float):
            a=[]
            for i in range(0,self.n):
                a.append(float(self.start))
            self.lijst=a
        elif isinstance(self.start,list):
            a=[]
            for i in range(0,self.n):
                a.append(float(self.start[i]))
            self.lijst=a

    def __str__(self):
        if isinstance(self.start,int) or isinstance(self.start,float):
            vector=str('{0:.6f}'.format(self.start))+'\n'
            for i in range(1,self.n):
                vector=vector+str('{0:.6f}'.format(self.start))+'\n'
            return vector
        elif isinstance(self.start,list):
            vector=str('{0:.6f}'.format(self.start[0]))+'\n'
            for i in range(1,self.n):
                vector=vector+str('{0:.6f}'.format(self.start[i]))+'\n'
            return vector

    def lincomb(self,v2,a=1,b=1):
        c=[]
        for i in range(0,self.n):
            c.append(a*self.lijst[i]+b*v2.lijst[i])
        return Vector(self.n,c)

    def scalar(self,a):
        c=[]
        for i in range(0,self.n):
            c.append(a*self.lijst[i])
        return Vector(self.n,c)

    def inner(self,v2):
        c=[]
        for i in range(0,self.n):
            c.append(self.lijst[i]*v2.lijst[i])
        return sum(c)

    def norm(self):
        c=[]
        for i in range(0,self.n):
            c.append(self.lijst[i]**2)
        return sum(c)**0.5

    def proj(self,v2):
        teller=self.inner(v2)
        noemer=self.inner(self)
        antwoord=self.scalar(teller/noemer)
        return antwoord
    
    def normal(self):
        breuk=(self.norm())**(-1)
        antwoord=self.scalar(breuk)
        return antwoord

def gramoptel(u,v):
    p=[]
    for i in range(0,len(u)):
        p.append(u[i].proj(v[len(u)]))
    som=p[0]
    for i in range(1,len(p)):
        som=som.lincomb(p[i])
    antwoord=som.scalar(-1)
    return antwoord

def GrammSchmidt(v):
    u=[v[0]]
    for i in range(1,len(v)):
        u.append(v[len(u)].lincomb(gramoptel(u,v)))
    e=[]
    for i in u:
        e.append(i.normal())
    return e