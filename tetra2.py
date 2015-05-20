aantal=input()
a=[0,0,0,1]
def G(n):
    for i in range(4,int(n)+1):
       a.append(sum(a[(i-4):i]))
    return a

print(G(aantal))