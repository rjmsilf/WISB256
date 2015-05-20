aantal=input()
a=aantal.split()

def reken(n):
    for i in range(0,n):
        if a[i]=='+':
            a[i]=str(float(a[i-2])+float(a[i-1]))
            del(a[(i-2):i])
            return a
        elif a[i]=='-':
            a[i]=str(float(a[i-2])-float(a[i-1]))
            del(a[(i-2):i])
            return a
        elif a[i]=='*':
            a[i]=str(float(a[i-2])*float(a[i-1]))
            del(a[(i-2):i])
            return a
        elif a[i]=='/':
            a[i]=str(float(a[i-2])/float(a[i-1]))
            del(a[(i-2):i])
            return a

while len(a)>1:
    reken(len(a))
antwoord='{0:.3f}'.format(float(a[0]))
print(antwoord)
