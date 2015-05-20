aantal=input()
a1=[]
a2=[]
b=[]

def dubbel(w3):
    c=[]
    for k in w3:
        c.append(k)
        for i in range(0,(len(c)-2)):
            if c[i]==c[i+1]:
                del(c[i])
    woord=''.join(c)
    return woord

for i in range(0,int(aantal)):
    woord=input()
    a1.append(woord)
    a2.append(dubbel(woord))
aantal2=input()
for j in range(0,int(aantal2)):
    woord2=input()
    b.append(dubbel(woord2))



def vergelijk(w1):
    b1=[]
    for i in range(0,len(w1)):
        b1.append(w1[i])
    for k in range(0,len(a2)):
        for j in range(0,len(:
            return a1[k]
        if str(a2[k])[0]==str(w1)[0] and str(a2[k])[int(len(a2[k]))-1]==str(w1)[int(len(w1))-1]:
            return a1[k]
    doen='?'
    return doen


for i in b:
    print(vergelijk(i))