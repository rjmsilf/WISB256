aantal=input()

a=[0,0,0,1]
def G(n):
    for i in range(4,1001):
       a.append(sum(a[(i-4):i]))
    return a[int(n)]

print(G(aantal))
