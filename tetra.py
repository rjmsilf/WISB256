aantal=input()
a=[]
def G(n):
    if int(n)==0:
        return 0
    elif int(n)==1:
        return 0
    elif int(n)==2:
        return 0
    elif int(n)==3:
        return 1
    else:
        antwoord=G(int(n)-1)+G(int(n)-2)+G(int(n)-3)+G(int(n)-4)
        return antwoord

for i in range(0,int(aantal)+1):
    a.append(G(i))
print(a)

