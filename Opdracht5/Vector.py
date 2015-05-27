class Vector():

    def __init__(self,n,s=0):
        self.n=n
        self.start=s
        if isinstance(self.start,int) or isinstance(self.start,float):
            a=[]
            for i in range(0,self.n):
                a.append(float(self.start))
            self.lijst=a
        if isinstance(self.start,list):
            a=[]
            for i in range(0,self.n):
                a.append(float(self.start[i]))
            self.lijst=a

    def __str__(self):
        if isinstance(self.start,int) or isinstance(self.start,float):
            vector=str(float(self.start))+'\n'
            for i in range(1,self.n):
                vector=vector+str(float(self.start))+'\n'
            return vector
        elif isinstance(self.start,list):
            vector=str(float(self.start[0]))+'\n'
            for i in range(1,self.n):
                vector=vector+str(float(self.start[i]))+'\n'
            return vector

    def lincomb(self,v2,a,b):
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
